from django.db.models import Sum, Count
from django.utils import timezone
from apps.users.models import CustomUser, UserProfile, TenantMembership
from apps.core.models import ClientTenant, Domain
from django_tenants.utils import schema_context

def dashboard_callback(request, context):
    """
    Computes multi-tenant telemetry and operational KPIs for the Tailwind Unfold Master Admin Dashboard.
    """
    try:
        total_users = CustomUser.objects.count()
        total_mentors = UserProfile.objects.filter(background_check_status='verified').count()
        total_tenants = ClientTenant.objects.count()
        active_tenants = ClientTenant.objects.filter(is_active=True).count()
        
        # Telemetry containers
        tiipe_data = {
            'programs_count': 0,
            'sessions_count': 0,
            'completed_sessions': 0,
            'donations_count': 0,
            'total_donated': 0.0,
            'recent_donations': [],
            'recent_sessions': [],
        }
        
        novatrix_data = {
            'pillars_count': 0,
            'case_studies_count': 0,
            'courses_count': 0,
            'cohorts_count': 0,
            'inquiries_count': 0,
            'open_tickets': 0,
            'recent_inquiries': [],
            'recent_tickets': [],
        }
        
        # Pull TIIPE Tenant Data
        try:
            with schema_context('tiipe'):
                from apps.tiipe_lms.models import Program, MentorshipSession
                from apps.payments.models import Donation
                
                tiipe_data['programs_count'] = Program.objects.filter(is_active=True).count()
                tiipe_data['sessions_count'] = MentorshipSession.objects.count()
                tiipe_data['completed_sessions'] = MentorshipSession.objects.filter(status='completed').count()
                
                donations_qs = Donation.objects.all()
                tiipe_data['donations_count'] = donations_qs.count()
                donations_sum = donations_qs.filter(status='succeeded').aggregate(total=Sum('amount'))['total']
                tiipe_data['total_donated'] = float(donations_sum or 0.0)
                
                tiipe_data['recent_donations'] = list(donations_qs.order_by('-created_at')[:5].values(
                    'donor_name', 'amount', 'fund_allocation', 'frequency', 'status', 'created_at'
                ))
                tiipe_data['recent_sessions'] = list(MentorshipSession.objects.order_by('-start_time')[:5].values(
                    'subject_topic', 'status', 'start_time'
                ))
        except Exception as e:
            print(f"TIIPE telemetry collection note: {e}")

        # Pull Novatrix Tenant Data
        try:
            with schema_context('novatrix'):
                from apps.novatrix_services.models import ServicePillar, ProjectCaseStudy, TrainingCourse, TrainingCohort, ProjectInquiry, SupportTicket
                
                novatrix_data['pillars_count'] = ServicePillar.objects.filter(is_active=True).count()
                novatrix_data['case_studies_count'] = ProjectCaseStudy.objects.count()
                novatrix_data['courses_count'] = TrainingCourse.objects.count()
                novatrix_data['cohorts_count'] = TrainingCohort.objects.filter(is_registration_active=True).count()
                novatrix_data['inquiries_count'] = ProjectInquiry.objects.filter(is_reviewed=False).count()
                novatrix_data['open_tickets'] = SupportTicket.objects.exclude(status='resolved').count()
                
                novatrix_data['recent_inquiries'] = list(ProjectInquiry.objects.order_by('-created_at')[:5].values(
                    'client_name', 'organization', 'service_required', 'is_reviewed', 'created_at'
                ))
                novatrix_data['recent_tickets'] = list(SupportTicket.objects.order_by('-created_at')[:5].values(
                    'client_name', 'subject', 'priority', 'status', 'created_at'
                ))
        except Exception as e:
            print(f"Novatrix telemetry collection note: {e}")

        context.update({
            'total_users': total_users,
            'total_mentors': total_mentors,
            'active_tenants': active_tenants,
            'total_tenants': total_tenants,
            'tiipe_stats': tiipe_data,
            'novatrix_stats': novatrix_data,
            'system_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        })
    except Exception as err:
        print(f"Error in dashboard_callback: {err}")

    return context
