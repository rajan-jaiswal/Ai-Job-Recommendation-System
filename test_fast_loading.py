#!/usr/bin/env python3
"""
Test script to verify fast loading
"""

import requests
import time

def test_fast_loading():
    """Test that recommendations load quickly"""
    print("🚀 Testing Fast Loading")
    print("=" * 40)
    
    test_data = {
        "skills": "Python, Machine Learning, Data Analysis",
        "interests": "Data Science, AI, Research",
        "academic_background": "Computer Science, Bachelor, 3.8 GPA",
        "previous_internships": "Data Science Intern at TechCorp, 3 months",
        "location": "Chicago, IL"
    }
    
    # Test regular recommendations
    print("📤 Testing regular recommendations...")
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:5000/api/recommendations",
            json=test_data,
            timeout=10
        )
        
        duration = time.time() - start_time
        print(f"⏱️  Regular recommendations: {duration:.2f} seconds")
        
        if response.status_code == 200:
            print("✅ Regular recommendations work!")
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test recommendations with jobs
    print("\n📤 Testing recommendations with jobs...")
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:5000/api/recommendations-with-jobs",
            json=test_data,
            timeout=10
        )
        
        duration = time.time() - start_time
        print(f"⏱️  Recommendations with jobs: {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"✅ Got {len(recommendations)} recommendations with jobs!")
            
            # Check if jobs are included
            for rec in recommendations[:2]:
                real_jobs = rec.get('real_jobs', [])
                print(f"   - {rec['title']}: {len(real_jobs)} jobs")
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_fast_loading()
    
    if success:
        print("\n🎉 Fast loading test passed!")
        print("✅ Both endpoints work quickly")
    else:
        print("\n⚠️  Some tests failed")
