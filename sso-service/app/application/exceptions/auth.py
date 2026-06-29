from app.application.exceptions.base import AppError


class UsernameAlreadyExistsError(AppError):
    code = "USERNAME_ALREADY_EXISTS"
    message = "Username already exists"


class InvalidCredentialsError(AppError):
    code = "INVALID_CREDENTIALS"
    message = "Invalid username or password"


class TokenRequiredError(AppError):
    code = "TOKEN_REQUIRED"
    message = "Authorization token is required"


class InvalidTokenError(AppError):
    code = "INVALID_TOKEN"
    message = "Invalid or expired token"
