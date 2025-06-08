import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from utils.logger import request_id_var


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        token = request_id_var.set(request_id)
        try:
            response = await call_next(request)
        finally:
            request_id_var.reset(token)  # clean up context after request
        response.headers["X-Request-ID"] = request_id
        return response
