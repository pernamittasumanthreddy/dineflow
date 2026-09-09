"""Production Request Telemetry, Performance Profiling & Security Headers Middleware."""
import time
import logging

logger = logging.getLogger(__name__)

class RequestTimingMiddleware:
    """
    Measures HTTP request execution duration and adds an X-Response-Time-Ms header.
    Emits a warning log for slow queries/views exceeding 500 milliseconds.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()
        
        response = self.get_response(request)
        
        duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        response['X-Response-Time-Ms'] = str(duration_ms)
        
        if duration_ms > 500.0:
            logger.warning(f"SLOW REQUEST: {request.method} {request.path} took {duration_ms}ms")
            
        return response

class SecurityHeaderMiddleware:
    """
    Injects enterprise security headers on all HTTP responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response
