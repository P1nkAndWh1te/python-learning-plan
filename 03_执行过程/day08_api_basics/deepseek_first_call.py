import os

from openai import OpenAI, OpenAIError, RateLimitError


def main():
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise RuntimeError(
            "DEEPSEEK_API_KEY is not set. Set it in PowerShell before running this script."
        )

    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "你是一个擅长给零基础学生讲编程概念的老师。"},
                {"role": "user", "content": "用三句话解释：什么是 API？请用零基础能听懂的中文回答。"},
            ],
            stream=False,
        )
    except RateLimitError as exc:
        print("DeepSeek request reached the server, but the account has no available quota.")
        print("Check balance, quota, or rate limits in the DeepSeek platform.")
        print(f"Error: {exc}")
        return
    except OpenAIError as exc:
        print("DeepSeek request failed.")
        print(f"Error: {exc}")
        return

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
