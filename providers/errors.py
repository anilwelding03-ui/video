class ProviderError(RuntimeError):
    """Base class for provider initialization/runtime issues."""


class ProviderNotConfiguredError(ProviderError):
    """Raised by optional local adapters when dependencies/config are missing."""
