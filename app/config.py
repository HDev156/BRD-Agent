"""Configuration management for the BRD Generator Backend API.

This module handles loading and validating configuration from environment variables.
"""

from functools import lru_cache
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Attributes:
        openai_api_key: OpenAI API key for authentication (required)
        openai_model: OpenAI model to use for BRD generation (default: gpt-4)
        openai_base_url: Base URL for OpenAI-compatible API (optional, for Groq/other providers)
        port: Server port number (default: 8000)
        dataset_mode_enabled: Enable dataset-based ingestion (default: False)
        email_dataset_path: Path to email dataset file
        meeting_dataset_path: Path to meeting dataset directory
        max_dataset_emails: Maximum emails to load from dataset (default: 1000)
        max_dataset_meetings: Maximum meetings to load from dataset (default: 100)
        dataset_sample_size: Sample size for BRD generation (default: 50)
    """
    
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key for authentication"
    )
    openai_model: str = Field(
        default="gpt-4",
        description="OpenAI model to use for BRD generation"
    )
    openai_base_url: Optional[str] = Field(
        default=None,
        description="Base URL for OpenAI-compatible API (optional)"
    )
    port: int = Field(
        default=8000,
        description="Server port number"
    )
    
    # Dataset configuration
    dataset_mode_enabled: bool = Field(
        default=False,
        description="Enable dataset-based ingestion"
    )
    email_dataset_path: Optional[str] = Field(
        default=None,
        description="Path to email dataset CSV file"
    )
    meeting_dataset_path: Optional[str] = Field(
        default=None,
        description="Path to meeting dataset directory"
    )
    max_dataset_emails: int = Field(
        default=1000,
        description="Maximum emails to load from dataset"
    )
    max_dataset_meetings: int = Field(
        default=100,
        description="Maximum meetings to load from dataset"
    )
    dataset_sample_size: int = Field(
        default=50,
        description="Sample size for BRD generation from dataset"
    )
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


@lru_cache()
def get_settings() -> Settings:
    """Get application settings singleton.
    
    This function uses lru_cache to ensure settings are loaded only once
    and reused across the application.
    
    Returns:
        Settings: Application settings instance
        
    Raises:
        ValidationError: If required environment variables are missing or invalid
    """
    return Settings()
