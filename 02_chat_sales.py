from dotenv import load_dotenv
import os
import json
from datetime import datetime
from openai import OpenAI


load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有读到 DEEPSEEK_API_KEY,请检查 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

#这里的messages就是AI的“记忆”
messages = [
    {
        "role":"system",
        "content":(
            "你是一个销售话术助手。"
            "你擅长把客户异议转化成跟进话术。"
            "回答要具体、分点、可直接复制使用。"
            "每次回答后，追问一个有助于推进销售的问题。"
        )
    }
]

def save_chat(messages):
    filename = f"chet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(messages, f , ensure_ascii=False, indent=2)
    print(f"\n对话已保存到: {filename}")

print("销售话术助手已启动。输入 exit 退出。\n")

while True:
    user_input = input("你：").strip()

    if user_input.lower() in ["exit", "quit", "退出"]:
        save_chat(messages)
        print("再见")
        break

    if not user_input:
        continue

    #把用户的输入加入记忆
    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )

        answer = response.choices[0].message.content
        print(f"\nAI: {answer}\n")

        #把AI的回答也加入记忆
        messages.append({
            "role": "assistant",
            "content": answer
        })
    except Exception as e:
        print(f"\n出错了：{e}\n")