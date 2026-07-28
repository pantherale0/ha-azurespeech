"""Exception definitions for Azure Speech API client."""


class AzureSpeechApiClientError(Exception):
    """Exception raised for general Azure Speech API errors."""


class AzureSpeechApiClientCommunicationError(AzureSpeechApiClientError):
    """Exception raised for network communication or timeout errors."""


class AzureSpeechApiClientAuthenticationError(AzureSpeechApiClientError):
    """Exception raised for authentication errors (HTTP 401/403)."""


class AzureSpeechApiClientRateLimitError(AzureSpeechApiClientError):
    """Exception raised for rate limiting errors (HTTP 429)."""

    def __init__(self, retry_after: int | None = None) -> None:
        """Initialize the rate limit error with optional retry after delay."""
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")
        self.retry_after = retry_after
