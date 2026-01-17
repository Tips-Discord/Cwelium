import os
import sys
import tls_client
import websocket

from .files import Files
from .console import Render
from .raider import Raider
from .menu import Menu
from .config import C, PROXY_ENABLED

console = Render()


def setup_tls_session() -> tls_client.Session:
    """Create and configure TLS session with Discord fingerprinting."""
    return tls_client.Session(
        client_identifier="chrome_138",
        random_tls_extension_order=True,
        ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-5-10-11-13-16-18-23-27-35-43-45-51-17613-65037-65281,4588-29-23-24,0",
        h2_settings={
            "HEADER_TABLE_SIZE": 65536,
            "ENABLE_PUSH": 0,
            "INITIAL_WINDOW_SIZE": 6291456,
            "MAX_HEADER_LIST_SIZE": 262144
        },
        h2_settings_order=[
            "HEADER_TABLE_SIZE",
            "ENABLE_PUSH",
            "INITIAL_WINDOW_SIZE",
            "MAX_HEADER_LIST_SIZE"
        ],
        supported_signature_algorithms=[
            "ecdsa_secp256r1_sha256",
            "rsa_pss_rsae_sha256",
            "rsa_pkcs1_sha256",
            "ecdsa_secp384r1_sha384",
            "rsa_pss_rsae_sha384",
            "rsa_pkcs1_sha384",
            "rsa_pss_rsae_sha512",
            "rsa_pkcs1_sha512"
        ],
        supported_versions=["TLS_1_3", "TLS_1_2"],
        key_share_curves=["GREASE", "X25519MLKEM768", "X25519", "secp256r1", "secp384r1"],
        pseudo_header_order=[":method", ":authority", ":scheme", ":path"],
        connection_flow=15663105,
        priority_frames=[]
    )


def initialize_application():
    """Initialize files, folders, and config."""
    try:
        Files.initialize()
        console.log("Success", C["green"], False, "Initialized files and folders")
    except Exception as e:
        console.log("Failed", C["red"], False, f"Initialization error: {str(e)}")
        sys.exit(1)


def load_resources():
    """Load tokens and proxies from files."""
    tokens = Files.load_tokens()
    proxies = Files.load_proxies()

    if not tokens:
        console.log("Warning", C["yellow"], False, "No tokens found in data/tokens.txt")
        console.log("Info", C["yellow"], False, "Please add tokens to data/tokens.txt and restart")

    console.log("Info", C["cyan"], False, f"Loaded {len(tokens)} tokens and {len(proxies)} proxies")

    return tokens, proxies


def create_raider(session: tls_client.Session):
    """Initialize the Raider instance."""
    try:
        raider = Raider(session)
        console.log("Success", C["green"], False, "Raider initialized successfully")
        return raider
    except Exception as e:
        console.log("Failed", C["red"], False, f"Failed to initialize Raider: {str(e)}")
        sys.exit(1)


def main():
    """Main application entry point."""
    # Clear screen and show ASCII art
    console.clear()
    console.render_ascii()

    # Initialize everything
    initialize_application()
    
    # Load resources
    tokens, proxies = load_resources()
    
    if not tokens:
        input("\nPress Enter to exit...")
        return

    # Setup TLS session
    try:
        session = setup_tls_session()
        console.log("Success", C["green"], False, "TLS session configured")
    except Exception as e:
        console.log("Failed", C["red"], False, f"TLS session error: {str(e)}")
        input("\nPress Enter to exit...")
        return

    # Configure proxies globally if enabled
    if PROXY_ENABLED and proxies:
        console.log("Info", C["cyan"], False, f"Proxy mode enabled with {len(proxies)} proxies")
        session.proxies_list = proxies  # Store for per-thread assignment
    else:
        session.proxies_list = []
        console.log("Info", C["cyan"], False, "Proxy mode disabled")

    # Create core components
    raider = create_raider(session)
    
    # Create and run menu
    menu = Menu(raider, tokens, proxies)
    
    try:
        console.log("Info", C["cyan"], False, "Starting Cwelium menu...")
        menu.run()
    except KeyboardInterrupt:
        console.clear()
        console.log("Info", C["yellow"], False, "Interrupted by user")
    except Exception as e:
        console.log("Failed", C["red"], False, f"Menu error: {str(e)}")
    finally:
        console.clear()
        print(f"{C['light_blue']}Cwelium shutdown complete. Goodbye.{C['white']}")
        sys.exit(0)


if __name__ == "__main__":
    main()