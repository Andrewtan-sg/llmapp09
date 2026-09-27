"""Fail safely when required CI environment variables are not configured."""

import os
import sys


def main() -> int:
    required = sys.argv[1:]
    if not required:
        print("No environment variables were supplied for validation.")
        return 2

    missing = [name for name in required if not os.getenv(name, "").strip()]
    if missing:
        print("Missing required GitHub Actions configuration:")
        for name in missing:
            print(f"- {name}")
        return 1

    print("Required GitHub Actions configuration is present:")
    for name in required:
        print(f"- {name}=<SET>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
