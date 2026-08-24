# PowerShell script to push project to GitHub
# Usage: .\push-to-github.ps1

Write-Host "GitHub Push Script" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green
Write-Host ""

# Get GitHub username
$username = Read-Host "Enter your GitHub username"

# Get repository name
$repoName = Read-Host "Enter your repository name (or press Enter for 'job-recommendation')"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "job-recommendation"
}

Write-Host ""
Write-Host "Repository URL: https://github.com/$username/$repoName" -ForegroundColor Yellow
Write-Host ""

# Check if remote already exists
$remoteExists = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote 'origin' already exists: $remoteExists" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/n)"
    if ($overwrite -eq "y" -or $overwrite -eq "Y") {
        git remote remove origin
        Write-Host "Removed existing remote" -ForegroundColor Green
    } else {
        Write-Host "Keeping existing remote. Exiting." -ForegroundColor Red
        exit
    }
}

# Add remote
Write-Host "Adding remote repository..." -ForegroundColor Cyan
git remote add origin "https://github.com/$username/$repoName.git"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error adding remote. Please check your repository name and try again." -ForegroundColor Red
    exit 1
}

# Rename branch to main
Write-Host "Renaming branch to 'main'..." -ForegroundColor Cyan
git branch -M main

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "You may be prompted for your GitHub credentials." -ForegroundColor Yellow
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Success! Your code has been pushed to GitHub." -ForegroundColor Green
    Write-Host "Repository: https://github.com/$username/$repoName" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Push failed. Please check:" -ForegroundColor Red
    Write-Host "1. Repository exists on GitHub" -ForegroundColor Yellow
    Write-Host "2. You have access to the repository" -ForegroundColor Yellow
    Write-Host "3. Your GitHub credentials are correct" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "For authentication issues, consider using:" -ForegroundColor Yellow
    Write-Host "- GitHub Personal Access Token (instead of password)" -ForegroundColor Yellow
    Write-Host "- SSH keys: git remote set-url origin git@github.com:$username/$repoName.git" -ForegroundColor Yellow
}
