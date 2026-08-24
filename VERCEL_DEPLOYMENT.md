# Vercel Deployment Guide

This project is configured for deployment on Vercel. Follow these steps to deploy:

## Prerequisites

1. A GitHub account
2. A Vercel account (sign up at https://vercel.com)

## Deployment Steps

### 1. Push to GitHub

If you haven't already pushed to GitHub:

```bash
# Create a new repository on GitHub (don't initialize with README)
# Then run these commands:

git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# For production deployment
vercel --prod
```

#### Option B: Using Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New Project"
3. Import your GitHub repository
4. Vercel will automatically detect the configuration:
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`
5. Click "Deploy"

### 3. Environment Variables (Optional)

If you want to use environment variables for API keys:

1. Go to your project settings on Vercel
2. Navigate to "Environment Variables"
3. Add your API keys:
   - `RAPIDAPI_KEY`: Your RapidAPI key
   - `JSEARCH_ENABLED`: true/false
   - `INDEED_ENABLED`: true/false
   - etc.

Then update `api_config.py` to read from environment variables:

```python
import os

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', 'your_default_key')
```

### 4. Important Notes

- **File Uploads**: The `/uploads` directory is ephemeral on Vercel. Files uploaded will be lost after the function execution. Consider using a cloud storage service (AWS S3, Cloudinary, etc.) for production.

- **API Keys**: Make sure to remove or secure your API keys in `api_config.py` before pushing to GitHub. Consider using environment variables instead.

- **Function Timeout**: Vercel has a 10-second timeout for Hobby plan and 60 seconds for Pro plan. Make sure your API calls complete within this time.

- **Cold Starts**: Serverless functions may have cold starts. The first request might be slower.

### 5. Custom Domain (Optional)

1. Go to your project settings on Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Follow the DNS configuration instructions

## Troubleshooting

### Build Fails

- Check that all dependencies in `requirements.txt` are compatible with Python 3.9
- Ensure `api/index.py` exists and properly imports the Flask app

### Function Timeout

- Optimize your code to reduce execution time
- Consider upgrading to Vercel Pro for longer timeouts
- Use caching where possible

### Import Errors

- Make sure all Python files are in the correct directories
- Check that `api/index.py` has the correct path to import `app.py`

## Project Structure

```
.
├── api/
│   └── index.py          # Vercel serverless function wrapper
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── uploads/              # Upload directory (ephemeral on Vercel)
├── app.py                # Main Flask application
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Support

For Vercel-specific issues, check:
- Vercel Documentation: https://vercel.com/docs
- Vercel Python Runtime: https://vercel.com/docs/runtimes/python
