# TIIPE & Novatrix Unified Multi-Tenant Backend (Django 5.1 + DRF)

A production-grade, enterprise Multi-Tenant backend architected to power:
1. **TIIPE (Parent Brand)**: [https://impactinstituteglobal.org/](https://impactinstituteglobal.org/) - 501(c)(3) Nonprofit Educational and Community Public Health Platform.
2. **Novatrix (Subsidiary Brand)**: [https://thenovatrix.com/](https://thenovatrix.com/) - End-to-end Custom Software Development, Systems Implementation, and Technology Training Company.
3. **Cross-Platform Mobile Apps**: Native iOS and Android Flutter applications for both brands.

---

## 🏛 Architecture Overview

```
                      +----------------------------------------------------+
                      |       Cloudflare / Nginx / Load Balancer           |
                      +----------------------------------------------------+
                                          |
                  +-----------------------+-----------------------+
                  |                                               |
         Host: impactinstituteglobal.org                 Host: thenovatrix.com
         (Or Mobile Header: X-Tenant: tiipe)             (Or Mobile Header: X-Tenant: novatrix)
                  |                                               |
                  +-----------------------+-----------------------+
                                          |
                     +------------------------------------------+
                     |    TenantHeaderAndHostMiddleware         |
                     |  Resolves host or X-Tenant header        |
                     +------------------------------------------+
                                          |
             +----------------------------+----------------------------+
             |                                                         |
             v                                                         v
    +------------------+                                      +------------------+
    |  Schema: tiipe   |                                      | Schema: novatrix |
    | - TIIPE LMS      |                                      | - Services       |
    | - Mentorship     |                                      | - Projects/Cases |
    | - Governance     |                                      | - Training/Cohort|
    | - Donations      |                                      | - Inquiries      |
    | - Radio/Podcasts |                                      | - Support Tickets|
    | - TIIPE CMS      |                                      | - Novatrix CMS   |
    +------------------+                                      +------------------+
             \                                                         /
              \                                                       /
               +--------------------------+--------------------------+
                                          |
                                          v
                            +---------------------------+
                            |      Schema: public       |
                            | - CustomUser (Shared Auth)|
                            | - Tenant & Domain Routing |
                            | - TenantMembership & Roles|
                            +---------------------------+
```

### Key Architectural Tenets:
- **PostgreSQL Schema Isolation (`django-tenants`)**: High-performance data isolation with strict tenant boundary enforcement.
- **Shared Authentication**: Single login table (`CustomUser`) across both brands with tenant-specific roles (`TenantMembership`).
- **Dynamic Tenant Detection**: Middleware detects tenant through `request.get_host()` domain routing or `X-Tenant: tiipe` / `X-Tenant: novatrix` HTTP headers.
- **Async Execution**: Redis and Celery background workers for transactional emails and push notifications.
- **S3 / Spaces Multi-Tenant Storage**: Media uploads are dynamically routed into schema-scoped cloud directories.
- **Interactive Documentation**: OpenAPI 3.0 with Swagger UI and Redoc powered by `drf-spectacular`.

---

## 🚀 Quickstart with Docker Compose

Ensure Docker and Docker Compose are installed, then execute:

```bash
# 1. Clone the repository and navigate to backend
cd backend

# 2. Copy the environment variables template
cp .env.example .env

# 3. Launch the full stack (Postgres, Redis, Django Backend, Celery Worker, Celery Beat)
docker-compose up --build
```

The container startup automatically runs:
1. `python manage.py migrate_schemas --shared`
2. `python manage.py migrate_schemas --tenant`
3. `python manage.py seed_tenants` (Idempotently creates public, tiipe, and novatrix tenants, superuser, and seed catalog)

API Gateway will be live at: `http://localhost:8000/`

---

## 🔧 Local Development Setup (Without Docker)

```bash
# 1. Create and activate a Python 3.11+ virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables in .env
cp .env.example .env

# 4. Run multi-tenant schema migrations
python manage.py migrate_schemas --shared
python manage.py migrate_schemas --tenant

# 5. Seed initial tenants and content
python manage.py seed_tenants

# 6. Start the development server
python manage.py runserver 0.0.0.0:8000
```

---

## 🔑 Default Credentials (Seed Data)

| Role | Email | Password |
| :--- | :--- | :--- |
| **Global Superuser** | `admin@impactinstituteglobal.org` | `AdminPassword2026!` |

---

## 📱 Mobile App & Web Client Integration Guide

When calling the API from Flutter mobile applications or frontend client web apps, specify the tenant context using **either** of the following methods:

### Method 1: HTTP Header (Recommended for Mobile Apps)
Include the `X-Tenant` header with every request:
```http
GET /api/v1/cms/heroes/ HTTP/1.1
Host: localhost:8000
Authorization: Bearer <JWT_ACCESS_TOKEN>
X-Tenant: tiipe
```

### Method 2: Host / Subdomain Routing
Configure your local `/etc/hosts` or production DNS:
```
127.0.0.1 impactinstituteglobal.org
127.0.0.1 thenovatrix.com
127.0.0.1 tiipe.localhost
127.0.0.1 novatrix.localhost
```
Then send requests directly to `http://tiipe.localhost:8000/api/v1/...` or `http://novatrix.localhost:8000/api/v1/...`.

---

## 📚 Interactive Swagger / OpenAPI Documentation

- **Public Schema Swagger**: `http://localhost:8000/api/docs/`
- **Tenant Schema Swagger**: `http://tiipe.localhost:8000/api/docs/` or with `X-Tenant: novatrix`
- **OpenAPI 3.0 JSON Schema**: `http://localhost:8000/api/schema/`

---

## 🔌 API Endpoint Directory

### Shared Authentication (`/api/v1/auth/`)
- `POST /api/v1/auth/register/` - Register new user, profile, and tenant membership.
- `POST /api/v1/auth/login/` - Authenticate with email/password; returns JWT access/refresh tokens and active tenant memberships.
- `POST /api/v1/auth/token/refresh/` - Refresh expired JWT access token.
- `GET /api/v1/auth/me/` - Retrieve authenticated user profile.
- `PATCH /api/v1/auth/me/` - Update profile bio, phone, avatar, or contact details.
- `POST /api/v1/auth/change-password/` - Update password.

### CMS Content (`/api/v1/cms/`)
- `GET /api/v1/cms/heroes/` - Retrieve active hero banners.
- `GET /api/v1/cms/navigation/` - Header and footer dynamic navigation links.
- `GET /api/v1/cms/governance-documents/` - Bylaws, 501(c)(3) tax letter, annual reports (TIIPE).
- `POST /api/v1/cms/governance-documents/{id}/record_download/` - Track document download count.
- `GET /api/v1/cms/board-members/` - Board of directors and executive leadership bios.
- `GET /api/v1/cms/media-broadcasts/` - AdieTalk radio streams and podcast episodes.
- `GET /api/v1/cms/webinars/` - Upcoming and recorded health/technology webinars.
- `GET /api/v1/cms/impact-metrics/` - Live impact counters (e.g. 2,000+ Students Mentored).
- `GET /api/v1/cms/benefit-statements/` - Brand values and mission pillars.
- `GET /api/v1/cms/articles/` - Insights, announcements, and research articles.
- `GET /api/v1/cms/faqs/` - Frequently asked questions.
- `GET /api/v1/cms/testimonials/` - Client and student testimonials.
- `POST /api/v1/cms/contact/` - Submit general contact message.

### TIIPE LMS & Mentorship (`/api/v1/lms/`)
- `GET /api/v1/lms/programs/` - Core educational and public health programs.
- `POST /api/v1/lms/mentor-applications/` - Submit volunteer mentor onboarding application.
- `POST /api/v1/lms/mentor-applications/{id}/approve/` - Admin verification & background check approval.
- `GET /api/v1/lms/availabilities/` - Mentor weekly schedule slots.
- `GET, POST /api/v1/lms/sessions/` - Schedule and manage 1-on-1 tutoring sessions with automatic video room generation.
- `POST /api/v1/lms/sessions/{id}/complete_session/` - Mentor notes and student rating completion.
- `GET /api/v1/lms/modules/` - Self-paced micro-learning pathways.
- `POST /api/v1/lms/progress/record_lesson/` - Track student lesson progress and certificate eligibility.
- `GET /api/v1/lms/health-resources/` - Public health and maternal health literacy pamphlets.
- `GET /api/v1/lms/policy-briefs/` - Open-access community research papers.

### Novatrix Services & Projects (`/api/v1/services/`)
- `GET /api/v1/services/pillars/` - 4 Core Service Pillars (Software, Implementation, Training, Support).
- `GET /api/v1/services/industries/` - Industry-specific digital transformation solutions.
- `GET /api/v1/services/case-studies/` - Project portfolio with transparent status (Delivered, In Development, Concept).
- `GET /api/v1/services/courses/` - Technology training catalog (Web/Mobile, Data/AI, DevOps).
- `GET /api/v1/services/cohorts/` - Active training cohort schedules.
- `POST /api/v1/services/project-inquiries/` - Submit custom software/system consultation form with brief upload.
- `POST /api/v1/services/training-inquiries/` - Submit individual or corporate training enrollment request.
- `POST /api/v1/services/support-tickets/` - Submit client technical maintenance and support ticket.
- `GET /api/v1/services/downloads/` - Download corporate capability statements and brochures.

### Payments & Invoicing (`/api/v1/payments/`)
- `POST /api/v1/payments/donations/` - Process 501(c)(3) charitable donation (one-time or monthly) with program sub-ledger allocation and automated tax receipt.
- `GET /api/v1/payments/transactions/` - Client and student commercial payment history.
- `GET /api/v1/payments/invoices/` - Itemized corporate invoices.
- `POST /api/v1/payments/webhooks/{gateway}/` - Webhook receiver for Stripe/Paystack.

### Notifications (`/api/v1/notifications/`)
- `POST /api/v1/notifications/push-tokens/` - Register mobile device FCM/APNS token.
- `GET /api/v1/notifications/logs/` - User notification history.

### Files & Media Assets (`/api/v1/files/`)
- `POST /api/v1/files/assets/` - Upload images, audio, or video with automatic tenant directory scoping.
- `POST /api/v1/files/documents/` - Upload capability statements or student worksheets.
