"""
Job Search Service for Smart Career Recommendation System
Integrates with multiple job search APIs to fetch real job postings
"""

import requests
import json
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from api_config import get_api_config, is_any_api_enabled

class JobSearchService:
    """Service to search for real job postings from various APIs"""
    
    def __init__(self):
        self.setup_logging()
        self.api_config = get_api_config()
        self.job_apis = self._initialize_apis()
        
        # Fallback job data when APIs are not available
        self.fallback_jobs = self._load_fallback_jobs()
    
    def _initialize_apis(self):
        """Initialize job search APIs based on configuration"""
        apis = {}
        
        # JSearch API
        if self.api_config['jsearch']['enabled']:
            apis['jsearch'] = {
                'base_url': 'https://jsearch.p.rapidapi.com',
                'headers': {
                    'X-RapidAPI-Key': self.api_config['jsearch']['api_key'],
                    'X-RapidAPI-Host': 'jsearch.p.rapidapi.com'
                },
                'enabled': True
            }
        
        # Indeed API
        if self.api_config['indeed']['enabled']:
            apis['indeed'] = {
                'base_url': 'https://indeed-indeed.p.rapidapi.com',
                'headers': {
                    'X-RapidAPI-Key': self.api_config['indeed']['api_key'],
                    'X-RapidAPI-Host': 'indeed-indeed.p.rapidapi.com'
                },
                'enabled': True
            }
        
        return apis
    
    def setup_logging(self):
        """Setup logging for the job search service"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _load_fallback_jobs(self) -> List[Dict]:
        """Load fallback job data when APIs are not available"""
        return [
            {
                'job_id': 'fallback_1',
                'title': 'Software Engineer',
                'company': 'TechCorp Inc.',
                'location': 'San Francisco, CA',
                'salary': '$80,000 - $120,000',
                'description': 'We are looking for a skilled Software Engineer to join our team. You will be responsible for developing and maintaining web applications using modern technologies.',
                'requirements': 'Python, JavaScript, React, Node.js, SQL, AWS',
                'job_type': 'Full-time',
                'experience_level': 'Mid-Level',
                'posted_date': '2024-01-15',
                'apply_url': 'https://techcorp.com/careers/software-engineer',
                'source': 'Company Website',
                'is_real': False
            },
            {
                'job_id': 'fallback_2',
                'title': 'Data Scientist',
                'company': 'DataLab Solutions',
                'location': 'New York, NY',
                'salary': '$90,000 - $140,000',
                'description': 'Join our data science team to build machine learning models and analyze large datasets. Work with cutting-edge AI technologies.',
                'requirements': 'Python, Machine Learning, SQL, Statistics, TensorFlow, Pandas',
                'job_type': 'Full-time',
                'experience_level': 'Mid-Level',
                'posted_date': '2024-01-14',
                'apply_url': 'https://datalab.com/careers/data-scientist',
                'source': 'Company Website',
                'is_real': False
            },
            {
                'job_id': 'fallback_3',
                'title': 'Frontend Developer',
                'company': 'WebStudio',
                'location': 'Austin, TX',
                'salary': '$70,000 - $110,000',
                'description': 'Create beautiful and responsive user interfaces for our web applications. Work with modern frontend frameworks and tools.',
                'requirements': 'JavaScript, React, HTML, CSS, TypeScript, Bootstrap',
                'job_type': 'Full-time',
                'experience_level': 'Entry to Mid-Level',
                'posted_date': '2024-01-13',
                'apply_url': 'https://webstudio.com/careers/frontend-developer',
                'source': 'Company Website',
                'is_real': False
            },
            {
                'job_id': 'fallback_4',
                'title': 'DevOps Engineer',
                'company': 'CloudTech',
                'location': 'Seattle, WA',
                'salary': '$85,000 - $130,000',
                'description': 'Manage cloud infrastructure and deployment pipelines. Work with containerization and automation tools.',
                'requirements': 'AWS, Docker, Kubernetes, Python, Linux, CI/CD',
                'job_type': 'Full-time',
                'experience_level': 'Mid-Level',
                'posted_date': '2024-01-12',
                'apply_url': 'https://cloudtech.com/careers/devops-engineer',
                'source': 'Company Website',
                'is_real': False
            },
            {
                'job_id': 'fallback_5',
                'title': 'Mobile App Developer',
                'company': 'AppCorp',
                'location': 'Remote',
                'salary': '$75,000 - $115,000',
                'description': 'Develop mobile applications for iOS and Android platforms. Work with cross-platform frameworks.',
                'requirements': 'React Native, Swift, Kotlin, JavaScript, Firebase',
                'job_type': 'Full-time',
                'experience_level': 'Mid-Level',
                'posted_date': '2024-01-11',
                'apply_url': 'https://appcorp.com/careers/mobile-developer',
                'source': 'Company Website',
                'is_real': False
            }
        ]
    
    def search_jobs(self, job_title: str, location: str = '', skills: List[str] = None, 
                   job_type: str = 'fulltime', num_pages: int = 1) -> List[Dict]:
        """
        Search for jobs using available APIs
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            skills: List of skills to filter by
            job_type: Type of job (fulltime, parttime, contract)
            num_pages: Number of pages to fetch
            
        Returns:
            List of job postings
        """
        jobs = []
        max_retries = 2  # Limit retries to prevent infinite loading
        
        # Try to get jobs from APIs first (with timeout)
        for api_name, api_config in self.job_apis.items():
            if api_config['enabled'] and len(jobs) < 10:  # Stop if we have enough jobs
                try:
                    self.logger.info(f"Searching with {api_name}...")
                    api_jobs = self._search_with_api(api_name, job_title, location, skills, job_type, min(num_pages, 1))
                    jobs.extend(api_jobs)
                    self.logger.info(f"Found {len(api_jobs)} jobs from {api_name}")
                    
                    # If we got jobs, break to avoid too many API calls
                    if api_jobs:
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error searching with {api_name}: {str(e)}")
                    # Continue to next API or fallback
        
        # If no jobs found from APIs, use fallback data
        if not jobs:
            self.logger.info("No jobs found from APIs, using fallback data")
            jobs = self._filter_fallback_jobs(job_title, skills)
        
        # Remove duplicates and sort by relevance
        jobs = self._deduplicate_jobs(jobs)
        jobs = self._sort_jobs_by_relevance(jobs, job_title, skills)
        
        return jobs[:20]  # Return top 20 jobs
    
    def _search_with_api(self, api_name: str, job_title: str, location: str, 
                        skills: List[str], job_type: str, num_pages: int) -> List[Dict]:
        """Search jobs using specific API"""
        if api_name == 'jsearch':
            return self._search_jsearch(job_title, location, skills, job_type, num_pages)
        elif api_name == 'indeed':
            return self._search_indeed(job_title, location, skills, job_type, num_pages)
        else:
            return []
    
    def _search_jsearch(self, job_title: str, location: str, skills: List[str], 
                       job_type: str, num_pages: int) -> List[Dict]:
        """Search jobs using JSearch API"""
        jobs = []
        
        for page in range(num_pages):
            try:
                url = f"{self.job_apis['jsearch']['base_url']}/search"
                params = {
                    'query': job_title,
                    'page': page + 1,
                    'num_pages': 1,
                    'date_posted': 'month',
                    'country': 'us'
                }
                
                if location:
                    params['location'] = location
                
                if skills:
                    # Add skills to the query instead of separate parameter
                    skills_query = f"{job_title} {' '.join(skills[:3])}"
                    params['query'] = skills_query
                
                response = requests.get(url, headers=self.job_apis['jsearch']['headers'], params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if 'data' in data:
                    for job in data['data']:
                        jobs.append(self._format_jsearch_job(job))
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                self.logger.error(f"Error with JSearch API: {str(e)}")
                break
        
        return jobs
    
    def _search_indeed(self, job_title: str, location: str, skills: List[str], 
                      job_type: str, num_pages: int) -> List[Dict]:
        """Search jobs using Indeed API"""
        jobs = []
        
        for page in range(num_pages):
            try:
                url = f"{self.job_apis['indeed']['base_url']}/search"
                params = {
                    'query': job_title,
                    'location': location,
                    'page': page,
                    'limit': 10
                }
                
                response = requests.get(url, headers=self.job_apis['indeed']['headers'], params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if 'results' in data:
                    for job in data['results']:
                        jobs.append(self._format_indeed_job(job))
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                self.logger.error(f"Error with Indeed API: {str(e)}")
                break
        
        return jobs
    
    def _format_jsearch_job(self, job: Dict) -> Dict:
        """Format job data from JSearch API"""
        city = job.get('job_city') or ''
        state = job.get('job_state') or ''
        country = job.get('job_country') or ''
        location_parts = [p for p in [city, state, country] if p]
        location = ', '.join(location_parts) if location_parts else (job.get('job_is_remote') and 'Remote' or 'Not specified')

        min_sal = job.get('job_min_salary')
        max_sal = job.get('job_max_salary')
        sal_period = job.get('job_salary_period', '')
        if min_sal and max_sal:
            salary = f"${int(min_sal):,} - ${int(max_sal):,}{' / ' + sal_period if sal_period else ''}"
        elif min_sal:
            salary = f"${int(min_sal):,}+"
        else:
            salary = 'Not specified'

        return {
            'job_id': job.get('job_id', ''),
            'title': job.get('job_title', ''),
            'company': job.get('employer_name', ''),
            'location': location,
            'salary': salary,
            'description': job.get('job_description', ''),
            'requirements': self._extract_requirements(job.get('job_description', '')),
            'job_type': job.get('job_employment_type', 'Full-time'),
            'experience_level': self._determine_experience_level(job.get('job_description', '')),
            'posted_date': job.get('job_posted_at_datetime_utc', ''),
            'apply_url': job.get('job_apply_link', ''),
            'source': 'JSearch',
            'is_real': True
        }
    
    def _format_indeed_job(self, job: Dict) -> Dict:
        """Format job data from Indeed API"""
        return {
            'job_id': job.get('id', ''),
            'title': job.get('title', ''),
            'company': job.get('company', ''),
            'location': job.get('location', ''),
            'salary': job.get('salary', 'Not specified'),
            'description': job.get('description', ''),
            'requirements': self._extract_requirements(job.get('description', '')),
            'job_type': job.get('type', 'Full-time'),
            'experience_level': self._determine_experience_level(job.get('description', '')),
            'posted_date': job.get('date', ''),
            'apply_url': job.get('url', ''),
            'source': 'Indeed',
            'is_real': True
        }
    
    def _filter_fallback_jobs(self, job_title: str, skills: List[str]) -> List[Dict]:
        """Filter fallback jobs based on job title and skills"""
        filtered_jobs = []
        
        for job in self.fallback_jobs:
            # Check if job title matches
            title_match = any(word.lower() in job['title'].lower() for word in job_title.split())
            
            # Check if skills match
            skill_match = False
            if skills:
                job_requirements = job['requirements'].lower()
                skill_match = any(skill.lower() in job_requirements for skill in skills)
            else:
                skill_match = True
            
            if title_match or skill_match:
                filtered_jobs.append(job)
        
        return filtered_jobs
    
    def _extract_requirements(self, description: str) -> str:
        """Extract key requirements from job description"""
        # Simple keyword extraction - can be enhanced with NLP
        keywords = [
            'python', 'javascript', 'java', 'react', 'node.js', 'sql', 'aws',
            'docker', 'kubernetes', 'machine learning', 'data science', 'ai',
            'frontend', 'backend', 'full stack', 'mobile', 'ios', 'android'
        ]
        
        found_skills = []
        description_lower = description.lower()
        
        for keyword in keywords:
            if keyword in description_lower:
                found_skills.append(keyword.title())
        
        return ', '.join(found_skills[:10])  # Limit to 10 skills
    
    def _determine_experience_level(self, description: str) -> str:
        """Determine experience level from job description"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['senior', 'lead', 'principal', '5+ years', '10+ years']):
            return 'Senior'
        elif any(word in description_lower for word in ['junior', 'entry', '0-2 years', '1-3 years']):
            return 'Entry-Level'
        else:
            return 'Mid-Level'
    
    def _deduplicate_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on title and company"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _sort_jobs_by_relevance(self, jobs: List[Dict], job_title: str, skills: List[str]) -> List[Dict]:
        """Sort jobs by relevance to job title and skills"""
        def relevance_score(job):
            score = 0
            
            # Title match score
            title_words = job_title.lower().split()
            job_title_lower = job['title'].lower()
            for word in title_words:
                if word in job_title_lower:
                    score += 2
            
            # Skills match score
            if skills:
                job_requirements = job['requirements'].lower()
                for skill in skills:
                    if skill.lower() in job_requirements:
                        score += 1
            
            # Real job bonus
            if job.get('is_real', False):
                score += 3
            
            return score
        
        return sorted(jobs, key=relevance_score, reverse=True)
    
    def get_job_details(self, job_id: str) -> Optional[Dict]:
        """Get detailed information about a specific job"""
        # This would typically make an API call to get full job details
        # For now, return a placeholder
        return {
            'job_id': job_id,
            'full_description': 'Full job description would be fetched here',
            'company_info': 'Company information would be fetched here',
            'benefits': 'Benefits and perks would be listed here',
            'application_process': 'Application process details would be here'
        }
    
    def set_api_key(self, api_name: str, api_key: str):
        """Set API key for a specific service"""
        if api_name in self.job_apis:
            self.job_apis[api_name]['headers']['X-RapidAPI-Key'] = api_key
            self.job_apis[api_name]['enabled'] = True
            self.logger.info(f"API key set for {api_name}")
    
    def get_available_apis(self) -> List[str]:
        """Get list of available and enabled APIs"""
        return [name for name, config in self.job_apis.items() if config['enabled']]

# Example usage and testing
if __name__ == "__main__":
    job_service = JobSearchService()
    
    # Test job search
    jobs = job_service.search_jobs(
        job_title="Software Engineer",
        location="San Francisco",
        skills=["Python", "JavaScript", "React"],
        job_type="fulltime"
    )
    
    print(f"Found {len(jobs)} jobs:")
    for job in jobs[:5]:
        print(f"- {job['title']} at {job['company']} ({job['location']})")
        print(f"  Salary: {job['salary']}")
        print(f"  Apply: {job['apply_url']}")
        print()
