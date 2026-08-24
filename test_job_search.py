#!/usr/bin/env python3
"""
Test script for job search functionality with real API
"""

import requests
import json
from job_search_service import JobSearchService

def test_job_search_api():
    """Test the job search API directly"""
    print("🔍 Testing Job Search API with your RapidAPI key...")
    print("=" * 60)
    
    # Test the API directly
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": "43774399d4msh623b25b4b75f9d5p1cbae2jsn5b099e5e9e62"
    }
    
    params = {
        "query": "software engineer",
        "page": 1,
        "num_pages": 1,
        "country": "us",
        "date_posted": "month"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ API Response Status: {response.status_code}")
        print(f"📊 Found {len(data.get('data', []))} jobs")
        
        if 'data' in data and data['data']:
            print("\n🎯 Sample Job Postings:")
            print("-" * 40)
            
            for i, job in enumerate(data['data'][:3], 1):
                print(f"\n{i}. {job.get('job_title', 'N/A')}")
                print(f"   Company: {job.get('employer_name', 'N/A')}")
                print(f"   Location: {job.get('job_city', 'N/A')}, {job.get('job_state', 'N/A')}")
                print(f"   Salary: {job.get('job_salary', 'Not specified')}")
                print(f"   Posted: {job.get('job_posted_at_datetime_utc', 'N/A')}")
                print(f"   Apply: {job.get('job_apply_link', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return False

def test_job_search_service():
    """Test the integrated job search service"""
    print("\n🔧 Testing Integrated Job Search Service...")
    print("=" * 60)
    
    try:
        # Initialize job search service
        job_service = JobSearchService()
        
        # Test job search
        jobs = job_service.search_jobs(
            job_title="Software Engineer",
            location="Chicago",
            skills=["Python", "JavaScript", "React"],
            job_type="fulltime",
            num_pages=1
        )
        
        print(f"✅ Job Search Service: Found {len(jobs)} jobs")
        
        if jobs:
            print("\n🎯 Real Job Results:")
            print("-" * 40)
            
            for i, job in enumerate(jobs[:3], 1):
                print(f"\n{i}. {job['title']}")
                print(f"   Company: {job['company']}")
                print(f"   Location: {job['location']}")
                print(f"   Salary: {job['salary']}")
                print(f"   Source: {job['source']}")
                print(f"   Real Job: {'Yes' if job.get('is_real', False) else 'No'}")
                if job.get('apply_url'):
                    print(f"   Apply: {job['apply_url']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Service Error: {str(e)}")
        return False

def test_recommendations_with_jobs():
    """Test recommendations with real job integration"""
    print("\n🎯 Testing Recommendations with Real Jobs...")
    print("=" * 60)
    
    try:
        import requests
        
        # Test the recommendations with jobs endpoint
        url = "http://localhost:5000/api/recommendations-with-jobs"
        data = {
            "skills": "Python, Machine Learning, Data Analysis",
            "interests": "Data Science, AI, Research",
            "academic_background": "Computer Science, Bachelor, 3.8 GPA",
            "previous_internships": "Data Science Intern at TechCorp, 3 months",
            "location": "Chicago, IL"
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            recommendations = result.get('recommendations', [])
            
            print(f"✅ Got {len(recommendations)} recommendations with real jobs")
            
            for i, rec in enumerate(recommendations[:2], 1):
                print(f"\n{i}. {rec['title']} ({int(rec['similarity_score'] * 100)}% match)")
                real_jobs = rec.get('real_jobs', [])
                print(f"   Real Jobs Found: {len(real_jobs)}")
                
                for job in real_jobs[:2]:
                    print(f"   - {job['title']} at {job['company']}")
                    print(f"     Location: {job['location']}")
                    print(f"     Salary: {job['salary']}")
                    print(f"     Source: {job['source']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Recommendations Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Real Job Search Integration")
    print("=" * 60)
    
    # Test 1: Direct API call
    api_success = test_job_search_api()
    
    # Test 2: Job search service
    service_success = test_job_search_service()
    
    # Test 3: Recommendations with jobs (requires server running)
    print("\n⚠️  Note: For full integration test, make sure the Flask server is running:")
    print("   python app.py")
    print("   Then run: python test_job_search.py")
    
    if api_success and service_success:
        print("\n🎉 All tests passed! Your job search integration is working!")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
