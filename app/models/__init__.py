"""Data models for BRD Generator API.

This package contains Pydantic models for request validation and
response serialization.
"""

from .request import BRDRequest
from .response import BRDResponse, Requirement, Stakeholder

__all__ = ['BRDRequest', 'BRDResponse', 'Requirement', 'Stakeholder']
