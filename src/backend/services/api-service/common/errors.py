class APIError(Exception):
    """Base class for all API errors."""
    status_code = 500
    error_code  = "internal_error"

    def __init__(self, message=None, *, status_code=None, error_code=None, payload=None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code
        self.payload = payload or {}

    def to_dict(self):
        rv = dict(self.payload)
        rv["code"]    = self.error_code
        rv["message"] = self.args[0] if self.args else ""
        return rv

class BadRequestError(APIError):
    status_code = 400
    error_code  = "bad_request"

class NotFoundError(APIError):
    status_code = 404
    error_code  = "not_found"

class ConflictError(APIError):
    status_code = 409
    error_code  = "conflict"

class ForbiddenError(APIError):
    status_code = 403
    error_code  = "forbidden"

class UnauthorizedError(APIError):
    status_code = 401
    error_code  = "unauthorized"

class InternalServerError(APIError):
    status_code = 500
    error_code  = "internal_server_error"

class ServiceUnavailableError(APIError):
    status_code = 503
    error_code  = "service_unavailable"
