import platform
import requests
import os
import sys
from pathlib import Path


def download_sqlite_extensions():
    arch = platform.machine()
    system = platform.system().lower()
    base_url = "https://github.com/asg017/sqlite-vss/releases/download/v0.1.2"

    # Define the target directory within the user's home directory
    target_dir = Path.home() / ".semantify" / "native_libs"
    os.makedirs(target_dir, exist_ok=True)

    # Define URLs for downloading based on the system and architecture
    if arch == "arm64" and system == "darwin":
        filenames = {
            "vector0.dylib": f"{base_url}/sqlite-vss-v0.1.2-deno-darwin-aarch64.vector0.dylib",
            "vss0.dylib": f"{base_url}/sqlite-vss-v0.1.2-deno-darwin-aarch64.vss0.dylib"
        }
    elif arch == "x86_64" and system == "darwin":
        filenames = {
            "vector0.dylib": f"{base_url}/sqlite-vss-v0.1.2-deno-darwin-x86_64.vector0.dylib",
            "vss0.dylib": f"{base_url}/sqlite-vss-v0.1.2-deno-darwin-x86_64.vss0.dylib"
        }
    elif arch == "x86_64" and system == "linux":
        filenames = {
            "vector0.so": f"{base_url}/sqlite-vss-v0.1.2-deno-linux-x86_64.vector0.so",
            "vss0.so": f"{base_url}/sqlite-vss-v0.1.2-deno-linux-x86_64.vss0.so"
        }
    else:
        print(f"Unsupported architecture or platform: {arch} on {system}")
        sys.exit(1)

    for local_filename, download_url in filenames.items():
        file_path = target_dir / local_filename
        if not file_path.exists():
            print(f"Downloading {download_url} to {file_path}")
            response = requests.get(download_url)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print(f"Failed to download {local_filename}.")
                sys.exit(1)
