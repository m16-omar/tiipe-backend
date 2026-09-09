import os
from django.conf import settings
from django.db import connection
from storages.backends.s3boto3 import S3Boto3Storage

class TenantMediaStorage(S3Boto3Storage):
    """
    Multi-tenant aware S3 / Spaces storage backend.
    Prefixes file keys with the current tenant schema name (e.g. 'tiipe/media/...' or 'novatrix/media/...').
    """
    def _clean_name(self, name):
        schema_name = getattr(connection, 'schema_name', 'public')
        return os.path.join(schema_name, 'media', name)

    def url(self, name, parameters=None, expire=None, http_method=None):
        return super().url(name, parameters, expire, http_method)
