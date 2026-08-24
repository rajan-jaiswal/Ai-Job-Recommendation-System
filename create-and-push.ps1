# Script to create GitHub repository and push code
# This requires a GitHub Personal Access Token

param(
    [string]$RepoName = "job-recommendation",
    [string]$GitHubUsername = "rajan-jaiswal",
    [string]$Token = ""
)

Write-Host "GitHub Repository Creation and Push Script" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

# Get token if not provided
if ([string]::IsNullOrWhiteSpace($Token)) {
    Write-Host "You need a GitHub Personal Access Token to create a repository." -ForegroundColor Yellow
    Write-Host "Get one at: https://github.com/settings/tokens" -ForegroundColor Yellow
    Write-Host "Required scopes: repo (Full control of private repositories)" -ForegroundColor Yellow
    Write-Host ""
    $Token = Read-Host "Enter your GitHub Personal Access Token" -AsSecureString
    $Token = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Token)
    )
}

if ([string]::IsNullOrWhiteSpace($Token)) {
    Write-Host "Token is required. Exiting." -ForegroundColor Red
    exit 1
}

# Create repository via GitHub API
Write-Host "Creating repository '$RepoName' on GitHub..." -ForegroundColor Cyan

$headers = @{
    "Authorization" = "token $Token"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    name = $RepoName
    description = "Smart Career Recommendation System - AI-powered job recommendations based on skills and interests"
    private = $false
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "Repository created successfully!" -ForegroundColor Green
    Write-Host "Repository URL: $($response.html_url)" -ForegroundColor Green
} catch {
    Write-Host "Error creating repository: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "Authentication failed. Please check your token." -ForegroundColor Red
    } elseif ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "Repository might already exist. Trying to push anyway..." -ForegroundColor Yellow
    } else {
        exit 1
    }
}

Write-Host ""
Write-Host "Setting up git remote..." -ForegroundColor Cyan

# Remove existing remote if any
git remote remove origin 2>$null

# Add remote
git remote add origin "https://$Token@github.com/$GitHubUsername/$RepoName.git"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error setting remote. Trying without token in URL..." -ForegroundColor Yellow
    git remote remove origin 2>$null
    git remote add origin "https://github.com/$GitHubUsername/$RepoName.git"
}

# Rename branch to main
Write-Host "Renaming branch to 'main'..." -ForegroundColor Cyan
git branch -M main

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
$env:GIT_TERMINAL_PROMPT = 0
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Success! Your code has been pushed to GitHub." -ForegroundColor Green
    Write-Host "Repository: https://github.com/$GitHubUsername/$RepoName" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Push failed. You may need to:" -ForegroundColor Red
    Write-Host "1. Use a Personal Access Token for authentication" -ForegroundColor Yellow
    Write-Host "2. Or use SSH: git remote set-url origin git@github.com:$GitHubUsername/$RepoName.git" -ForegroundColor Yellow
}
