from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class ClientTenant(TenantMixin):
    """
    Tenant representation for PostgreSQL schema isolation.
    Tenants represent brands (TIIPE - Parent, Novatrix - Subsidiary).
    """
    BRAND_CHOICES = (
        ('public', 'Public Master Routing Gateway'),
        ('tiipe', 'The Impact Institute for Public Education (Parent)'),
        ('novatrix', 'Novatrix Technology & Workforce (Subsidiary)'),
    )
    
    name = models.CharField(max_length=150, help_text="Company / Brand display name")
    brand_type = models.CharField(max_length=30, choices=BRAND_CHOICES, default='public')
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    primary_color = models.CharField(max_length=20, default='#1E3A8A')
    accent_color = models.CharField(max_length=20, default='#D97706')
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # Automatically create the PostgreSQL schema on tenant save
    auto_create_schema = True

    def __str__(self):
        return f"{self.name} ({self.schema_name})"


class Domain(DomainMixin):
    """
    Domain routing model for mapping hostnames to tenant schemas.
    """
    pass
