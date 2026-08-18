#!/usr/bin/env python3
"""Serve this folder on localhost with a simple HTTP server."""

import argparse
import http.server
import os
import socket
import socketserver
import webbrowser
from functools import partial


def main() -> None:
    parser = argparse.ArgumentParser(description="Host this folder on localhost.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Port to listen on (default: 8000)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open a browser automatically",
    )
    args = parser.parse_args()

    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)

    handler = partial(http.server.SimpleHTTPRequestHandler, directory=root)

    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    with ReusableTCPServer(("0.0.0.0", args.port), handler) as httpd:
        url = f"http://localhost:{args.port}"

        print(f"Serving {root}")
        print(f"Local:   {url}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                network_url = f"http://{s.getsockname()[0]}:{args.port}"
            print(f"Network: {network_url}")
        except OSError:
            print("Network: unavailable (use localhost on this machine)")
        print("Press Ctrl+C to stop.")

        if not args.no_browser:
            webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()
