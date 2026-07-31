"""
Sovereign Hybrid Compute (SHC) API client.

Dual-transport client for SHC: REST v2 (default) or MCP Streamable HTTP.

    from shc_toolkit import SHCClient, create_client

    # Backward-compatible (always REST):
    c = SHCClient()
    vms = c.list_vms()

    # Transport-aware factory:
    c = create_client(transport="auto")  # MCP if available, else REST
    c = create_client(transport="mcp")   # force MCP
    c = create_client(transport="rest")  # force REST
"""

from .client import (
    InsufficientCreditError,
    ProvisioningStuckError,
    SHCAuthError,
    SHCClient,
    SHCConfirmationRequiredError,
    SHCError,
    SHCNotFoundError,
    SHCRateLimitError,
    SHCServerError,
)
from .sizes import SIZE_MAP, list_sizes, resolve_size, resolve_specs
from .transport import resolve_transport

__all__ = [
    "SIZE_MAP",
    "VM",
    "Balance",
    "CatalogPackage",
    "InsufficientCreditError",
    "ProvisioningStuckError",
    "SHCAuthError",
    "SHCClient",
    "SHCConfirmationRequiredError",
    "SHCError",
    "SHCNotFoundError",
    "SHCRateLimitError",
    "SHCServerError",
    "SHCTransport",
    "SupportTicket",
    "create_client",
    "list_sizes",
    "resolve_size",
    "resolve_specs",
]

# Re-export Protocol for type checking
from .models import VM, Balance, CatalogPackage, SupportTicket
from .transport import SHCTransport


def create_client(
    api_key: str | None = None,
    *,
    transport: str | None = None,
    **kwargs,
):
    """Create an SHC client with automatic transport selection.

    Args:
        api_key: SHC API key (shc_live_...). Falls back to SHC_API_KEY env var.
        transport: 'rest', 'mcp', or 'auto' (default). If None, reads
                   SHC_TRANSPORT env var, defaults to 'rest'.
        **kwargs: Transport-specific options (e.g. base_url for REST).

    Returns:
        SHCClient (REST) or SHCMCPClient (MCP), both implementing SHCTransport.

    Raises:
        ImportError: If transport='mcp' but the 'mcp' package is not installed.
        ValueError: If no API key is available.
    """

    resolved = resolve_transport(transport)

    if resolved == "mcp":
        try:
            from .mcp_client import SHCMCPClient
        except ImportError as e:
            raise ImportError(
                "MCP transport requires the 'mcp' package. "
                "Install with: pip install shc-toolkit[mcp] "
                f"(original error: {e})"
            ) from e
        return SHCMCPClient(api_key=api_key, **kwargs)

    return SHCClient(api_key=api_key, **kwargs)


# Console and bootstrap modules are optional (require playwright).
# Import lazily so `pip install shc-toolkit` works without playwright.
def __getattr__(name):
    if name in ("ConsoleSession", "ConsoleError"):
        from .console import ConsoleError, ConsoleSession  # noqa: F401

        return locals()[name]
    if name in ("VMBootstrap",):
        from .bootstrap import VMBootstrap

        return VMBootstrap
    if name == "SHCMCPClient":
        from .mcp_client import SHCMCPClient

        return SHCMCPClient
    if name in ("CloudflareTunnel", "ConsoleShell", "TunnelError", "ensure_ssh_access"):
        from .tunnel import (
            CloudflareTunnel,
            ConsoleShell,
            TunnelError,
            ensure_ssh_access,
        )

        return {
            "CloudflareTunnel": CloudflareTunnel,
            "ConsoleShell": ConsoleShell,
            "TunnelError": TunnelError,
            "ensure_ssh_access": ensure_ssh_access,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
