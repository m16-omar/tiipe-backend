import datetime
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.core.models import ClientTenant, Domain
from apps.users.models import UserProfile, TenantMembership

class Command(BaseCommand):
    help = "Idempotently seeds multi-tenant schemas (Public, TIIPE, Novatrix) with users, CMS content, programs, services, and courses."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("==> Initializing Multi-Tenant Seeding Process..."))
        User = get_user_model()

        # 1. SEED PUBLIC SCHEMA TENANT & DOMAIN
        connection.set_schema_to_public()
        public_tenant, created = ClientTenant.objects.get_or_create(
            schema_name='public',
            defaults={
                'name': 'Public Gateway & Identity Management',
                'brand_type': 'public',
                'tagline': 'Master Routing and Shared Authentication Gateway',
                'description': 'Public schema handling global users and routing.',
                'primary_color': '#1E3A8A',
                'contact_email': 'admin@impactinstituteglobal.org',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✓ Created Public Tenant Schema"))

        # Add domains for public schema
        for dom_name in ['localhost', '127.0.0.1', 'backend', 'api.impactinstituteglobal.org']:
            Domain.objects.get_or_create(
                domain=dom_name,
                defaults={'tenant': public_tenant, 'is_primary': (dom_name == 'localhost')}
            )

        # 2. CREATE SUPERUSER
        admin_email = 'admin@impactinstituteglobal.org'
        admin_user = User.objects.filter(email=admin_email).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                email=admin_email,
                password='AdminPassword2026!'
            )
            UserProfile.objects.create(
                user=admin_user,
                first_name='Global',
                last_name='Administrator',
                phone='+1 914-555-0199',
                bio='Master System Administrator for TIIPE and Novatrix platforms.',
                background_check_status='verified'
            )
            self.stdout.write(self.style.SUCCESS(f"✓ Created Superuser: {admin_email} (Password: AdminPassword2026!)"))

        # 3. CREATE TIIPE TENANT (PARENT)
        tiipe_tenant, t_created = ClientTenant.objects.get_or_create(
            schema_name='tiipe',
            defaults={
                'name': 'The Impact Institute for Public Education',
                'brand_type': 'tiipe',
                'tagline': 'Transforming knowledge into impact.',
                'description': (
                    'Promoting equitable access to education, lifelong learning, workforce development, '
                    'public health education, civic engagement, and community-based research.'
                ),
                'primary_color': '#1E3A8A',
                'accent_color': '#D97706',
                'contact_email': 'info@impactinstituteglobal.org',
                'contact_phone': '+1 (914) 235-0000',
                'is_active': True
            }
        )
        if t_created:
            self.stdout.write(self.style.SUCCESS("✓ Created TIIPE Tenant Schema ('tiipe')"))

        # TIIPE Domains
        for dom in ['impactinstituteglobal.org', 'www.impactinstituteglobal.org', 'tiipe.localhost']:
            Domain.objects.get_or_create(
                domain=dom,
                defaults={'tenant': tiipe_tenant, 'is_primary': (dom == 'impactinstituteglobal.org')}
            )

        # 4. CREATE NOVATRIX TENANT (SUBSIDIARY)
        novatrix_tenant, n_created = ClientTenant.objects.get_or_create(
            schema_name='novatrix',
            defaults={
                'name': 'Novatrix Technology & Workforce Development',
                'brand_type': 'novatrix',
                'tagline': 'Software that works. Systems that scale. Training that lasts.',
                'description': (
                    'End-to-end digital transformation and workforce development: custom software development, '
                    'system implementation, and practical technology training.'
                ),
                'primary_color': '#163A5F',
                'accent_color': '#2563EB',
                'contact_email': 'contact@thenovatrix.com',
                'contact_phone': '+234 800 668 2874',
                'is_active': True
            }
        )
        if n_created:
            self.stdout.write(self.style.SUCCESS("✓ Created Novatrix Tenant Schema ('novatrix')"))

        # Novatrix Domains
        for dom in ['thenovatrix.com', 'www.thenovatrix.com', 'novatrix.localhost']:
            Domain.objects.get_or_create(
                domain=dom,
                defaults={'tenant': novatrix_tenant, 'is_primary': (dom == 'thenovatrix.com')}
            )

        # Attach Admin Memberships
        TenantMembership.objects.get_or_create(user=admin_user, tenant=tiipe_tenant, role='admin')
        TenantMembership.objects.get_or_create(user=admin_user, tenant=novatrix_tenant, role='admin')

        # 5. SEED TIIPE TENANT SCHEMA CONTENT
        self.stdout.write(self.style.NOTICE("==> Seeding TIIPE Tenant Data..."))
        connection.set_tenant(tiipe_tenant)
        self._seed_tiipe_data()

        # 6. SEED NOVATRIX TENANT SCHEMA CONTENT
        self.stdout.write(self.style.NOTICE("==> Seeding Novatrix Tenant Data..."))
        connection.set_tenant(novatrix_tenant)
        self._seed_novatrix_data()

        # Reset connection to public
        connection.set_schema_to_public()
        self.stdout.write(self.style.SUCCESS("✨ Successfully completed Multi-Tenant Seeding!"))

    def _seed_tiipe_data(self):
        from apps.cms.models import (
            HeroSection, NavigationMenu, GovernanceDocument, BoardMember,
            MediaBroadcast, Webinar, ImpactMetric, PublicBenefitStatement,
            FAQ, Testimonial
        )
        from apps.tiipe_lms.models import Program, LearningModule, Lesson, PublicHealthResource, PolicyBrief

        # Hero
        HeroSection.objects.update_or_create(
            page_identifier='home',
            defaults={
                'headline': 'Transforming Knowledge into Lasting Social Impact',
                'subheadline': (
                    'Expanding equitable access to tutoring, workforce readiness, maternal health literacy, '
                    'civic engagement, and community-based research in New Rochelle, NY and globally.'
                ),
                'cta_primary_text': 'Become a Mentor',
                'cta_primary_link': '/volunteer',
                'cta_secondary_text': 'Explore Programs',
                'cta_secondary_link': '/programs',
                'cta_tertiary_text': 'Donate to TIIPE',
                'cta_tertiary_link': '/donate',
                'background_image_url': 'https://impactinstituteglobal.org/hero-bg.jpg',
                'is_active': True
            }
        )

        # Impact Metrics
        metrics = [
            ('Active Learners Supported', '2,000', '+', 'Underserved students reaching academic milestones', 1),
            ('Verified Tutoring Completed', '5,000', ' hrs', '1-on-1 personalized mentorship delivered', 2),
            ('Health Literacy Pamphlets', '10,000', '+', 'Maternal health and prevention downloads', 3),
            ('Community Policy Briefs', '6', '', 'Open-access research publications released', 4),
        ]
        for label, val, suff, desc, order in metrics:
            ImpactMetric.objects.update_or_create(
                label=label,
                defaults={'value': val, 'suffix': suff, 'description': desc, 'display_order': order}
            )

        # Governance Documents
        gov_docs = [
            ('TIIPE Corporate Bylaws & Governance Framework', 'bylaws', 'Foundational governance charter establishing board authority and voting.', 'https://impactinstituteglobal.org/docs/bylaws.pdf'),
            ('Conflict of Interest & Recusal Standards', 'conflict_of_interest', 'Ethical policy governing disclosures and fiduciary responsibility.', 'https://impactinstituteglobal.org/docs/coi_policy.pdf'),
            ('501(c)(3) Tax-Exempt IRS Determination Letter', '501c3_status', 'Official recognition of nonprofit tax-deductible charitable status.', 'https://impactinstituteglobal.org/docs/501c3.pdf'),
            ('Annual Public Benefit & Financial Impact Report', 'annual_report', 'Itemized allocation of philanthropic funding across educational programs.', 'https://impactinstituteglobal.org/docs/annual_report.pdf'),
        ]
        for title, dtype, desc, furl in gov_docs:
            GovernanceDocument.objects.update_or_create(
                title=title,
                defaults={'doc_type': dtype, 'description': desc, 'file_url': furl, 'published_year': 2026, 'is_public': True}
            )

        # Board Members
        board = [
            ('Dr. Adie A.', 'Founder & President', 'Leading civic educator and researcher passionate about systemic educational access.', 1),
            ('Sarah Jenkins, CPA', 'Treasurer & Board Chair', 'Over 15 years nonprofit financial stewardship and governance oversight.', 2),
            ('Marcus O. Vance', 'Director of Community Outreach', 'Civic organizer focused on youth development and workforce equity.', 3),
        ]
        for name, role, bio, order in board:
            BoardMember.objects.update_or_create(
                name=name,
                defaults={'role_title': role, 'bio': bio, 'display_order': order, 'is_active': True}
            )

        # Programs
        programs = [
            (
                'Academic Tutoring & Youth Mentorship', 'academic-tutoring', 'education_tutoring',
                'Personalized academic guidance connecting underserved students with certified professional mentors.',
                'Match 1,000 students to verified tutors across mathematics, reading, and digital science.',
                'High school and middle school students in New Rochelle, NY.'
            ),
            (
                'Workforce Readiness & Digital BootCamp', 'workforce-readiness', 'workforce_development',
                'Hands-on technical training equipping youth and career changers with coding and digital skills.',
                'Train 500 emerging professionals for high-demand digital careers.',
                'Young adults and career changers seeking technology certifications.'
            ),
            (
                'Maternal & Public Health Education', 'public-health-literacy', 'public_health',
                'Culturally tailored health literacy campaigns promoting maternal wellness and disease prevention.',
                'Distribute 10,000 health pamphlets and reach 1,500 webinar participants.',
                'Families, mothers, and community wellness advocates.'
            ),
            (
                'Civic Participation & AdieTalk Media', 'civic-engagement', 'civic_engagement',
                'Empowering community voices through broadcast media, town halls, and democratic literacy.',
                'Reach 5,000 monthly active listeners on AdieTalk Radio.',
                'Community advocates, local voters, and civic organizations.'
            )
        ]
        for ptitle, pslug, pcat, psum, pgoal, paud in programs:
            prog, _ = Program.objects.update_or_create(
                slug=pslug,
                defaults={
                    'title': ptitle,
                    'category': pcat,
                    'summary': psum,
                    'description': psum,
                    'impact_goal': pgoal,
                    'target_audience': paud,
                    'is_active': True
                }
            )
            # Add a sample module
            mod, _ = LearningModule.objects.update_or_create(
                program=prog,
                slug=f"{pslug}-foundations",
                defaults={
                    'title': f"{ptitle} - Foundations Pathway",
                    'description': 'Interactive self-paced micro-learning curriculum with downloadable worksheets.',
                    'level': 'beginner',
                    'estimated_hours': 6,
                    'is_published': True
                }
            )
            Lesson.objects.update_or_create(
                module=mod,
                display_order=1,
                defaults={
                    'title': 'Unit 1: Core Principles & Skill Assessment',
                    'content_body': '# Welcome to Unit 1\nThis lesson outlines the primary skills and practice drills.',
                    'worksheet_download_url': 'https://impactinstituteglobal.org/worksheets/unit1.pdf'
                }
            )

        # Media Broadcast
        MediaBroadcast.objects.update_or_create(
            title='AdieTalk Radio: Bridging the Digital Divide in Public Education',
            defaults={
                'media_type': 'adietalk_radio',
                'summary': 'Live community broadcast discussing educational equity, youth mentoring, and workforce readiness.',
                'stream_url': 'https://impactinstituteglobal.org/radio/stream.mp3',
                'duration_minutes': 45,
                'is_featured': True
            }
        )

        # Public Health Resource
        PublicHealthResource.objects.update_or_create(
            title='Maternal Nutrition and Early Childhood Health Guide (2026)',
            defaults={
                'category': 'maternal_health',
                'description': 'Comprehensive, evidence-based guide for expecting mothers and young families.',
                'target_group': 'Expecting Mothers & Caregivers',
                'file_download_url': 'https://impactinstituteglobal.org/health/maternal-guide-2026.pdf'
            }
        )

        # Policy Brief
        PolicyBrief.objects.update_or_create(
            slug='educational-equity-new-rochelle-2026',
            defaults={
                'title': 'Addressing Systemic Barriers to Economic Mobility in Suburban Public Schools',
                'abstract': 'An empirical analysis of tutoring accessibility and digital literacy interventions in Westchester County.',
                'research_area': 'Educational Equity & Civic Mobility',
                'pdf_download_url': 'https://impactinstituteglobal.org/research/policy-brief-2026-01.pdf'
            }
        )

        self.stdout.write(self.style.SUCCESS("✓ TIIPE Tenant Data Seeded"))

    def _seed_novatrix_data(self):
        from apps.cms.models import HeroSection, FAQ, Testimonial
        from apps.novatrix_services.models import (
            ServicePillar, IndustrySolution, ProjectCaseStudy,
            TrainingCourse, TrainingCohort, CapabilityDownload
        )

        # Hero
        HeroSection.objects.update_or_create(
            page_identifier='home',
            defaults={
                'headline': 'Software that works. Systems that scale. Training that lasts.',
                'subheadline': (
                    'Novatrix designs custom software, implements enterprise digital systems, '
                    'and provides practical technology training for organizations and emerging professionals.'
                ),
                'cta_primary_text': 'Discuss Your Project',
                'cta_primary_link': '/consultation',
                'cta_secondary_text': 'Explore Our Training',
                'cta_secondary_link': '/courses',
                'background_image_url': 'https://thenovatrix.com/hero-bg.jpg',
                'is_active': True
            }
        )

        # 4 Core Service Pillars
        pillars = [
            (
                'Custom Software Development', 'software-development',
                'Secure, scalable, and user-friendly web, mobile, portal, and API solutions tailored to operational needs.',
                'Organizations struggle with rigid off-the-shelf tools that do not fit their exact operational workflows.',
                ['Web Applications (Django, React, Next.js)', 'Cross-Platform Mobile Apps (Flutter iOS/Android)', 'REST & GraphQL API Architectures', 'Custom Admin Dashboards & Portals'],
                'Greenfield Product Build, Legacy Modernization, Architecture & Security Audit',
                ['Discover & Requirements Alignment', 'Define Architecture & Data Schema', 'Design Wireframes & Prototypes', 'Develop & Unit Test', 'Launch & Production Deployment'],
                1
            ),
            (
                'System Implementation & Integration', 'system-implementation',
                'End-to-end deployment, data migration, configuration, and API integration connecting critical business applications.',
                'Systems fail when implementation ignores data migration, workflow configuration, and user training.',
                ['Enterprise ERP & CRM Configuration', 'Payment Gateway & Financial Ledger Integration', 'Database & Cloud Migration', 'Third-Party Webhook & Event Pipelines'],
                'Platform Migration, Third-Party Integration, Business Automation',
                ['System Assessment', 'Data Mapping & Schema Validation', 'Configuration & Integration', 'User Acceptance Testing', 'Go-Live Support'],
                2
            ),
            (
                'Technology Training & Workforce Development', 'technology-training',
                'Hands-on, project-based training from digital foundations to software engineering, data analytics, and cloud.',
                'Traditional courses teach theoretical concepts without real-world engineering projects or verified competency.',
                ['Individual Immersive BootCamps', 'Custom Corporate Team Upskilling', 'Assessed Digital Credentials', 'Production Portfolio Projects'],
                'Cohort-Based Training, Corporate Workshops, Self-Paced Mentored Tracks',
                ['Needs Assessment', 'Hands-On Curriculum Delivery', 'Real-World Capstone Build', 'Assessment & Credentialing', 'Post-Training Support'],
                3
            ),
            (
                'Support and System Optimization', 'support-maintenance',
                'Continuous maintenance, proactive SLA monitoring, security patching, performance tuning, and issue resolution.',
                'Digital platforms degrade without proactive maintenance, security patches, and database optimizations.',
                ['24/7 Uptime & SLA Monitoring', 'Security Audits & Patch Management', 'Database Query Tuning & Caching', 'Feature Iteration & Upgrades'],
                'Monthly Retainers, Incident Response SLA, Health Audits',
                ['Telemetry & Logging Setup', 'Proactive Health Audits', 'Immediate Incident Response', 'Monthly Performance Optimization'],
                4
            ),
        ]
        for title, slug, summary, prob, caps, eng, proc, order in pillars:
            ServicePillar.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'summary': summary,
                    'problem_addressed': prob,
                    'capabilities': caps,
                    'engagement_types': eng,
                    'delivery_process': proc,
                    'display_order': order,
                    'is_active': True
                }
            )

        # Industry Solutions
        industries = [
            ('Education & E-Learning', 'education', 'Custom learning management systems, student portals, and mobile classrooms.', 1),
            ('Healthcare Systems', 'healthcare', 'Patient records workflow, maternal health tracking, and telemetry dashboards.', 2),
            ('Nonprofits & NGOs', 'nonprofits', 'Donor management, 501(c)(3) governance portals, and program impact trackers.', 3),
            ('SMEs & Commercial Business', 'smes', 'ERP implementation, automated billing, and customer communication pipelines.', 4),
            ('Public Sector & Civic Technology', 'public-sector', 'Transparent public registries, citizen engagement, and open data portals.', 5),
            ('Media & Communications', 'media', 'Digital broadcasting hubs, podcast syndication, and high-conversion content platforms.', 6),
        ]
        for iname, islug, iover, order in industries:
            IndustrySolution.objects.update_or_create(
                slug=islug,
                defaults={'name': iname, 'overview': iover, 'common_challenges': 'Fragmented systems and manual data silos.', 'display_order': order}
            )

        # Project Case Studies
        projects = [
            (
                'TIIPE Digital Platform & Mobile Ecosystem', 'tiipe-platform-blueprint',
                'The Impact Institute for Public Education', 'Nonprofit Education', 'in_development',
                'TIIPE needed a multi-tenant digital portal to support tutoring matching, 501(c)(3) donations, and health literacy.',
                'Designed a multi-tenant Django backend with schema isolation and cross-platform Flutter mobile applications.',
                'Unified Web Portal and iOS/Android Mobile App with real-time video tutoring and Stripe donation ledger.',
                ['Django 5.1', 'Django REST Framework', 'PostgreSQL Schemas', 'Flutter', 'Celery', 'Stripe'],
                'Trained volunteer coordinators and staff on administrative dashboard operations.',
                'Platform MVP ready to onboard 2,000 learners and 500 mentors.',
                True
            ),
            (
                'Enterprise Multi-Channel Billing & Invoicing System', 'enterprise-billing-system',
                'Apex Logistics International', 'SMEs & Commercial Business', 'delivered',
                'Manual paper invoicing caused delays and payment reconciliation errors.',
                'Implemented automated Stripe & Paystack integration with PDF invoice generation and webhook accounting.',
                'Centralized accounting portal with real-time payment reconciliation and automatic client receipts.',
                ['Django', 'PostgreSQL', 'Redis', 'Stripe API', 'React'],
                'Conducted 3 live training sessions for finance and billing operations staff.',
                'Reduced invoice processing turnaround time by 80%.',
                True
            )
        ]
        for ptitle, pslug, pclient, pind, pstat, pchall, papp, psol, ptech, ptrain, pout, pfeat in projects:
            ProjectCaseStudy.objects.update_or_create(
                slug=pslug,
                defaults={
                    'title': ptitle,
                    'client_name': pclient,
                    'industry': pind,
                    'status': pstat,
                    'challenge': pchall,
                    'approach': papp,
                    'solution': psol,
                    'technology_stack': ptech,
                    'training_and_adoption': ptrain,
                    'outcomes_achieved': pout,
                    'is_featured': pfeat
                }
            )

        # Training Courses & Cohorts
        courses = [
            (
                'Fullstack Web & Mobile Application Engineering', 'fullstack-software-engineering',
                'web_mobile', 'intermediate', 'live_online', 12,
                'Master end-to-end product development with Django, React, PostgreSQL, and Flutter mobile apps.',
                'Aspiring software engineers, computer science graduates, and junior developers.',
                ['Production Django & DRF Architectures', 'React Web Applications with State Management', 'Cross-Platform Flutter Mobile Apps', 'Docker & Cloud Deployment'],
                350.00, 'USD'
            ),
            (
                'Data Analytics, Data Engineering & Applied AI', 'data-ai-engineering',
                'data_ai', 'intermediate', 'live_online', 10,
                'Hands-on data pipelines, SQL modeling, machine learning workflows, and generative AI integrations.',
                'Data analysts, engineers, and professionals seeking modern AI skill sets.',
                ['Advanced PostgreSQL & Analytics Modeling', 'Python Data Pipelines with Pandas & Celery', 'LLM Integrations & Vector Embeddings', 'Interactive Business Intelligence Dashboards'],
                400.00, 'USD'
            ),
            (
                'Cloud Infrastructure, DevOps & Containerization', 'cloud-devops-engineering',
                'cloud_devops', 'advanced', 'live_online', 8,
                'Learn Docker, Kubernetes, CI/CD automated pipelines, and cloud security architecture.',
                'Developers and sysadmins transitioning to modern cloud engineering.',
                ['Docker Containerization & Multi-Stage Builds', 'Automated CI/CD with GitHub Actions', 'AWS / DigitalOcean Cloud Provisioning', 'Monitoring with Redis, Celery & Sentry'],
                300.00, 'USD'
            ),
            (
                'Digital Literacy & Business Systems Foundations', 'digital-foundations',
                'digital_foundations', 'beginner', 'self_paced', 4,
                'Foundational technology skills, CRM usage, spreadsheet automation, and digital communication.',
                'Students, administrative staff, and business owners seeking digital efficiency.',
                ['Cloud Workspace & Collaboration Tools', 'Spreadsheet Data Organization', 'Customer Relationship Management Basics', 'Cybersecurity Awareness & Data Privacy'],
                150.00, 'USD'
            ),
        ]
        for ctitle, cslug, ccat, clev, cfmt, cdur, csum, caud, cout, cprice, ccurr in courses:
            crs, _ = TrainingCourse.objects.update_or_create(
                slug=cslug,
                defaults={
                    'title': ctitle,
                    'topic_category': ccat,
                    'level': clev,
                    'format': cfmt,
                    'duration_weeks': cdur,
                    'summary': csum,
                    'target_audience': caud,
                    'learning_outcomes': cout,
                    'price_amount': cprice,
                    'price_currency': ccurr,
                    'is_enrollment_open': True
                }
            )
            # Create a cohort
            TrainingCohort.objects.update_or_create(
                course=crs,
                cohort_name='Cohort 2026-Q3',
                defaults={
                    'start_date': datetime.date(2026, 10, 1),
                    'end_date': datetime.date(2026, 12, 20),
                    'schedule_description': 'Tuesdays & Thursdays 6:00 PM - 8:00 PM WAT',
                    'max_capacity': 25,
                    'is_registration_active': True
                }
            )

        # Capability Download
        CapabilityDownload.objects.update_or_create(
            title='Novatrix Corporate Capability Statement & Service Catalog (2026)',
            defaults={
                'document_type': 'Capability Statement',
                'file_url': 'https://thenovatrix.com/downloads/novatrix-capability-statement-2026.pdf',
                'file_size_kb': 1200,
                'is_active': True
            }
        )

        self.stdout.write(self.style.SUCCESS("✓ Novatrix Tenant Data Seeded"))
