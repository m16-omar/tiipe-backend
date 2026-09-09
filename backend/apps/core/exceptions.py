from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Standardized JSON exception handler for API responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            'success': False,
            'status_code': response.status_code,
            'error_type': exc.__class__.__name__,
            'detail': response.data
        }
        response.data = custom_data
    else:
        # Unhandled server error
        custom_data = {
            'success': False,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'error_type': 'InternalServerError',
            'detail': str(exc) if str(exc) else 'An unexpected internal server error occurred.'
        }
        response = Response(custom_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
