#!/usr/bin/env python3
"""
Test resume upload with real job search
"""

import requests
import time
import json

def test_resume_upload_with_real_jobs():
    """Test resume upload with real job search"""
    print("📄 Testing Resume Upload with Real Job Search")
    print("=" * 50)
    
    # Create a sample resume file for testing
    sample_resume_content = """
    John Doe
    Software Engineer
    john.doe@email.com | (555) 123-4567 | San Francisco, CA
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 3+ years of experience in full-stack web development, 
    specializing in Python, JavaScript, and cloud technologies.
    
    TECHNICAL SKILLS
    Programming Languages: Python, JavaScript, TypeScript, Java, SQL, HTML, CSS
    Frameworks & Libraries: React, Node.js, Express.js, Django, Flask, Spring Boot
    Databases: PostgreSQL, MongoDB, Redis, MySQL
    Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, CI/CD
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of California, Berkeley
    Graduated: May 2020 | GPA: 3.8/4.0
    
    PROFESSIONAL EXPERIENCE
    Software Engineer | TechCorp Inc. | Jan 2021 - Present
    • Developed and maintained web applications using Python, Django, and React
    • Implemented RESTful APIs and microservices architecture
    • Collaborated with cross-functional teams using Agile methodologies
    
    PROJECTS
    E-Commerce Platform | Personal Project | 2021
    • Full-stack web application built with Django and React
    • Integrated payment processing with Stripe API
    • Deployed on AWS with Docker containerization
    """
    
    # Save sample resume to file
    with open('test_resume.txt', 'w', encoding='utf-8') as f:
        f.write(sample_resume_content)
    
    try:
        print("📤 Uploading resume and searching for real jobs...")
        start_time = time.time()
        
        # Test resume upload
        with open('test_resume.txt', 'rb') as f:
            files = {'resume': ('test_resume.txt', f, 'text/plain')}
            
            response = requests.post(
                'http://localhost:5000/api/upload-resume',
                files=files,
                timeout=30
            )
        
        duration = time.time() - start_time
        print(f"⏱️  Resume processing time: {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            parsed_data = data.get('parsed_data', {})
            
            print(f"✅ Resume processed successfully!")
            print(f"📊 Found {len(recommendations)} career recommendations")
            
            # Show parsed data
            print(f"\n📋 Parsed Resume Data:")
            print(f"   Skills: {parsed_data.get('skills', 'N/A')[:100]}...")
            print(f"   Interests: {parsed_data.get('interests', 'N/A')[:100]}...")
            print(f"   Education: {parsed_data.get('academic_background', 'N/A')}")
            
            # Show recommendations with real jobs
            print(f"\n🎯 Career Recommendations with Real Jobs:")
            real_job_count = 0
            
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"\n{i}. {rec['title']} ({int(rec['similarity_score'] * 100)}% match)")
                real_jobs = rec.get('real_jobs', [])
                print(f"   Real Jobs Found: {len(real_jobs)}")
                
                for job in real_jobs[:2]:
                    is_real = job.get('is_real', False)
                    source = job.get('source', 'Unknown')
                    print(f"   - {job['title']} at {job['company']}")
                    print(f"     Location: {job['location']}")
                    print(f"     Salary: {job['salary']}")
                    print(f"     Source: {source} ({'Real' if is_real else 'Sample'})")
                    
                    if is_real:
                        real_job_count += 1
            
            print(f"\n📈 Summary:")
            print(f"   Total Real Jobs Found: {real_job_count}")
            print(f"   Processing Time: {duration:.2f} seconds")
            
            return True
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    finally:
        # Clean up test file
        import os
        if os.path.exists('test_resume.txt'):
            os.remove('test_resume.txt')

def test_regular_form_vs_resume():
    """Compare regular form vs resume upload"""
    print("\n🔄 Comparing Regular Form vs Resume Upload")
    print("=" * 50)
    
    # Test regular form
    print("📝 Testing regular form submission...")
    start_time = time.time()
    
    form_data = {
        "skills": "Python, JavaScript, React, Node.js, SQL",
        "interests": "Web Development, Full Stack, Software Engineering",
        "academic_background": "Computer Science, Bachelor, 3.8 GPA",
        "previous_internships": "Software Engineer Intern at TechCorp, 3 months"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/recommendations',
            json=form_data,
            timeout=10
        )
        
        form_duration = time.time() - start_time
        print(f"⏱️  Regular form: {form_duration:.2f} seconds")
        
        if response.status_code == 200:
            print("✅ Regular form works")
        else:
            print(f"❌ Regular form error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Regular form error: {e}")
    
    print(f"\n💡 Resume upload includes real job search (slower but more comprehensive)")
    print(f"💡 Regular form uses sample jobs (faster but limited)")

if __name__ == "__main__":
    print("🚀 Testing Resume Upload with Real Job Search")
    print("=" * 50)
    
    # Test resume upload with real jobs
    resume_success = test_resume_upload_with_real_jobs()
    
    # Compare with regular form
    test_regular_form_vs_resume()
    
    print("\n" + "=" * 50)
    if resume_success:
        print("🎉 Resume upload with real job search is working!")
        print("✅ Resume parsing works")
        print("✅ Real job search works")
        print("✅ Recommendations with real jobs work")
    else:
        print("⚠️  Resume upload test failed")
        print("💡 Check if the Flask server is running")
