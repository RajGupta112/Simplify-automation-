SimplifIQ - AI Lead Automation System

An AI-powered lead enrichment and automated outreach platform built using Django, Celery, Redis, Gemini AI, Playwright, and ReportLab.

This system automates the complete lead qualification and outreach workflow for B2B businesses.

Features
Lead intake API
Company website scraping
AI-powered company analysis
Personalized business insights
Automated PDF audit generation
Personalized outreach email generation
Automatic email delivery
Asynchronous workflow using Celery + Redis
Error handling and workflow status tracking
End-to-End Workflow
User submits lead form
System validates input
Website data is scraped using Playwright
Gemini AI analyzes the company
AI generates:
Company summary
Pain points
AI opportunities
Automation recommendations
Personalized outreach email
Professional PDF audit report is generated
PDF is automatically emailed to the lead
Workflow status updated in database
Tech Stack

Backend:

Django
Django REST Framework

Async Processing:

Celery
Redis

AI:

Gemini 2.5 Flash

Web Scraping:

Playwright

PDF Generation:

ReportLab

Database:

PostgreSQL / SQLite
Project Structure
core/
├── core/
├── leads/
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── enrichment_service.py
│   │   ├── pdf_service.py
│   │   └── email_service.py
│   ├── tasks.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── media/
├── templates/
├── manage.py
└── requirements.txt
Installation
Clone Repository
git clone <repo_url>
cd simplifyiq
Create Virtual Environment

Linux/macOS:

python -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Install Playwright Browsers
playwright install
Environment Variables

Create .env

SECRET_KEY=your_secret_key

DEBUG=True

DATABASE_URL=sqlite:///db.sqlite3

REDIS_URL=redis://127.0.0.1:6379/0

GEMINI_API_KEY=your_gemini_api_key

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

DEFAULT_FROM_EMAIL=automation.ai@gmail.com
Database Migration
python manage.py migrate
Run Redis
redis-server
Run Celery Worker
celery -A core worker -l info
Run Django Server
python manage.py runserver
API Endpoint

POST Request:

/api/leads/

Example Payload:

{
    "full_name": "Raj Gupta",
    "email": "raj@gmail.com",
    "company_name": "DOstack",
    "website": "https://dostack.ai",
    "industry": "Artificial Intelligence",
    "business_goal": "Improve AI onboarding experience"
}
AI Capabilities

The AI system generates:

Personalized company summaries
Operational pain points
AI transformation opportunities
Workflow automation recommendations
High-converting outreach emails

The generated insights are based on:

Website content
Business context
Industry
Business goals
Technology stack
Architecture Decisions
Why Celery?

Celery is used for asynchronous background processing because:

AI requests take time
Web scraping is slow
PDF generation is resource-intensive
Email sending should not block API responses
Why Playwright?

Playwright is used because many modern websites are JavaScript-rendered and traditional scraping libraries cannot extract complete content reliably.

Why Gemini AI?

Gemini 2.5 Flash provides:

Fast response times
Good reasoning capability
Structured JSON generation
Strong business analysis quality
Error Handling

The system handles:

Invalid websites
Scraping failures
AI API failures
Email delivery failures
PDF generation issues
Missing website content

Workflow statuses:

Pending
Processing
Completed
Failed
Tradeoffs & Limitations
Dynamic websites may block scraping
AI responses occasionally require JSON cleanup
Large website content is truncated for token optimization
Email personalization depends on available public data
Future Improvements
Frontend dashboard
CRM integration
Retry queue system
Multi-page website crawling
AI lead scoring
Admin analytics panel
Multi-language support
Author

Raj Gupta

AI Software Developer Internship Assessment Submission