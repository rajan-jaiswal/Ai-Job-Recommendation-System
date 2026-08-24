from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import uuid
from werkzeug.utils import secure_filename
from resume_parser import ResumeParser
from job_search_service import JobSearchService

app = Flask(__name__)
CORS(app)

# Configuration for file uploads (disabled for Vercel - ephemeral storage)
# For production, use cloud storage like AWS S3, Google Cloud Storage, or Azure Blob Storage
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Only create upload directory locally (for development)
# On Vercel, this directory will be ephemeral and won't persist
if os.environ.get('FLASK_ENV') != 'production':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS or \
           filename.endswith('.txt')  # Allow .txt for testing

class CareerRecommendationEngine:
    def __init__(self):
        self.students_df = None
        self.careers_df = None
        self.vectorizer = TfidfVectorizer()
        self.career_vectors = None
        self.load_data()
        self.prepare_vectors()
    
    def load_data(self):
        """Load sample datasets for students and career roles"""
        # Sample students data
        students_data = {
            'student_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Emma Brown', 
                    'Frank Miller', 'Grace Lee', 'Henry Taylor', 'Ivy Chen', 'Jack Anderson',
                    'Kate Williams', 'Liam Johnson', 'Maya Patel', 'Noah Singh', 'Olivia Garcia',
                    'Paul Martinez', 'Quinn Thompson', 'Rachel Kim', 'Sam Rodriguez', 'Tina Wang'],
            'skills': [
                'Python, Machine Learning, Data Analysis, SQL, Statistics',
                'JavaScript, React, Node.js, HTML, CSS, Web Development',
                'Java, Spring Boot, Microservices, Database Design, REST APIs',
                'Python, Data Science, Machine Learning, TensorFlow, Jupyter',
                'C++, Algorithms, Data Structures, System Design, Problem Solving',
                'Python, Flask, Django, PostgreSQL, API Development',
                'R, Statistical Analysis, Data Visualization, Research, Statistics',
                'JavaScript, Vue.js, Frontend Development, UI/UX, Responsive Design',
                'Python, Machine Learning, Deep Learning, Computer Vision, OpenCV',
                'Java, Android Development, Mobile Apps, Kotlin, Firebase',
                'Python, Data Engineering, ETL, Apache Spark, Big Data',
                'JavaScript, Full Stack Development, MongoDB, Express.js, React',
                'C#, .NET, ASP.NET, SQL Server, Enterprise Applications',
                'Python, AI, Natural Language Processing, BERT, Transformers',
                'Swift, iOS Development, Mobile Apps, Xcode, Core Data',
                'Python, DevOps, Docker, Kubernetes, AWS, CI/CD',
                'JavaScript, React Native, Mobile Development, Redux, TypeScript',
                'Python, Bioinformatics, Data Analysis, R, Scientific Computing',
                'Java, Spring Security, OAuth, JWT, Microservices Architecture',
                'Python, Blockchain, Smart Contracts, Web3, Solidity'
            ],
            'interests': [
                'Data Science, AI, Research, Analytics, Problem Solving',
                'Web Development, UI/UX, Frontend, User Experience, Design',
                'Backend Development, System Architecture, Database Design, APIs',
                'Machine Learning, Data Analysis, Research, Statistics, AI',
                'Software Engineering, Algorithms, System Design, Optimization',
                'Web Development, Backend, APIs, Database, Full Stack',
                'Research, Statistics, Data Analysis, Academic, Scientific Computing',
                'Frontend Development, UI/UX, Design, User Experience, Web',
                'Computer Vision, AI, Machine Learning, Deep Learning, Research',
                'Mobile Development, Android, App Development, User Interface',
                'Big Data, Data Engineering, ETL, Cloud Computing, Analytics',
                'Full Stack Development, Web Applications, Database, APIs',
                'Enterprise Software, Business Applications, Database, Security',
                'Natural Language Processing, AI, Machine Learning, Research',
                'Mobile Development, iOS, App Development, User Experience',
                'Cloud Computing, DevOps, Infrastructure, Automation, Scalability',
                'Mobile Development, Cross Platform, React Native, JavaScript',
                'Bioinformatics, Scientific Computing, Research, Data Analysis',
                'Enterprise Development, Security, Microservices, Architecture',
                'Blockchain, Cryptocurrency, Web3, Smart Contracts, DeFi'
            ],
            'academic_background': [
                'Computer Science, Bachelor, 3.8 GPA',
                'Web Development, Bootcamp, Certificate',
                'Computer Science, Master, 3.9 GPA',
                'Data Science, Master, 3.7 GPA',
                'Computer Science, Bachelor, 3.6 GPA',
                'Software Engineering, Bachelor, 3.5 GPA',
                'Statistics, Master, 3.8 GPA',
                'Computer Science, Bachelor, 3.4 GPA',
                'Computer Science, PhD, 3.9 GPA',
                'Computer Science, Bachelor, 3.3 GPA',
                'Data Engineering, Master, 3.6 GPA',
                'Computer Science, Bachelor, 3.7 GPA',
                'Information Technology, Bachelor, 3.5 GPA',
                'Computer Science, PhD, 3.8 GPA',
                'Computer Science, Bachelor, 3.6 GPA',
                'Computer Science, Master, 3.7 GPA',
                'Computer Science, Bachelor, 3.4 GPA',
                'Bioinformatics, Master, 3.8 GPA',
                'Computer Science, Master, 3.6 GPA',
                'Computer Science, Bachelor, 3.5 GPA'
            ],
            'previous_internships': [
                'Data Analyst Intern at TechCorp, 3 months',
                'Frontend Developer Intern at WebStudio, 2 months',
                'Backend Developer Intern at EnterpriseSoft, 4 months',
                'Data Science Intern at DataLab, 3 months',
                'Software Engineer Intern at TechGiant, 4 months',
                'Full Stack Developer Intern at StartupXYZ, 3 months',
                'Research Assistant at University Lab, 6 months',
                'UI/UX Intern at DesignAgency, 2 months',
                'ML Engineer Intern at AI Company, 4 months',
                'Mobile Developer Intern at AppCorp, 3 months',
                'Data Engineer Intern at BigData Inc, 4 months',
                'Web Developer Intern at Digital Agency, 3 months',
                'Software Developer Intern at Enterprise Corp, 4 months',
                'AI Research Intern at Research Lab, 6 months',
                'iOS Developer Intern at Mobile Studio, 3 months',
                'DevOps Intern at CloudTech, 4 months',
                'React Native Intern at Mobile Startup, 3 months',
                'Bioinformatics Intern at Research Institute, 4 months',
                'Java Developer Intern at Enterprise Solutions, 4 months',
                'Blockchain Developer Intern at Crypto Startup, 3 months'
            ]
        }
        
        # Sample career roles data
        careers_data = {
            'career_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            'title': [
                'Data Scientist', 'Software Engineer', 'Frontend Developer', 'Backend Developer',
                'Full Stack Developer', 'Machine Learning Engineer', 'Data Analyst', 'DevOps Engineer',
                'Mobile App Developer', 'UI/UX Designer', 'Product Manager', 'Cloud Architect',
                'Cybersecurity Analyst', 'AI Research Scientist', 'Blockchain Developer'
            ],
            'required_skills': [
                'Python, Machine Learning, Statistics, Data Analysis, SQL, R, TensorFlow, Scikit-learn',
                'Java, Python, C++, Algorithms, Data Structures, System Design, Problem Solving',
                'JavaScript, React, HTML, CSS, Vue.js, Angular, Responsive Design, UI/UX',
                'Java, Python, Node.js, Database Design, REST APIs, Microservices, Spring Boot',
                'JavaScript, Python, React, Node.js, Database, Full Stack, APIs, Git',
                'Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, Computer Vision, NLP',
                'Python, R, SQL, Statistics, Data Visualization, Excel, Tableau, Power BI',
                'Docker, Kubernetes, AWS, CI/CD, Python, Linux, Infrastructure, Automation',
                'Swift, Kotlin, React Native, Mobile Development, iOS, Android, Firebase',
                'Figma, Adobe XD, Sketch, UI/UX Design, Prototyping, User Research, Wireframing',
                'Product Strategy, Analytics, User Research, Agile, Leadership, Communication',
                'AWS, Azure, GCP, Cloud Architecture, Docker, Kubernetes, Infrastructure, Security',
                'Cybersecurity, Network Security, Penetration Testing, Risk Assessment, Compliance',
                'Python, Machine Learning, Deep Learning, Research, PhD, Publications, AI',
                'Solidity, Web3, Blockchain, Smart Contracts, Ethereum, Cryptocurrency, DeFi'
            ],
            'description': [
                'Analyze complex data to help organizations make data-driven decisions using machine learning and statistical methods.',
                'Design, develop, and maintain software applications and systems using various programming languages and frameworks.',
                'Create user-facing web applications and interfaces using modern frontend technologies and frameworks.',
                'Build server-side applications, APIs, and database systems that power web and mobile applications.',
                'Develop both frontend and backend components of web applications, handling the complete development cycle.',
                'Design and implement machine learning models and AI systems to solve complex business problems.',
                'Collect, process, and analyze data to provide insights and support business decision-making processes.',
                'Manage and automate software deployment, infrastructure, and operations using cloud technologies.',
                'Develop mobile applications for iOS and Android platforms using native or cross-platform technologies.',
                'Design user interfaces and experiences for digital products, focusing on usability and aesthetics.',
                'Lead product development from conception to launch, working with cross-functional teams.',
                'Design and implement cloud infrastructure solutions for scalable and secure applications.',
                'Protect organizations from cyber threats by implementing security measures and monitoring systems.',
                'Conduct research in artificial intelligence and machine learning to advance the field.',
                'Develop decentralized applications and smart contracts using blockchain technologies.'
            ],
            'salary_range': [
                '$80,000 - $150,000', '$70,000 - $130,000', '$60,000 - $120,000', '$70,000 - $130,000',
                '$75,000 - $140,000', '$90,000 - $160,000', '$55,000 - $100,000', '$80,000 - $150,000',
                '$70,000 - $130,000', '$60,000 - $110,000', '$80,000 - $150,000', '$90,000 - $160,000',
                '$70,000 - $130,000', '$100,000 - $180,000', '$85,000 - $150,000'
            ],
            'experience_level': [
                'Mid-Level', 'Entry to Senior', 'Entry to Mid-Level', 'Mid-Level', 'Mid-Level',
                'Mid to Senior', 'Entry to Mid-Level', 'Mid-Level', 'Entry to Mid-Level', 'Entry to Mid-Level',
                'Mid to Senior', 'Senior', 'Mid-Level', 'Senior', 'Mid-Level'
            ]
        }
        
        self.students_df = pd.DataFrame(students_data)
        self.careers_df = pd.DataFrame(careers_data)
    
    def prepare_vectors(self):
        """Prepare TF-IDF vectors for career roles"""
        # Combine skills and interests for each career role
        career_texts = []
        for _, career in self.careers_df.iterrows():
            text = f"{career['required_skills']} {career['description']}"
            career_texts.append(text)
        
        self.career_vectors = self.vectorizer.fit_transform(career_texts)
    
    def get_recommendations(self, skills, interests, academic_background, previous_internships):
        """Get career recommendations based on student profile"""
        # Create student profile text
        student_text = f"{skills} {interests} {academic_background} {previous_internships}"
        
        # Vectorize student profile
        student_vector = self.vectorizer.transform([student_text])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(student_vector, self.career_vectors)[0]
        
        # Get top 5 recommendations
        top_indices = np.argsort(similarities)[::-1][:5]
        
        recommendations = []
        for idx in top_indices:
            career = self.careers_df.iloc[idx]
            recommendation = {
                'career_id': int(career['career_id']),
                'title': career['title'],
                'description': career['description'],
                'required_skills': career['required_skills'],
                'salary_range': career['salary_range'],
                'experience_level': career['experience_level'],
                'similarity_score': float(similarities[idx]),
                'match_reasons': self._get_match_reasons(skills, interests, career['required_skills'])
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_match_reasons(self, student_skills, student_interests, career_skills):
        """Generate reasons why this career matches the student"""
        student_skills_lower = [skill.strip().lower() for skill in student_skills.split(',')]
        career_skills_lower = [skill.strip().lower() for skill in career_skills.split(',')]
        
        matched_skills = []
        for skill in student_skills_lower:
            for career_skill in career_skills_lower:
                if skill in career_skill or career_skill in skill:
                    matched_skills.append(skill.title())
                    break
        
        reasons = []
        if matched_skills:
            reasons.append(f"Your skills in {', '.join(matched_skills[:3])} align well with this role")
        
        # Check for interest matches
        student_interests_lower = [interest.strip().lower() for interest in student_interests.split(',')]
        career_text_lower = career_skills.lower()
        
        matched_interests = []
        for interest in student_interests_lower:
            if any(keyword in career_text_lower for keyword in [interest, interest.replace(' ', '')]):
                matched_interests.append(interest.title())
        
        if matched_interests:
            reasons.append(f"Your interests in {', '.join(matched_interests[:2])} match this career path")
        
        if not reasons:
            reasons.append("This role offers growth opportunities in your field")
        
        return reasons

# Initialize recommendation engine and job search service
recommendation_engine = CareerRecommendationEngine()
job_search_service = JobSearchService()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """API endpoint to get career recommendations"""
    try:
        data = request.get_json()
        
        skills = data.get('skills', '')
        interests = data.get('interests', '')
        academic_background = data.get('academic_background', '')
        previous_internships = data.get('previous_internships', '')
        
        if not all([skills, interests, academic_background]):
            return jsonify({'error': 'Skills, interests, and academic background are required'}), 400
        
        recommendations = recommendation_engine.get_recommendations(
            skills, interests, academic_background, previous_internships
        )
        
        return jsonify({
            'recommendations': recommendations,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/careers', methods=['GET'])
def get_all_careers():
    """API endpoint to get all available career roles"""
    try:
        careers = recommendation_engine.careers_df.to_dict('records')
        return jsonify({'careers': careers, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students', methods=['GET'])
def get_all_students():
    """API endpoint to get all students (for admin purposes)"""
    try:
        students = recommendation_engine.students_df.to_dict('records')
        return jsonify({'students': students, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """API endpoint to upload and parse resume"""
    try:
        # Check if file is present in request
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed.'}), 400
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Parse resume
        parser = ResumeParser()
        parsed_data = parser.parse_resume(file_path, file_extension)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass  # File cleanup is not critical
        
        if 'error' in parsed_data:
            return jsonify({'error': parsed_data['error']}), 400
        
        # Format data for recommendation engine
        formatted_data = parser.format_for_recommendation(parsed_data)
        
        if 'error' in formatted_data:
            return jsonify({'error': formatted_data['error']}), 400
        
        # Get recommendations based on parsed resume
        recommendations = recommendation_engine.get_recommendations(
            formatted_data['skills'],
            formatted_data['interests'],
            formatted_data['academic_background'],
            formatted_data['previous_internships']
        )
        
        # Add real job search for resume uploads
        recommendations_with_jobs = []
        for i, rec in enumerate(recommendations):
            job_title = rec['title']
            job_skills = rec['required_skills'].split(',')[:5]
            
            try:
                # Search for real jobs based on resume content
                jobs = job_search_service.search_jobs(
                    job_title=job_title,
                    location='',  # No specific location for resume uploads
                    skills=job_skills,
                    job_type='fulltime',
                    num_pages=1
                )
                rec['real_jobs'] = jobs[:3]
            except Exception as e:
                app.logger.error(f"Job search failed for {job_title}: {str(e)}")
                # Use sample jobs as fallback
                rec['real_jobs'] = job_search_service._filter_fallback_jobs(job_title, job_skills)[:3]
            
            recommendations_with_jobs.append(rec)
            
            # Limit to first 3 recommendations for speed
            if i >= 2:
                break
        
        return jsonify({
            'parsed_data': formatted_data,
            'recommendations': recommendations_with_jobs,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500

@app.route('/api/parse-resume-only', methods=['POST'])
def parse_resume_only():
    """API endpoint to parse resume without getting recommendations"""
    try:
        # Check if file is present in request
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed.'}), 400
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Parse resume
        parser = ResumeParser()
        parsed_data = parser.parse_resume(file_path, file_extension)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass  # File cleanup is not critical
        
        if 'error' in parsed_data:
            return jsonify({'error': parsed_data['error']}), 400
        
        # Format data for recommendation engine
        formatted_data = parser.format_for_recommendation(parsed_data)
        
        return jsonify({
            'parsed_data': formatted_data,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500

@app.route('/api/search-jobs', methods=['POST'])
def search_jobs():
    """API endpoint to search for real job postings"""
    try:
        data = request.get_json()
        
        job_title = data.get('job_title', '')
        location = data.get('location', '')
        skills = data.get('skills', [])
        job_type = data.get('job_type', 'fulltime')
        num_pages = data.get('num_pages', 1)
        
        if not job_title:
            return jsonify({'error': 'Job title is required'}), 400
        
        # Search for jobs
        jobs = job_search_service.search_jobs(
            job_title=job_title,
            location=location,
            skills=skills,
            job_type=job_type,
            num_pages=num_pages
        )
        
        return jsonify({
            'jobs': jobs,
            'total_found': len(jobs),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error searching jobs: {str(e)}'}), 500

@app.route('/api/recommendations-with-jobs', methods=['POST'])
def get_recommendations_with_jobs():
    """API endpoint to get career recommendations with real job postings"""
    try:
        data = request.get_json()
        
        skills = data.get('skills', '')
        interests = data.get('interests', '')
        academic_background = data.get('academic_background', '')
        previous_internships = data.get('previous_internships', '')
        location = data.get('location', '')
        
        if not all([skills, interests, academic_background]):
            return jsonify({'error': 'Skills, interests, and academic background are required'}), 400
        
        # Get career recommendations
        recommendations = recommendation_engine.get_recommendations(
            skills, interests, academic_background, previous_internships
        )
        
        # Check if any APIs are enabled
        from api_config import is_any_api_enabled
        apis_enabled = is_any_api_enabled()
        
        if not apis_enabled:
            # Use sample jobs for fast response
            recommendations_with_jobs = []
            for rec in recommendations:
                # Get sample jobs for this career
                sample_jobs = job_search_service._filter_fallback_jobs(rec['title'], rec['required_skills'].split(','))
                rec['real_jobs'] = sample_jobs[:3]
                recommendations_with_jobs.append(rec)
        else:
            # Use real job search (with timeout protection)
            recommendations_with_jobs = []
            for i, rec in enumerate(recommendations):
                job_title = rec['title']
                job_skills = rec['required_skills'].split(',')[:5]
                
                try:
                    jobs = job_search_service.search_jobs(
                        job_title=job_title,
                        location=location,
                        skills=job_skills,
                        job_type='fulltime',
                        num_pages=1
                    )
                    rec['real_jobs'] = jobs[:3]
                except Exception as e:
                    app.logger.error(f"Job search failed for {job_title}: {str(e)}")
                    rec['real_jobs'] = []
                
                recommendations_with_jobs.append(rec)
                
                # Limit to first 3 recommendations for speed
                if i >= 2:
                    break
        
        return jsonify({
            'recommendations': recommendations_with_jobs,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/job-details/<job_id>', methods=['GET'])
def get_job_details(job_id):
    """API endpoint to get detailed information about a specific job"""
    try:
        job_details = job_search_service.get_job_details(job_id)
        
        if job_details:
            return jsonify({
                'job_details': job_details,
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Job not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Error getting job details: {str(e)}'}), 500

@app.route('/api/set-api-key', methods=['POST'])
def set_api_key():
    """API endpoint to set API keys for job search services"""
    try:
        data = request.get_json()
        
        api_name = data.get('api_name')
        api_key = data.get('api_key')
        
        if not api_name or not api_key:
            return jsonify({'error': 'API name and key are required'}), 400
        
        job_search_service.set_api_key(api_name, api_key)
        
        return jsonify({
            'message': f'API key set for {api_name}',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error setting API key: {str(e)}'}), 500

@app.route('/api/available-apis', methods=['GET'])
def get_available_apis():
    """API endpoint to get list of available job search APIs"""
    try:
        apis = job_search_service.get_available_apis()
        return jsonify({
            'apis': apis,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': f'Error getting APIs: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
