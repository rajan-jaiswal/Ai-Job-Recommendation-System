"""
API Configuration for Job Search Services
Store your API keys here for real job search functionality

SECURITY NOTE: For production, use environment variables instead of hardcoding keys.
Set environment variables like: export RAPIDAPI_KEY="your_key_here"
"""

import os

# Job Search API Configuration
# Get your API keys from the respective services
# Priority: Environment variables > Hardcoded values (for local dev only)

# RapidAPI Keys (for JSearch and Indeed APIs)
# Use environment variable if available, otherwise use local dev key
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')

# JSearch API Configuration
JSEARCH_API_KEY = RAPIDAPI_KEY
JSEARCH_ENABLED = True  # Enabled for real job search with resume upload

# Indeed API Configuration  
INDEED_API_KEY = RAPIDAPI_KEY
INDEED_ENABLED = False  # Set to True when you have an API key

# Alternative Job Search APIs
# You can add more APIs here as needed

# LinkedIn Jobs API (requires special approval)
LINKEDIN_CLIENT_ID = "YOUR_LINKEDIN_CLIENT_ID"
LINKEDIN_CLIENT_SECRET = "YOUR_LINKEDIN_CLIENT_SECRET"
LINKEDIN_ENABLED = False

# GitHub Jobs API (deprecated but still works for some data)
GITHUB_JOBS_ENABLED = False

# ZipRecruiter API
ZIPRECRUITER_API_KEY = "YOUR_ZIPRECRUITER_API_KEY"
ZIPRECRUITER_ENABLED = False

# API Rate Limits (requests per minute)
API_RATE_LIMITS = {
    'jsearch': 100,
    'indeed': 50,
    'linkedin': 200,
    'github': 60,
    'ziprecruiter': 100
}

# Job Search Settings
DEFAULT_JOB_TYPE = 'fulltime'
DEFAULT_NUM_PAGES = 1
DEFAULT_JOBS_PER_PAGE = 10
MAX_JOBS_PER_SEARCH = 50

# Fallback Settings
USE_FALLBACK_JOBS = True  # Use sample jobs when APIs are not available
FALLBACK_JOB_COUNT = 5

# Instructions for getting API keys:
"""
1. JSearch API (Recommended):
   - Go to https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
   - Subscribe to the API (free tier available)
   - Copy your RapidAPI key
   - Set JSEARCH_ENABLED = True

2. Indeed API:
   - Go to https://rapidapi.com/letscrape-6bRBa3QguO5/api/indeed-indeed
   - Subscribe to the API
   - Copy your RapidAPI key
   - Set INDEED_ENABLED = True

3. LinkedIn Jobs API:
   - Go to https://developer.linkedin.com/
   - Create an application
   - Get client ID and secret
   - Set LINKEDIN_ENABLED = True

4. ZipRecruiter API:
   - Go to https://www.ziprecruiter.com/employers/api
   - Apply for API access
   - Get your API key
   - Set ZIPRECRUITER_ENABLED = True
"""

def get_api_config():
    """Get current API configuration"""
    return {
        'jsearch': {
            'enabled': JSEARCH_ENABLED,
            'api_key': JSEARCH_API_KEY
        },
        'indeed': {
            'enabled': INDEED_ENABLED,
            'api_key': INDEED_API_KEY
        },
        'linkedin': {
            'enabled': LINKEDIN_ENABLED,
            'client_id': LINKEDIN_CLIENT_ID,
            'client_secret': LINKEDIN_CLIENT_SECRET
        },
        'github': {
            'enabled': GITHUB_JOBS_ENABLED
        },
        'ziprecruiter': {
            'enabled': ZIPRECRUITER_ENABLED,
            'api_key': ZIPRECRUITER_API_KEY
        }
    }

def is_any_api_enabled():
    """Check if any job search API is enabled"""
    config = get_api_config()
    return any(api['enabled'] for api in config.values())
