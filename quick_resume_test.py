#!/usr/bin/env python3
"""
Quick test for resume upload with real job search
"""

import requests
import time

def test_resume_upload():
    """Quick test of resume upload"""
    print("📄 Quick Resume Upload Test")
    print("=" * 30)
    
    # Create a simple test resume
    resume_content = """
    John Doe
    Software Engineer
    john.doe@email.com
    
    SKILLS
    Python, JavaScript, React, Node.js, SQL, AWS
    
    EXPERIENCE
    2 years software development experience
    
    EDUCATION
    Computer Science, Bachelor, 3.8 GPA
    """
    
    # Save to file
    with open('test_resume.txt', 'w') as f:
        f.write(resume_content)
    
    try:
        print("📤 Uploading resume...")
        start_time = time.time()
        
        with open('test_resume.txt', 'rb') as f:
            files = {'resume': ('test_resume.txt', f, 'text/plain')}
            response = requests.post(
                'http://localhost:5000/api/upload-resume',
                files=files,
                timeout=15
            )
        
        duration = time.time() - start_time
        print(f"⏱️  Time: {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Resume uploaded successfully!")
            print(f"📊 Recommendations: {len(data.get('recommendations', []))}")
            
            # Check for real jobs
            real_jobs = 0
            for rec in data.get('recommendations', []):
                for job in rec.get('real_jobs', []):
                    if job.get('is_real', False):
                        real_jobs += 1
            
            print(f"🎯 Real jobs found: {real_jobs}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        import os
        if os.path.exists('test_resume.txt'):
            os.remove('test_resume.txt')

if __name__ == "__main__":
    success = test_resume_upload()
    
    if success:
        print("\n🎉 Resume upload with real job search is working!")
    else:
        print("\n⚠️  Resume upload test failed")
