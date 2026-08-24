#!/usr/bin/env python3
"""
Test script to verify the loading issue is fixed
"""

import requests
import time
import json

def test_recommendations_with_timeout():
    """Test recommendations with real jobs to ensure no infinite loading"""
    print("🔍 Testing Recommendations with Real Jobs (Timeout Test)")
    print("=" * 60)
    
    # Test data
    test_data = {
        "skills": "Python, Machine Learning, Data Analysis",
        "interests": "Data Science, AI, Research",
        "academic_background": "Computer Science, Bachelor, 3.8 GPA",
        "previous_internships": "Data Science Intern at TechCorp, 3 months",
        "location": "Chicago, IL"
    }
    
    try:
        print("📤 Sending request to recommendations-with-jobs endpoint...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:5000/api/recommendations-with-jobs",
            json=test_data,
            timeout=30  # 30 second timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Request completed in {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            
            print(f"✅ Success! Got {len(recommendations)} recommendations")
            
            for i, rec in enumerate(recommendations, 1):
                print(f"\n{i}. {rec['title']} ({int(rec['similarity_score'] * 100)}% match)")
                real_jobs = rec.get('real_jobs', [])
                print(f"   Real Jobs: {len(real_jobs)}")
                
                for job in real_jobs[:2]:
                    print(f"   - {job['title']} at {job['company']}")
                    print(f"     Source: {job['source']}")
                    print(f"     Real: {'Yes' if job.get('is_real', False) else 'No'}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_regular_recommendations():
    """Test regular recommendations (without real jobs)"""
    print("\n🔍 Testing Regular Recommendations (No Real Jobs)")
    print("=" * 60)
    
    test_data = {
        "skills": "Python, Machine Learning, Data Analysis",
        "interests": "Data Science, AI, Research",
        "academic_background": "Computer Science, Bachelor, 3.8 GPA",
        "previous_internships": "Data Science Intern at TechCorp, 3 months"
    }
    
    try:
        print("📤 Sending request to regular recommendations endpoint...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:5000/api/recommendations",
            json=test_data,
            timeout=10
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️  Request completed in {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"✅ Success! Got {len(recommendations)} recommendations")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Loading Fix")
    print("=" * 60)
    
    # Test 1: Regular recommendations (should be fast)
    regular_success = test_regular_recommendations()
    
    # Test 2: Recommendations with real jobs (should complete within 30 seconds)
    jobs_success = test_recommendations_with_timeout()
    
    print("\n" + "=" * 60)
    if regular_success and jobs_success:
        print("🎉 All tests passed! Loading issue is fixed!")
        print("✅ Regular recommendations work quickly")
        print("✅ Real job recommendations complete within timeout")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
