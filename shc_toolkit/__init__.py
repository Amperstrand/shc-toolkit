"""
Sovereign Hybrid Compute (SHC) API client.
"""

from .client import SHCClient, SHCError, ProvisioningStuckError

__all__ = [
    "SHCClient",
    "SHCError",
    "ProvisioningStuckError",
]

# Console and bootstrap modules are optional (require playwright).
# Import lazily so `pip install shc-toolkit` works without playwright.
def __getattr__(name):
    if name in ("ConsoleSession", "ConsoleError"):
        from .console import ConsoleSession, ConsoleError
        return locals()[name]
    if name in ("VMBootstrap",):
        from .bootstrap import VMBootstrap
        return VMBootstrap
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
