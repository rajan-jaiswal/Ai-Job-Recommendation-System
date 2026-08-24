#!/usr/bin/env python3
"""
Demo script for Smart Career Recommendation System
This script demonstrates the recommendation engine functionality
"""

import requests
import json
import time

def test_recommendation_api():
    """Test the recommendation API with sample data"""
    
    # Sample student profiles for testing
    test_cases = [
        {
            "name": "Data Science Student",
            "skills": "Python, Machine Learning, Data Analysis, SQL, Statistics, R, TensorFlow",
            "interests": "Data Science, AI, Research, Analytics, Problem Solving",
            "academic_background": "Data Science, Master, 3.8 GPA",
            "previous_internships": "Data Science Intern at DataLab, 3 months"
        },
        {
            "name": "Web Developer Student",
            "skills": "JavaScript, React, HTML, CSS, Node.js, Express.js, MongoDB",
            "interests": "Web Development, Frontend, UI/UX, User Experience, Design",
            "academic_background": "Computer Science, Bachelor, 3.6 GPA",
            "previous_internships": "Frontend Developer Intern at WebStudio, 2 months"
        },
        {
            "name": "Mobile Developer Student",
            "skills": "Swift, Kotlin, React Native, Mobile Development, iOS, Android, Firebase",
            "interests": "Mobile Development, App Development, User Interface, Cross Platform",
            "academic_background": "Computer Science, Bachelor, 3.5 GPA",
            "previous_internships": "Mobile Developer Intern at AppCorp, 3 months"
        }
    ]
    
    base_url = "http://localhost:5000"
    
    print("🚀 Smart Career Recommendation System - Demo")
    print("=" * 50)
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print("✅ Server is running!")
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Please start the Flask app first:")
        print("   python app.py")
        return
    
    print("\n📊 Testing Recommendation Engine...")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"   Skills: {test_case['skills'][:50]}...")
        print(f"   Interests: {test_case['interests'][:50]}...")
        
        try:
            # Make API request
            response = requests.post(
                f"{base_url}/api/recommendations",
                json=test_case,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get('recommendations', [])
                
                print(f"   ✅ Got {len(recommendations)} recommendations:")
                
                for j, rec in enumerate(recommendations[:3], 1):
                    similarity = int(rec['similarity_score'] * 100)
                    print(f"      {j}. {rec['title']} ({similarity}% match)")
                    print(f"         Salary: {rec['salary_range']}")
                    print(f"         Level: {rec['experience_level']}")
                
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    print("\n🎯 Testing Admin APIs...")
    print("-" * 30)
    
    # Test careers API
    try:
        response = requests.get(f"{base_url}/api/careers", timeout=5)
        if response.status_code == 200:
            data = response.json()
            careers = data.get('careers', [])
            print(f"✅ Careers API: {len(careers)} career roles available")
        else:
            print(f"❌ Careers API failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Careers API request failed: {e}")
    
    # Test students API
    try:
        response = requests.get(f"{base_url}/api/students", timeout=5)
        if response.status_code == 200:
            data = response.json()
            students = data.get('students', [])
            print(f"✅ Students API: {len(students)} student profiles available")
        else:
            print(f"❌ Students API failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Students API request failed: {e}")
    
    print("\n📄 Testing Resume Upload API...")
    print("-" * 30)
    
    # Test resume parsing (using sample text)
    try:
        from resume_parser import ResumeParser
        
        # Read sample resume
        with open('sample_resume.txt', 'r', encoding='utf-8') as f:
            sample_text = f.read()
        
        parser = ResumeParser()
        parsed_data = parser._parse_text(sample_text)
        formatted_data = parser.format_for_recommendation(parsed_data)
        
        print("✅ Resume Parser: Successfully parsed sample resume")
        print(f"   Skills found: {len(formatted_data.get('skills', '').split(','))}")
        print(f"   Interests found: {len(formatted_data.get('interests', '').split(','))}")
        print(f"   Education: {formatted_data.get('academic_background', 'N/A')}")
        
    except FileNotFoundError:
        print("⚠️  Sample resume file not found, skipping resume parser test")
    except Exception as e:
        print(f"❌ Resume parser test failed: {e}")
    
    print("\n🎉 Demo completed!")
    print("\nTo use the web interface:")
    print("1. Open your browser")
    print("2. Go to http://localhost:5000")
    print("3. Upload a resume or fill out the form manually")
    print("4. Get personalized career recommendations!")
    print("\n📋 Resume Upload Features:")
    print("• Upload PDF or DOCX files (max 16MB)")
    print("• Automatic text extraction and parsing")
    print("• Auto-fill form with extracted information")
    print("• Get instant recommendations based on resume")

def test_recommendation_engine_directly():
    """Test the recommendation engine directly without Flask"""
    print("\n🔧 Testing Recommendation Engine Directly...")
    print("-" * 40)
    
    try:
        from app import CareerRecommendationEngine
        
        # Initialize engine
        engine = CareerRecommendationEngine()
        print("✅ Recommendation engine initialized")
        
        # Test with sample data
        test_skills = "Python, Machine Learning, Data Analysis, SQL"
        test_interests = "Data Science, AI, Research, Analytics"
        test_academic = "Computer Science, Master, 3.8 GPA"
        test_internships = "Data Science Intern at TechCorp, 3 months"
        
        recommendations = engine.get_recommendations(
            test_skills, test_interests, test_academic, test_internships
        )
        
        print(f"✅ Got {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            similarity = int(rec['similarity_score'] * 100)
            print(f"   {i}. {rec['title']} ({similarity}% match)")
        
    except ImportError as e:
        print(f"❌ Cannot import recommendation engine: {e}")
    except Exception as e:
        print(f"❌ Error testing engine: {e}")

if __name__ == "__main__":
    print("Smart Career Recommendation System - Demo Script")
    print("=" * 50)
    
    # Test recommendation engine directly first
    test_recommendation_engine_directly()
    
    # Test API endpoints
    test_recommendation_api()
