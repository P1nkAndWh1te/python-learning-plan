import os


def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        print("DEEPSEEK_API_KEY is not set.")
        print('PowerShell temporary setup: $env:DEEPSEEK_API_KEY="your_api_key"')
        return

    masked = api_key[:7] + "..." + api_key[-4:] if len(api_key) >= 12 else "***"
    print("DEEPSEEK_API_KEY is set.")
    print(f"Masked value: {masked}")


if __name__ == "__main__":
    main()
