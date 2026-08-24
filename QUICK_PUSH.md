# Quick Push to GitHub

Since the repository doesn't exist yet, you have two options:

## Option 1: Create Repository Manually (Easiest)

1. **Go to GitHub**: https://github.com/new
2. **Create Repository**:
   - Repository name: `job-recommendation`
   - Description: "Smart Career Recommendation System"
   - Choose **Public** or **Private**
   - **DO NOT** check "Initialize with README" (we already have files)
3. **Click "Create repository"**
4. **Then run these commands**:

```powershell
cd "C:\Users\RAJAN\Desktop\job recommendation"
git remote remove origin 2>$null
git remote add origin https://github.com/rajan-jaiswal/job-recommendation.git
git branch -M main
git push -u origin main
```

**Note**: You'll be prompted for GitHub credentials. Use:
- **Username**: rajan-jaiswal
- **Password**: Use a **Personal Access Token** (not your GitHub password)
  - Get token at: https://github.com/settings/tokens
  - Create token with `repo` scope

## Option 2: Use the Automated Script

Run the PowerShell script that will create the repo and push:

```powershell
cd "C:\Users\RAJAN\Desktop\job recommendation"
.\create-and-push.ps1
```

This script will:
1. Ask for your GitHub Personal Access Token
2. Create the repository via GitHub API
3. Push your code automatically

**Get Personal Access Token**:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it: "Job Recommendation Push"
4. Select scope: **repo** (Full control of private repositories)
5. Click "Generate token"
6. Copy the token (you won't see it again!)

## After Pushing

Once pushed, your repository will be available at:
**https://github.com/rajan-jaiswal/job-recommendation**

Then you can deploy to Vercel by:
1. Going to https://vercel.com
2. Importing the repository
3. Clicking Deploy
