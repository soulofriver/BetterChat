# 💬 BetterChat

BetterChat is a lightweight desktop chatbot I built using Python and Tkinter. It connects to an AI model via your preferred API provider (like OpenAI, Nebius, etc.) and gives you a simple and responsive GUI for interacting with it — right from your desktop.

This project lives in a separate branch of my [BetterChat repo](https://github.com/soulofriver/BetterChat), where I experiment with ideas and GUI tooling around AI interfaces. 🎯

---

## 🧰 Features

- 🪟 Clean desktop interface built with `tkinter`
- 🔐 Secure, user-configurable API key and endpoint (saved to `config.json`)
- 📡 Supports any chat completion-compatible AI model (OpenAI, Nebius, etc.)
- 🧵 Asynchronous request handling using threads
- 🗨️ Custom chat styling for user, bot, and thinking states
- 🚫 Error messages for timeout, invalid keys, or wrong endpoints
- 🧠 Swappable model configuration via code or GUI menu

---

## 🚀 Quick Start

### 1. Clone This Branch
```bash
git clone -b <Ali Rafati> https://github.com/soulofriver/BetterChat.git
cd BetterChat

2. Install Dependencies
pip install requests

3. Run the App
python betterchat.py

Configuration
{
  "api_key": "YOUR API KEY",
  "api_url": "YOUR API URL"
}

You can also go to the File > Configure API menu in the app to edit these at any time.

 Don’t Forget:
In the code, replace:
"model": "YOUR API MODEL"
with something like:
"model": "gpt-3.5-turbo"

Contributions Welcome
Have ideas? Spot bugs? Want to make the chat history scroll better or add markdown rendering? Fork away or open an issue in the BetterChat main repo.