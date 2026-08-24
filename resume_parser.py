"""
Resume Parser Module for Smart Career Recommendation System
Extracts information from uploaded resumes (PDF, DOCX) and converts to structured data
"""

import os
import re
import PyPDF2
from docx import Document
from typing import Dict, List, Optional, Tuple
import logging

class ResumeParser:
    """Parse resumes and extract relevant information for job recommendations"""
    
    def __init__(self):
        self.skills_keywords = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'xml', 'json',
            
            # Frameworks and Libraries
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            'bootstrap', 'jquery', 'sass', 'less', 'webpack', 'babel',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite',
            'cassandra', 'dynamodb', 'neo4j',
            
            # Cloud and DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
            'terraform', 'ansible', 'chef', 'puppet', 'ci/cd', 'devops',
            
            # Data Science and AI
            'machine learning', 'deep learning', 'artificial intelligence', 'data science',
            'data analysis', 'statistics', 'nlp', 'computer vision', 'neural networks',
            'regression', 'classification', 'clustering', 'data visualization',
            
            # Mobile Development
            'ios', 'android', 'react native', 'flutter', 'xamarin', 'ionic',
            
            # Other Technical Skills
            'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum', 'jira', 'confluence',
            'linux', 'unix', 'windows', 'macos', 'bash', 'powershell', 'vim', 'emacs'
        ]
        
        self.education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'degree', 'diploma', 'certificate',
            'university', 'college', 'institute', 'school', 'gpa', 'cgpa', 'grade'
        ]
        
        self.experience_keywords = [
            'experience', 'intern', 'internship', 'work', 'job', 'position', 'role',
            'project', 'freelance', 'consultant', 'volunteer', 'part-time', 'full-time'
        ]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def parse_resume(self, file_path: str, file_type: str) -> Dict:
        """
        Parse resume file and extract structured information
        
        Args:
            file_path: Path to the resume file
            file_type: Type of file ('pdf' or 'docx')
            
        Returns:
            Dictionary containing extracted information
        """
        try:
            # Extract text from file
            text = self._extract_text(file_path, file_type)
            if not text:
                return {'error': 'Could not extract text from resume'}
            
            # Parse the extracted text
            parsed_data = self._parse_text(text)
            parsed_data['original_text'] = text[:500]  # Store first 500 chars for reference
            
            return parsed_data
            
        except Exception as e:
            self.logger.error(f"Error parsing resume: {str(e)}")
            return {'error': f'Error parsing resume: {str(e)}'}
    
    def _extract_text(self, file_path: str, file_type: str) -> str:
        """Extract text from PDF, DOCX, or TXT file"""
        try:
            if file_type.lower() == 'pdf':
                return self._extract_pdf_text(file_path)
            elif file_type.lower() == 'docx':
                return self._extract_docx_text(file_path)
            elif file_type.lower() == 'txt':
                return self._extract_txt_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            self.logger.error(f"Error extracting text: {str(e)}")
            return ""
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            self.logger.error(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            self.logger.error(f"Error reading DOCX: {str(e)}")
        return text
    
    def _extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT file"""
        text = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            self.logger.error(f"Error reading TXT: {str(e)}")
        return text
    
    def _parse_text(self, text: str) -> Dict:
        """Parse extracted text and extract relevant information"""
        text_lower = text.lower()
        
        # Extract skills
        skills = self._extract_skills(text_lower)
        
        # Extract education
        education = self._extract_education(text)
        
        # Extract experience
        experience = self._extract_experience(text)
        
        # Extract contact information
        contact = self._extract_contact_info(text)
        
        # Extract interests (from projects, activities, etc.)
        interests = self._extract_interests(text_lower)
        
        return {
            'skills': skills,
            'education': education,
            'experience': experience,
            'contact': contact,
            'interests': interests,
            'parsed_successfully': True
        }
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from resume text"""
        found_skills = []
        
        for skill in self.skills_keywords:
            if skill in text:
                found_skills.append(skill.title())
        
        # Remove duplicates and sort
        return sorted(list(set(found_skills)))
    
    def _extract_education(self, text: str) -> Dict:
        """Extract education information"""
        education_info = {
            'degree': '',
            'field': '',
            'institution': '',
            'gpa': '',
            'year': ''
        }
        
        # Look for degree patterns
        degree_patterns = [
            r'(bachelor|b\.?s\.?|b\.?a\.?|b\.?e\.?|b\.?tech)',
            r'(master|m\.?s\.?|m\.?a\.?|m\.?e\.?|m\.?tech|mba)',
            r'(phd|ph\.?d\.?|doctorate|doctoral)',
            r'(diploma|certificate)'
        ]
        
        for pattern in degree_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                education_info['degree'] = match.group(1).upper()
                break
        
        # Look for GPA
        gpa_pattern = r'gpa[:\s]*(\d+\.?\d*)'
        gpa_match = re.search(gpa_pattern, text, re.IGNORECASE)
        if gpa_match:
            education_info['gpa'] = gpa_match.group(1)
        
        # Look for field of study
        field_patterns = [
            r'(computer science|cs)',
            r'(information technology|it)',
            r'(software engineering|se)',
            r'(data science|ds)',
            r'(artificial intelligence|ai)',
            r'(machine learning|ml)',
            r'(business administration|mba)',
            r'(electrical engineering|ee)',
            r'(mechanical engineering|me)'
        ]
        
        for pattern in field_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                education_info['field'] = match.group(1).title()
                break
        
        return education_info
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience information"""
        experiences = []
        
        # Look for experience patterns
        exp_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:in|of)'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                years = int(match.group(1))
                experiences.append({
                    'years': years,
                    'type': 'professional'
                })
                break
        
        # Look for internship experience
        intern_patterns = [
            r'intern(?:ship)?[:\s]*(\d+)\s*(?:months?|mos?)',
            r'(\d+)\s*(?:months?|mos?)\s*(?:of\s*)?intern(?:ship)?'
        ]
        
        for pattern in intern_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                months = int(match.group(1))
                experiences.append({
                    'months': months,
                    'type': 'internship'
                })
                break
        
        return experiences
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        contact = {
            'email': '',
            'phone': '',
            'location': ''
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Extract phone
        phone_patterns = [
            r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'(\+?[0-9]{1,3}[-.\s]?)?([0-9]{10})'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact['phone'] = phone_match.group(0)
                break
        
        return contact
    
    def _extract_interests(self, text: str) -> List[str]:
        """Extract interests from resume text"""
        interests = []
        
        # Common interest keywords
        interest_keywords = [
            'web development', 'mobile development', 'data science', 'machine learning',
            'artificial intelligence', 'cybersecurity', 'cloud computing', 'devops',
            'ui/ux', 'user experience', 'frontend', 'backend', 'full stack',
            'blockchain', 'iot', 'game development', 'research', 'open source',
            'startup', 'entrepreneurship', 'leadership', 'teamwork', 'communication'
        ]
        
        for interest in interest_keywords:
            if interest in text:
                interests.append(interest.title())
        
        return interests
    
    def format_for_recommendation(self, parsed_data: Dict) -> Dict:
        """Format parsed resume data for recommendation engine"""
        if 'error' in parsed_data:
            return parsed_data
        
        # Combine skills into a string
        skills_str = ', '.join(parsed_data.get('skills', []))
        
        # Create interests string
        interests_str = ', '.join(parsed_data.get('interests', []))
        
        # Format education
        education = parsed_data.get('education', {})
        education_str = f"{education.get('field', '')} {education.get('degree', '')} {education.get('gpa', '')}".strip()
        
        # Format experience
        experience = parsed_data.get('experience', [])
        experience_str = ''
        for exp in experience:
            if exp['type'] == 'professional':
                experience_str += f"{exp['years']} years professional experience, "
            elif exp['type'] == 'internship':
                experience_str += f"{exp['months']} months internship experience, "
        
        experience_str = experience_str.rstrip(', ')
        
        return {
            'skills': skills_str,
            'interests': interests_str,
            'academic_background': education_str,
            'previous_internships': experience_str,
            'contact': parsed_data.get('contact', {}),
            'parsed_successfully': True
        }

# Example usage and testing
if __name__ == "__main__":
    parser = ResumeParser()
    
    # Test with sample text
    sample_text = """
    John Doe
    Software Engineer
    john.doe@email.com
    (555) 123-4567
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2020
    GPA: 3.8
    
    EXPERIENCE
    2 years of experience in web development
    6 months internship at TechCorp
    
    SKILLS
    Python, JavaScript, React, Node.js, SQL, AWS, Docker
    
    INTERESTS
    Web Development, Machine Learning, Open Source
    """
    
    result = parser._parse_text(sample_text)
    print("Parsed Resume Data:")
    print(json.dumps(result, indent=2))
