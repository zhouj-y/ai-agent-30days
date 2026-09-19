from dotenv import load_dotenv
import os
import json
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

#定义我们要给AI用的工具
def get_price(product_name):
    products = {
        "A产品": 1999,
        "B产品": 3999,
        "C产品": 899
    }
    if product_name in products:
        return products[product_name]
    else:
        return "抱歉，没找到这个产品"

#告诉AI 这个工具长什么样
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "查询产品价格。输入产品名称，返回价格。",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "产品的名称，例如“A产品、B产品"
                    }
                },
                "required": ["product_name"]
            }
        }
    }
]

#用户提问
messages = [
    {"role": "user", "content": "请问A产品多少钱？帮我查一下。"}
]

print("正在询问AI...")

#第一次请求：把工具说明书一起发给AI
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,
    tool_choice="auto"  #让ai自己决定用不用工具
)

message = response.choices[0].message

#检查AI 是不是要调用工具
if messages.tool_calls:
    print("AI 决定调用工具！")
    tool_call = messages.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    print(f"AI 调用的函数是：{function_name}")
    print(f"AI 传的参数是：{arguments}")

    #我们要帮AI  去执行这个函数

    if function_name == "get_price":
        result = get_price(arguments["product_name"])
        print(f"函数执行结果: {result}")

        #把函数结果告诉AI 让AI总结回复
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id":tool_call.id,
            "content": str(result)
        })
        #第二次请求：发结果给AI 要最终回复
        second_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages

        )
        print("\n===AI 最终回复===")
        print(second_response.choices[0].message.content)
else:
    print("AI 没有调用工具，直接回复：")
    print(message.content)