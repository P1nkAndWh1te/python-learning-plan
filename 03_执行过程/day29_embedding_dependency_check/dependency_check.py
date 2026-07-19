from __future__ import annotations

import importlib.util
import platform
import subprocess
import sys


sys.stdout.reconfigure(encoding="utf-8")

PACKAGES = [
    "chromadb",
    "onnxruntime",
    "torch",
    "sentence_transformers",
    "transformers",
]


def package_available(import_name: str) -> bool:
    return importlib.util.find_spec(import_name) is not None


def run_command(command: list[str]) -> str:
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = result.stdout.strip()
    if result.stderr.strip():
        output = f"{output}\n{result.stderr.strip()}".strip()
    return output


def main() -> None:
    print("Day29 embedding dependency check")
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print()

    print("Installed package import check:")
    for package in PACKAGES:
        status = "installed" if package_available(package) else "missing"
        print(f"- {package}: {status}")

    print()
    print("Latest visible versions from pip index:")
    for package_name in ("sentence-transformers", "torch"):
        first_line = run_command(
            [sys.executable, "-m", "pip", "index", "versions", package_name]
        ).splitlines()[0]
        print(f"- {first_line}")

    print()
    print("Decision:")
    print(
        "Do not install sentence-transformers automatically. "
        "It brings a larger local model stack, so install only after confirmation."
    )


if __name__ == "__main__":
    main()

