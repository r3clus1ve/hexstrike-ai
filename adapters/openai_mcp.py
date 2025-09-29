# --- wstaw na górę pliku hexstrike_mcp.py (importy)
import os
import logging

logger = logging.getLogger(__name__)

# --- helper funkcja (w dowolnym miejscu przed użyciem)
def prepare_tools_payload(all_tools):
    """
    Przytnij listę narzędzi przed wysłaniem do klienta MCP.
    all_tools: lista dictów lub stringów reprezentujących tools.
    Zwraca listę (max HEXSTRIKE_MAX_TOOLS elementów). Jeśli obcięto,
    dopisuje element informacyjny na końcu.
    """
    try:
        max_tools = int(os.getenv("HEXSTRIKE_MAX_TOOLS", "128"))
    except Exception:
        max_tools = 128

    total = len(all_tools)
    if total <= max_tools:
        logger.debug("prepare_tools_payload: total tools=%d <= max=%d", total, max_tools)
        return all_tools

    truncated = all_tools[:max_tools]
    # Dodaj informację, że lista została obcięta (możesz zmienić strukturę tego elementu)
    truncated.append({
        "name": f"...+{total - max_tools} more",
        "note": "truncated_by_server",
        "_meta_truncated_count": total - max_tools
    })
    logger.warning("Tools list truncated: original=%d, sent=%d (max=%d)", total, total - (total - max_tools), max_tools)
    return truncated

# --- przykład użycia: zamiast
# payload["tools"] = get_installed_tools()
# użyj:
all_tools = get_installed_tools()   # <-- oryginalna funkcja zwracająca listę narzędzi
payload["tools"] = prepare_tools_payload(all_tools)
# dalej: send payload do klienta MCP
