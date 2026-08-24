# GitHub Push Instructions

Your project is ready to be pushed to GitHub! Follow these steps:

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository:
   - Repository name: `job-recommendation` (or your preferred name)
   - Description: "Smart Career Recommendation System"
   - Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

## Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Use these:

```bash
# Navigate to your project directory
cd "C:\Users\RAJAN\Desktop\job recommendation"

# Add the remote repository (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Verify Push

1. Go to your GitHub repository page
2. You should see all your files there
3. Check that `.gitignore`, `vercel.json`, and `api/index.py` are present

## ⚠️ Important Security Note

**Before pushing, consider securing your API keys:**

Your `api_config.py` file contains an API key. You have two options:

### Option A: Remove API Key (Recommended for Public Repos)
1. Edit `api_config.py`
2. Replace the actual API key with a placeholder:
   ```python
   RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY_HERE"
   ```
3. Add `api_config.py` to `.gitignore` (already done)
4. Create a `api_config.example.py` with placeholder values

### Option B: Keep it Private
- Make sure your GitHub repository is set to **Private**
- Only share with trusted collaborators

## Quick Push Script

You can also use this PowerShell script (save as `push-to-github.ps1`):

```powershell
# Replace these variables
$GITHUB_USERNAME = "YOUR_USERNAME"
$REPO_NAME = "job-recommendation"

# Add remote
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Push
git branch -M main
git push -u origin main
```

## Next Steps After Pushing

1. **Deploy to Vercel**: See `VERCEL_DEPLOYMENT.md` for instructions
2. **Set up CI/CD**: Consider adding GitHub Actions for automated testing
3. **Add collaborators**: Invite team members if needed

## Troubleshooting

### Authentication Issues
If you get authentication errors:
- Use GitHub Personal Access Token instead of password
- Or use SSH: `git remote set-url origin git@github.com:USERNAME/REPO.git`

### Remote Already Exists
If you get "remote origin already exists":
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Push Rejected
If push is rejected:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```
