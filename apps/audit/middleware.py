"""Audit Trail Thread-Local Middleware."""
import threading

_thread_locals = threading.local()

def get_current_request():
    """Retrieve the current HTTP request from thread-local storage."""
    return getattr(_thread_locals, 'request', None)

def get_current_user():
    """Retrieve the authenticated user from thread-local request."""
    req = get_current_request()
    if req and hasattr(req, 'user') and req.user.is_authenticated:
        return req.user
    return None

def get_client_ip(request):
    """Safely extracts client IP address from HTTP request."""
    if not request:
        return '127.0.0.1'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    return ip

class AuditMiddleware:
    """Middleware capturing request context for audit trails."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        _thread_locals.request = None
        return response
