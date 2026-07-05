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

from .client import SHCClient, SHCError, ProvisioningStuckError, InsufficientCreditError
from .transport import resolve_transport
from .sizes import SIZE_MAP, resolve_size, resolve_specs, list_sizes

__all__ = [
    "SHCClient",
    "SHCError",
    "ProvisioningStuckError",
    "InsufficientCreditError",
    "SHCTransport",
    "create_client",
    "SIZE_MAP",
    "resolve_size",
    "resolve_specs",
    "list_sizes",
    "VM",
    "Balance",
    "CatalogPackage",
    "SupportTicket",
]

# Re-export Protocol for type checking
from .transport import SHCTransport
from .models import VM, Balance, CatalogPackage, SupportTicket


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
    import os

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
        from .console import ConsoleSession, ConsoleError
        return locals()[name]
    if name in ("VMBootstrap",):
        from .bootstrap import VMBootstrap
        return VMBootstrap
    if name == "SHCMCPClient":
        from .mcp_client import SHCMCPClient
        return SHCMCPClient
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
