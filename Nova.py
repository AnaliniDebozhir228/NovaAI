from core.brain import ask_ai
from core.memory import Memory


def main():
    memory = Memory()

    print("=" * 40)
    print("       NOVA — AI ASSISTANT")
    print("=" * 40)
    print("NOVA запущена. История диалога сохраняется.")
    print("Напиши «выход», чтобы завершить.\n")

    while True:
        message = input("Ты: ").strip()

        if message.lower() in ("выход", "exit", "quit"):
            print("NOVA: До встречи!")
            break

        if not message:
            continue

        try:
            history = memory.history(limit=20)
            answer = ask_ai(message, history)

            memory.save("user", message)
            memory.save("assistant", answer)

            print(f"\nNOVA: {answer}\n")

        except Exception as error:
            print(f"\nОшибка: {error}\n")


if __name__ == "__main__":
    main()