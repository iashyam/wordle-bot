from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class APIException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class NotFoundException(APIException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404)

class ValidationException(APIException):
    def __init__(self, message: str = "Validation error"):
        super().__init__(message=message, status_code=422)

class ServerErrorException(APIException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message=message, status_code=500)

async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "status_code": exc.status_code},
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Something went wrong on the server.", "status_code": 500},
    )

def register_exception_handlers(app):
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
