"""Custom exceptions for the BRD Generator Backend API.

This module defines domain-specific exceptions for clear error handling
throughout the application.
"""


class BRDGenerationError(Exception):
    """Raised when BRD generation fails.
    
    This exception is raised when the BRD generation process encounters
    an error that prevents successful completion, such as invalid OpenAI
    responses or processing failures.
    """
    pass


class OpenAIServiceError(Exception):
    """Raised when OpenAI API communication fails.
    
    This exception is raised when there are issues communicating with
    the OpenAI API, including authentication failures, rate limiting,
    network errors, or service unavailability.
    """
    pass


class ValidationError(Exception):
    """Raised when input validation fails.
    
    This exception is raised when request validation fails, such as
    missing required fields or invalid data formats.
    """
    pass
