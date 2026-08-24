#!/usr/bin/env python3
"""
Test frontend loading speed
"""

import requests
import time
import json

def test_frontend_speed():
    """Test that the frontend loads quickly"""
    print("🚀 Testing Frontend Loading Speed")
    print("=" * 40)
    
    # Test data
    test_data = {
        "skills": "Python, Machine Learning, Data Analysis",
        "interests": "Data Science, AI, Research",
        "academic_background": "Computer Science, Bachelor, 3.8 GPA",
        "previous_internships": "Data Science Intern at TechCorp, 3 months",
        "location": "Chicago, IL"
    }
    
    print("📤 Testing regular recommendations (fastest)...")
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:5000/api/recommendations",
            json=test_data,
            timeout=5
        )
        
        duration = time.time() - start_time
        print(f"⏱️  Response time: {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"✅ Success! Got {len(recommendations)} recommendations")
            
            # Show first recommendation
            if recommendations:
                rec = recommendations[0]
                print(f"   First recommendation: {rec['title']} ({int(rec['similarity_score'] * 100)}% match)")
                print(f"   Description: {rec['description'][:100]}...")
            
            return duration < 3.0  # Should be under 3 seconds
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_multiple_requests():
    """Test multiple requests to ensure consistency"""
    print("\n🔄 Testing Multiple Requests...")
    
    test_data = {
        "skills": "JavaScript, React, Node.js",
        "interests": "Web Development, Frontend",
        "academic_background": "Computer Science, Bachelor, 3.5 GPA",
        "previous_internships": "Web Developer Intern at Startup, 2 months"
    }
    
    times = []
    for i in range(3):
        start_time = time.time()
        try:
            response = requests.post(
                "http://localhost:5000/api/recommendations",
                json=test_data,
                timeout=5
            )
            duration = time.time() - start_time
            times.append(duration)
            print(f"   Request {i+1}: {duration:.2f} seconds")
        except Exception as e:
            print(f"   Request {i+1}: Error - {e}")
            return False
    
    avg_time = sum(times) / len(times)
    print(f"   Average time: {avg_time:.2f} seconds")
    
    return avg_time < 3.0

if __name__ == "__main__":
    print("🚀 Frontend Speed Test")
    print("=" * 40)
    
    # Test 1: Single request
    single_success = test_frontend_speed()
    
    # Test 2: Multiple requests
    multiple_success = test_multiple_requests()
    
    print("\n" + "=" * 40)
    if single_success and multiple_success:
        print("🎉 Frontend is FAST!")
        print("✅ Single request: Under 3 seconds")
        print("✅ Multiple requests: Consistent performance")
        print("\n💡 The 'Analyzing your profile' should now complete quickly!")
    else:
        print("⚠️  Frontend might be slow")
        print("💡 Try refreshing the browser page")
