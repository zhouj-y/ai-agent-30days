import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有读取到 DEEPSEEK_API_KEY,请检查 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system",
            "content": "你是一个销售话术助手，回答要具体、可直接使用。"
        },
        {
            "role": "user",
            "content": "客户说：你们产品太贵了。请给我3种回复话术。"
        }
    ],
    temperature=0.7
)

print(response.choices[0].message.content)