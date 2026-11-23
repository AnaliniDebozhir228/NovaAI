import subprocess
import webbrowser
from datetime import datetime


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def get_date():
    return datetime.now().strftime("%d.%m.%Y")


def open_website(url: str):
    if not url.startswith(("https://", "http://")):
        raise ValueError("Разрешены только HTTP и HTTPS адреса")

    webbrowser.open(url)
    return f"Открываю сайт: {url}"


def open_calculator():
    subprocess.Popen(["calc.exe"])
    return "Калькулятор открыт."


def open_notepad():
    subprocess.Popen(["notepad.exe"])
    return "Блокнот открыт."