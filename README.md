# BetterChat 🧠💬

**BetterChat** is a customizable desktop chat assistant built with Python and Tkinter. It connects to an AI language model via API (e.g., OpenAI) and responds based on selected categories, providing context-aware and tailored replies.

## ✨ Features

- 🖥️ Simple, clean GUI built with Tkinter  
- 🌙 Light/Dark mode toggle  
- 📂 Multiple assistant categories (Car Dealership, Finance, Travel, Tech Support)  
- 🔑 API configuration via GUI (saved locally in `config.json`)  
- 🧠 Smart responses based on user-defined context  
- 💬 Scrollable, styled chat window  

## 📸 Screenshot

> *(Optional: Add a screenshot of your app here)*  
> ![BetterChat Screenshot](screenshot.png)

## ⚙️ Requirements

- Python 3.8+
- Required Python packages:
  - `tkinter` (usually included with Python)
  - `requests`

## 🚀 Getting Started

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/BetterChat.git
   cd BetterChat
   ```

2. **Install dependencies** (if needed):

   ```bash
   pip install requests
   ```

3. **Run the app**:

   ```bash
   python betterchat.py
   ```

## 🔧 Configuration

From the app menu:  
`File > Configure API`

Enter the following:
- **API Key**: Your access token (e.g., OpenAI API key)
- **API URL**: Your endpoint (e.g., `https://api.openai.com/v1/chat/completions`)
- **Model**: (Optional) e.g., `gpt-3.5-turbo`

These settings are saved to `config.json` for future use.

## 📚 Categories

| Category         | Description |
|------------------|-------------|
| Car Dealership   | Focused on buying and selling cars |
| Finance Advisor  | Provides financial tips and investment advice |
| Travel Assistant | Helps with travel planning and destinations |
| Technical Support| Assists with tech issues and troubleshooting |

## 📝 Project Structure

```
.
├── betterchat.py      # Main application script
├── config.json        # Stored API settings (created automatically)
├── README.md          # Project documentation
└── screenshot.png     # (Optional) App image
```

## 🔒 Security Note

Your API key is stored in plain text (`config.json`). **Do not commit this file to public repositories.**

## 📄 License

This project is licensed under the MIT License.  
Feel free to modify, improve, and use it in your own projects!

---

**BetterChat** – A lightweight, customizable AI-powered chat assistant with category-based prompts and a desktop-friendly interface.