import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.windows import (
    get_time,
    get_date,
    open_website,
    open_calculator,
    open_notepad
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("OPENAI_MODEL")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Узнать текущее время.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_date",
            "description": "Узнать сегодняшнюю дату.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_calculator",
            "description": "Открыть калькулятор Windows.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_notepad",
            "description": "Открыть Блокнот Windows.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Открыть сайт в браузере после подтверждения пользователя.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Полный адрес сайта с https://"
                    }
                },
                "required": ["url"],
                "additionalProperties": False
            }
        }
    }
]


def execute_tool(name, arguments):
    if name == "get_time":
        return get_time()

    if name == "get_date":
        return get_date()

    if name == "open_calculator":
        return open_calculator()

    if name == "open_notepad":
        return open_notepad()

    if name == "open_website":
        url = arguments["url"]

        print(f"\nNOVA хочет открыть сайт: {url}")
        confirmation = input("Разрешить? (да/нет): ").strip().lower()

        if confirmation not in ("да", "д", "yes", "y"):
            return "Пользователь отменил открытие сайта."

        return open_website(url)

    return "Неизвестный инструмент."


def ask_ai(message: str, history: list) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "Ты — NOVA, ИИ-помощник для Windows. "
                "Отвечай на русском языке. "
                "Если пользователь просит узнать время или дату, "
                "используй соответствующий инструмент. "
                "Если просит открыть калькулятор или блокнот, "
                "используй соответствующий инструмент. "
                "Не утверждай, что выполнила действие, "
                "если инструмент его не выполнил."
            )
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": message
    })

    for _ in range(4):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            parallel_tool_calls=False
        )

        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            return assistant_message.content or "Не удалось получить ответ."

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name

            try:
                arguments = json.loads(tool_call.function.arguments)
                result = execute_tool(name, arguments)
            except Exception as error:
                result = f"Ошибка выполнения инструмента: {error}"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    return "Достигнут лимит вызовов инструментов."