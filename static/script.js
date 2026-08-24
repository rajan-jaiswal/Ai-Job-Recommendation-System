// Smart Career Recommendation System - Frontend JavaScript

class CareerRecommendationApp {
    constructor() {
        this.apiBaseUrl = '';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupSmoothScrolling();
        this.uploadedResumeData = null;
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('recommendationForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Navigation links
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });
    }

    setupSmoothScrolling() {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    handleNavClick(e) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        // Use uploaded resume data if available, otherwise use form data
        let formData;
        if (this.uploadedResumeData) {
            formData = this.uploadedResumeData;
            // Allow manual override of resume data
            const manualSkills = document.getElementById('skills').value.trim();
            const manualInterests = document.getElementById('interests').value.trim();
            const manualAcademic = document.getElementById('academicBackground').value.trim();
            const manualInternships = document.getElementById('previousInternships').value.trim();
            
            if (manualSkills) formData.skills = manualSkills;
            if (manualInterests) formData.interests = manualInterests;
            if (manualAcademic) formData.academic_background = manualAcademic;
            if (manualInternships) formData.previous_internships = manualInternships;
        } else {
            formData = {
                skills: document.getElementById('skills').value.trim(),
                interests: document.getElementById('interests').value.trim(),
                academic_background: document.getElementById('academicBackground').value.trim(),
                previous_internships: document.getElementById('previousInternships').value.trim()
            };
        }

        // Add location and real jobs preference
        formData.location = document.getElementById('location').value.trim();
        formData.include_real_jobs = document.getElementById('includeRealJobs').checked;

        // Validate required fields
        if (!formData.skills || !formData.interests || !formData.academic_background) {
            this.showAlert('Please fill in all required fields (Skills, Interests, and Academic Background) or upload a resume.', 'danger');
            return;
        }

        try {
            this.showLoadingModal();

            let recommendations;
            if (formData.include_real_jobs) {
                // Update loading message to reflect real-time job search
                const loadingText = document.querySelector('#loadingModal .modal-body p');
                if (loadingText) loadingText.textContent = 'Searching real-time job openings for your profile...';
                recommendations = await this.getRecommendationsWithJobs(formData);
            } else {
                recommendations = await this.getRecommendations(formData);
            }

            this.displayRecommendations(recommendations);
            this.hideLoadingModal();
            this.scrollToResults();
        } catch (error) {
            this.hideLoadingModal();
            this.showAlert('Error getting recommendations: ' + error.message, 'danger');
            console.error('Error:', error);
        }
    }

    async getRecommendations(formData) {
        const response = await fetch('/api/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to get recommendations');
        }

        const data = await response.json();
        return data.recommendations;
    }

    async getRecommendationsWithJobs(formData) {
        const response = await fetch('/api/recommendations-with-jobs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to get recommendations with jobs');
        }

        const data = await response.json();
        return data.recommendations;
    }

    displayRecommendations(recommendations) {
        const container = document.getElementById('recommendationsContainer');
        const resultsSection = document.getElementById('results');
        
        if (!container || !resultsSection) return;

        container.innerHTML = '';

        if (recommendations.length === 0) {
            container.innerHTML = `
                <div class="alert alert-warning text-center">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    No recommendations found. Please try adjusting your profile.
                </div>
            `;
            resultsSection.style.display = 'block';
            return;
        }

        // Create recommendations HTML
        recommendations.forEach((rec, index) => {
            const card = this.createRecommendationCard(rec, index + 1);
            container.appendChild(card);
        });

        // Add visualization
        this.addVisualization(recommendations);
        
        resultsSection.style.display = 'block';
        resultsSection.classList.add('fade-in');
    }

    createRecommendationCard(recommendation, rank) {
        const card = document.createElement('div');
        card.className = 'recommendation-card fade-in';
        card.style.animationDelay = `${rank * 0.1}s`;

        const similarityPercentage = Math.round(recommendation.similarity_score * 100);
        const skills = recommendation.required_skills.split(',').map(s => s.trim());
        const realJobs = recommendation.real_jobs || [];

        card.innerHTML = `
            <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="mb-0">
                    <i class="fas fa-medal me-2 text-warning"></i>
                    #${rank} ${recommendation.title}
                </h5>
                <span class="similarity-score">
                    ${similarityPercentage}% Match
                </span>
            </div>
            
            <p class="text-muted mb-3">${recommendation.description}</p>
            
            <div class="row mb-3">
                <div class="col-md-6">
                    <h6 class="text-primary mb-2">
                        <i class="fas fa-dollar-sign me-1"></i>
                        Salary Range
                    </h6>
                    <p class="mb-0">${recommendation.salary_range}</p>
                </div>
                <div class="col-md-6">
                    <h6 class="text-primary mb-2">
                        <i class="fas fa-chart-line me-1"></i>
                        Experience Level
                    </h6>
                    <p class="mb-0">${recommendation.experience_level}</p>
                </div>
            </div>
            
            <div class="mb-3">
                <h6 class="text-primary mb-2">
                    <i class="fas fa-tools me-1"></i>
                    Required Skills
                </h6>
                <div class="skills-tags">
                    ${skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                </div>
            </div>
            
            ${realJobs.length > 0 ? this.createRealJobsSection(realJobs) : ''}
            
            <div class="match-reasons">
                <h6 class="text-success mb-2">
                    <i class="fas fa-check-circle me-1"></i>
                    Why This Matches You
                </h6>
                <ul class="mb-0">
                    ${recommendation.match_reasons.map(reason => `<li>${reason}</li>`).join('')}
                </ul>
            </div>
        `;

        return card;
    }

    createRealJobsSection(realJobs) {
        return `
            <div class="real-jobs-section mb-4">
                <h6 class="text-success mb-3">
                    <i class="fas fa-briefcase me-1"></i>
                    Real Job Openings (${realJobs.length} found)
                </h6>
                <div class="row">
                    ${realJobs.map(job => this.createJobCard(job)).join('')}
                </div>
            </div>
        `;
    }

    createJobCard(job) {
        const isReal = job.is_real || false;
        const sourceBadge = isReal
            ? `<span class="badge bg-success"><i class="fas fa-circle me-1" style="font-size:8px"></i>Live</span>`
            : `<span class="badge bg-secondary">Sample</span>`;
        const salary = job.salary && job.salary !== 'Not specified' ? job.salary : 'Salary not listed';
        const desc = job.description ? job.description.substring(0, 120) + '...' : '';
        const loc = [job.location].filter(Boolean).join('').replace(/^,\s*/, '') || 'Location not listed';

        return `
            <div class="col-md-6 mb-3">
                <div class="card job-card h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="card-title mb-0">${job.title}</h6>
                            ${sourceBadge}
                        </div>
                        <p class="text-muted mb-1">
                            <i class="fas fa-building me-1"></i>
                            ${job.company}
                        </p>
                        <p class="text-muted mb-1">
                            <i class="fas fa-map-marker-alt me-1"></i>
                            ${loc}
                        </p>
                        <p class="text-primary mb-2">
                            <i class="fas fa-dollar-sign me-1"></i>
                            ${salary}
                        </p>
                        ${desc ? `<p class="small text-muted mb-3">${desc}</p>` : ''}
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">
                                <i class="fas fa-clock me-1"></i>
                                ${job.experience_level || 'Mid-Level'}
                            </small>
                            ${job.apply_url ? `
                                <a href="${job.apply_url}" target="_blank" rel="noopener" class="btn btn-sm btn-primary">
                                    <i class="fas fa-external-link-alt me-1"></i>
                                    Apply Now
                                </a>
                            ` : `
                                <button class="btn btn-sm btn-outline-secondary" disabled>
                                    <i class="fas fa-info-circle me-1"></i>
                                    Sample Job
                                </button>
                            `}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    addVisualization(recommendations) {
        const container = document.getElementById('recommendationsContainer');
        
        // Create chart container
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container';
        chartContainer.innerHTML = `
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-chart-bar me-2"></i>
                        Recommendation Analysis
                    </h5>
                </div>
                <div class="card-body">
                    <canvas id="recommendationChart" width="400" height="200"></canvas>
                </div>
            </div>
        `;
        
        container.appendChild(chartContainer);

        // Create chart
        this.createRecommendationChart(recommendations);
    }

    createRecommendationChart(recommendations) {
        const ctx = document.getElementById('recommendationChart');
        if (!ctx) return;

        const labels = recommendations.map(rec => rec.title);
        const scores = recommendations.map(rec => Math.round(rec.similarity_score * 100));
        const colors = [
            'rgba(13, 110, 253, 0.8)',
            'rgba(25, 135, 84, 0.8)',
            'rgba(255, 193, 7, 0.8)',
            'rgba(220, 53, 69, 0.8)',
            'rgba(111, 66, 193, 0.8)'
        ];

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Match Percentage',
                    data: scores,
                    backgroundColor: colors.slice(0, recommendations.length),
                    borderColor: colors.slice(0, recommendations.length).map(color => color.replace('0.8', '1')),
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Match: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    async loadStudents() {
        try {
            const response = await fetch('/api/students');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayStudentsTable(data.students);
            } else {
                throw new Error(data.error || 'Failed to load students');
            }
        } catch (error) {
            this.showAlert('Error loading students: ' + error.message, 'danger');
        }
    }

    async loadCareers() {
        try {
            const response = await fetch('/api/careers');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayCareersTable(data.careers);
            } else {
                throw new Error(data.error || 'Failed to load careers');
            }
        } catch (error) {
            this.showAlert('Error loading careers: ' + error.message, 'danger');
        }
    }

    displayStudentsTable(students) {
        const container = document.getElementById('adminContent');
        if (!container) return;

        const tableHtml = `
            <div class="admin-table">
                <table class="table table-striped table-hover mb-0">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Skills</th>
                            <th>Interests</th>
                            <th>Academic Background</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${students.map(student => `
                            <tr>
                                <td>${student.student_id}</td>
                                <td>${student.name}</td>
                                <td>
                                    <div class="skills-tags">
                                        ${student.skills.split(',').slice(0, 3).map(skill => 
                                            `<span class="skill-tag">${skill.trim()}</span>`
                                        ).join('')}
                                        ${student.skills.split(',').length > 3 ? 
                                            `<span class="skill-tag">+${student.skills.split(',').length - 3} more</span>` : ''
                                        }
                                    </div>
                                </td>
                                <td>
                                    <small class="text-muted">${student.interests.substring(0, 50)}...</small>
                                </td>
                                <td>
                                    <small class="text-muted">${student.academic_background}</small>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        container.innerHTML = tableHtml;
    }

    displayCareersTable(careers) {
        const container = document.getElementById('adminContent');
        if (!container) return;

        const tableHtml = `
            <div class="admin-table">
                <table class="table table-striped table-hover mb-0">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Required Skills</th>
                            <th>Salary Range</th>
                            <th>Experience Level</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${careers.map(career => `
                            <tr>
                                <td>${career.career_id}</td>
                                <td>
                                    <strong>${career.title}</strong>
                                    <br><small class="text-muted">${career.description.substring(0, 100)}...</small>
                                </td>
                                <td>
                                    <div class="skills-tags">
                                        ${career.required_skills.split(',').slice(0, 3).map(skill => 
                                            `<span class="skill-tag">${skill.trim()}</span>`
                                        ).join('')}
                                        ${career.required_skills.split(',').length > 3 ? 
                                            `<span class="skill-tag">+${career.required_skills.split(',').length - 3} more</span>` : ''
                                        }
                                    </div>
                                </td>
                                <td>
                                    <span class="badge bg-success">${career.salary_range}</span>
                                </td>
                                <td>
                                    <span class="badge bg-info">${career.experience_level}</span>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        container.innerHTML = tableHtml;
    }

    showLoadingModal() {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        modal.show();
        
        // Add progress indication with faster animation
        const loadingText = document.querySelector('#loadingModal .modal-body p');
        if (loadingText) {
            let dots = 0;
            const interval = setInterval(() => {
                dots = (dots + 1) % 4;
                loadingText.textContent = 'Analyzing your profile' + '.'.repeat(dots);
            }, 300); // Faster animation
            
            // Store interval ID to clear it later
            this.loadingInterval = interval;
        }
    }

    hideLoadingModal() {
        // Clear loading animation
        if (this.loadingInterval) {
            clearInterval(this.loadingInterval);
            this.loadingInterval = null;
        }
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
        if (modal) {
            modal.hide();
        }
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertContainer.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertContainer);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertContainer.parentNode) {
                alertContainer.remove();
            }
        }, 5000);
    }

    scrollToResults() {
        const resultsSection = document.getElementById('results');
        if (resultsSection) {
            resultsSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    getSampleJobsForCareer(careerTitle) {
        // Return sample jobs for the given career
        const sampleJobs = [
            {
                job_id: 'sample_1',
                title: careerTitle,
                company: 'TechCorp Inc.',
                location: 'San Francisco, CA',
                salary: '$80,000 - $120,000',
                description: 'Join our team to work on cutting-edge projects and build innovative solutions.',
                requirements: 'Python, JavaScript, React, Node.js, SQL',
                job_type: 'Full-time',
                experience_level: 'Mid-Level',
                posted_date: '2024-01-15',
                apply_url: 'https://techcorp.com/careers',
                source: 'Company Website',
                is_real: false
            },
            {
                job_id: 'sample_2',
                title: `Senior ${careerTitle}`,
                company: 'DataLab Solutions',
                location: 'New York, NY',
                salary: '$90,000 - $140,000',
                description: 'Lead exciting projects and mentor junior developers in a collaborative environment.',
                requirements: 'Python, Machine Learning, SQL, Statistics, TensorFlow',
                job_type: 'Full-time',
                experience_level: 'Senior',
                posted_date: '2024-01-14',
                apply_url: 'https://datalab.com/careers',
                source: 'Company Website',
                is_real: false
            },
            {
                job_id: 'sample_3',
                title: `${careerTitle} (Remote)`,
                company: 'CloudTech',
                location: 'Remote',
                salary: '$75,000 - $115,000',
                description: 'Work from anywhere and contribute to our global team of talented professionals.',
                requirements: 'Python, AWS, Docker, Kubernetes, CI/CD',
                job_type: 'Full-time',
                experience_level: 'Mid-Level',
                posted_date: '2024-01-13',
                apply_url: 'https://cloudtech.com/careers',
                source: 'Company Website',
                is_real: false
            }
        ];
        
        return sampleJobs;
    }

    async uploadResume() {
        const fileInput = document.getElementById('resumeFile');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showAlert('Please select a resume file first.', 'warning');
            return;
        }

        // Validate file size (16MB max)
        if (file.size > 16 * 1024 * 1024) {
            this.showAlert('File size too large. Maximum size is 16MB.', 'danger');
            return;
        }

        // Validate file type
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!allowedTypes.includes(file.type)) {
            this.showAlert('Invalid file type. Please upload a PDF or DOCX file.', 'danger');
            return;
        }

        try {
            this.showLoadingModal();
            
            // Update loading message for resume processing
            const loadingText = document.querySelector('#loadingModal .modal-body p');
            if (loadingText) {
                loadingText.textContent = 'Processing resume and searching for real jobs...';
            }
            
            const formData = new FormData();
            formData.append('resume', file);

            // Use longer timeout for resume upload with real job search
            const timeoutPromise = new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Resume processing timeout')), 30000)
            );

            const response = await Promise.race([
                fetch('/api/upload-resume', {
                    method: 'POST',
                    body: formData
                }),
                timeoutPromise
            ]);

            const data = await response.json();
            this.hideLoadingModal();

            if (data.status === 'success') {
                // Store parsed data
                this.uploadedResumeData = data.parsed_data;
                
                // Populate form fields with parsed data
                this.populateFormFromResume(data.parsed_data);
                
                // Count real jobs
                let realJobCount = 0;
                data.recommendations.forEach(rec => {
                    if (rec.real_jobs) {
                        realJobCount += rec.real_jobs.filter(job => job.is_real).length;
                    }
                });
                
                // Show success message with real job count
                if (realJobCount > 0) {
                    this.showAlert(`Resume processed successfully! Found ${realJobCount} real job openings.`, 'success');
                } else {
                    this.showAlert('Resume processed successfully! Showing sample jobs for demonstration.', 'info');
                }
                
                // Display recommendations with real jobs
                this.displayRecommendations(data.recommendations);
                this.scrollToResults();
                
            } else {
                this.showAlert('Error parsing resume: ' + data.error, 'danger');
            }

        } catch (error) {
            this.hideLoadingModal();
            if (error.message.includes('timeout')) {
                this.showAlert('Resume processing timed out. Please try again or use manual form entry.', 'warning');
            } else {
                this.showAlert('Error uploading resume: ' + error.message, 'danger');
            }
            console.error('Error:', error);
        }
    }

    populateFormFromResume(parsedData) {
        // Populate form fields with parsed resume data
        if (parsedData.skills) {
            document.getElementById('skills').value = parsedData.skills;
        }
        if (parsedData.interests) {
            document.getElementById('interests').value = parsedData.interests;
        }
        if (parsedData.academic_background) {
            document.getElementById('academicBackground').value = parsedData.academic_background;
        }
        if (parsedData.previous_internships) {
            document.getElementById('previousInternships').value = parsedData.previous_internships;
        }
    }

    async parseResumeOnly() {
        const fileInput = document.getElementById('resumeFile');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showAlert('Please select a resume file first.', 'warning');
            return;
        }

        try {
            this.showLoadingModal();
            
            const formData = new FormData();
            formData.append('resume', file);

            const response = await fetch('/api/parse-resume-only', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            this.hideLoadingModal();

            if (data.status === 'success') {
                // Store parsed data
                this.uploadedResumeData = data.parsed_data;
                
                // Populate form fields with parsed data
                this.populateFormFromResume(data.parsed_data);
                
                // Show success message
                this.showAlert('Resume parsed successfully! Form has been auto-filled.', 'success');
                
            } else {
                this.showAlert('Error parsing resume: ' + data.error, 'danger');
            }

        } catch (error) {
            this.hideLoadingModal();
            this.showAlert('Error parsing resume: ' + error.message, 'danger');
            console.error('Error:', error);
        }
    }
}

// Global functions for admin buttons
function loadStudents() {
    if (window.careerApp) {
        window.careerApp.loadStudents();
    }
}

function loadCareers() {
    if (window.careerApp) {
        window.careerApp.loadCareers();
    }
}

// Global functions for resume handling
function handleFileSelect(input) {
    const file = input.files[0];
    const uploadBtn = document.getElementById('uploadBtn');
    const resumePreview = document.getElementById('resumePreview');
    const resumeInfo = document.getElementById('resumeInfo');
    
    if (file) {
        // Enable upload button
        uploadBtn.disabled = false;
        
        // Show file info
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        resumeInfo.textContent = `Selected: ${file.name} (${fileSize} MB)`;
        resumePreview.style.display = 'block';
        
        // Validate file type
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!allowedTypes.includes(file.type)) {
            resumeInfo.innerHTML = `<span class="text-danger">Invalid file type. Please select a PDF or DOCX file.</span>`;
            uploadBtn.disabled = true;
        } else if (file.size > 16 * 1024 * 1024) {
            resumeInfo.innerHTML = `<span class="text-danger">File too large. Maximum size is 16MB.</span>`;
            uploadBtn.disabled = true;
        } else {
            resumeInfo.innerHTML = `<span class="text-success">Ready to upload: ${file.name} (${fileSize} MB)</span>`;
        }
    } else {
        uploadBtn.disabled = true;
        resumePreview.style.display = 'none';
    }
}

function uploadResume() {
    if (window.careerApp) {
        window.careerApp.uploadResume();
    }
}

function parseResumeOnly() {
    if (window.careerApp) {
        window.careerApp.parseResumeOnly();
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.careerApp = new CareerRecommendationApp();
    
    // Add some sample data to form for demo purposes
    const skillsField = document.getElementById('skills');
    const interestsField = document.getElementById('interests');
    const academicField = document.getElementById('academicBackground');
    const internshipsField = document.getElementById('previousInternships');
    
    if (skillsField && interestsField && academicField) {
        // Add placeholder text with examples
        skillsField.placeholder = 'e.g., Python, Machine Learning, Data Analysis, SQL, Statistics, JavaScript, React';
        interestsField.placeholder = 'e.g., Web Development, Data Science, AI, Mobile Apps, UI/UX Design';
        academicField.placeholder = 'e.g., Computer Science, Bachelor, 3.8 GPA';
        internshipsField.placeholder = 'e.g., Software Developer Intern at TechCorp, 3 months';
    }
});

// Add some utility functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success message
        const app = window.careerApp;
        if (app) {
            app.showAlert('Copied to clipboard!', 'success');
        }
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('recommendationForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
});

// Add form validation
function validateForm() {
    const requiredFields = ['skills', 'interests', 'academicBackground'];
    let isValid = true;
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else if (field) {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Add real-time form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    if (form) {
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    }
});
