class CacheNotConfiguredError(Exception):
    """Raised when the cache is not configured in settings."""

    def __init__(self, message="Cache is not configured in your settings.py"):
        self.message = message
        super().__init__(self.message)
