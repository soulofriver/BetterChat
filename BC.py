import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import requests
import json
import os

CONFIG_FILE = "config.json"

CATEGORIES = {
    "Car Dealership": "You are BetterChat, a helpful assistant working at a car dealership. Always respond in the context of buying or selling cars.",
    "Finance Advisor": "You are BetterChat, a smart and friendly finance advisor. Always respond with financial tips, investment advice, and money-saving strategies.",
    "Travel Assistant": "You are BetterChat, a cheerful travel assistant. Always respond with travel advice, flight bookings, destinations, and planning tips.",
    "Technical Support": "You are BetterChat, a knowledgeable tech support assistant. Help users with technical issues and explain things clearly."
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def configure_api():
    api_key = simpledialog.askstring("Configure API", "Enter your API key:", show='*')
    api_url = simpledialog.askstring("Configure API", "Enter the API endpoint URL:")
    model_name = simpledialog.askstring("Configure API", "Enter the model name (leave blank if handled in API):")
    config = {"api_key": api_key, "api_url": api_url, "model": model_name or ""}
    save_config(config)
    messagebox.showinfo("Success", "API settings saved successfully!")

def show_about():
    messagebox.showinfo(
        "About BetterChat",
        "BetterChat is a desktop chat assistant with category-based AI responses.\nBuilt with Tkinter."
    )

def chat_with_gpt(prompt, api_key, api_url, model):
    if not api_key:
        return "❌ API Key is not configured. Please go to File > Configure API."
    if not api_url:
        return "❌ API URL is not configured. Please go to File > Configure API."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    system_prompt = CATEGORIES.get(selected_category.get(), CATEGORIES["Car Dealership"])

    try:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            choice = data.get("choices", [{}])[0]
            return choice.get("message", {}).get("content", "").strip() or (
                f"❗ Unexpected API response format.\n{json.dumps(data, indent=2)}"
            )
        elif response.status_code == 401:
            return "❌ Invalid API key or access not granted. Please check your API key."
        elif response.status_code == 429:
            return "⛔️ You've exceeded your quota or sent too many requests. Please try again later."
        elif response.status_code == 404:
            return f"❗ API endpoint or model not found (404). Please verify API URL and model name."
        else:
            return f"❗ API error ({response.status_code}): {response.text}"

    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. The server took too long to respond."
    except requests.exceptions.ConnectionError:
        return "⚠️ Connection error. Please check your internet connection and API URL."
    except json.JSONDecodeError:
        return "⚠️ Failed to decode JSON response from the server."
    except Exception as e:
        return f"⚠️ An unexpected program error occurred: {e}"

def send_message(event=None):
    text = entry.get().strip()
    if not text:
        return

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {text}\n", "user")
    chat_area.insert(tk.END, "BetterChat: Thinking...\n", "thinking")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

    entry.delete(0, tk.END)
    root.after(100, lambda: update_chat_after_api_call(text))

def update_chat_after_api_call(prompt):
    chat_area.config(state=tk.NORMAL)
    chat_area.delete("end-3l", "end-1l")

    cfg = load_config()
    api_key = cfg.get("api_key")
    api_url = cfg.get("api_url")
    model = cfg.get("model", "")

    response = chat_with_gpt(prompt, api_key, api_url, model)
    chat_area.insert(tk.END, f"BetterChat: {response}\n", "bot")
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode

    # Update emoji on button
    emoji = "🌙" if is_dark_mode else "☀️"
    theme_button.config(text=emoji)

    # Define colors based on theme
    bg = "#1e1e1e" if is_dark_mode else "#f1f1f1"
    fg = "#ffffff" if is_dark_mode else "#000000"
    entry_bg = "#2c2c2c" if is_dark_mode else "#ffffff"
    entry_fg = "#ffffff" if is_dark_mode else "#000000"
    chat_bg = "#2c2c2c" if is_dark_mode else "#ffffff"
    chat_fg = "#f0f0f0" if is_dark_mode else "#333333"
    btn_bg = "#333333" if is_dark_mode else "#dddddd"
    btn_fg = "#ffffff" if is_dark_mode else "#000000"

    # Apply to widgets
    root.configure(bg=bg)
    category_frame.configure(bg=bg)
    category_label.configure(bg=bg, fg=fg)
    entry_frame.configure(bg=bg)
    chat_frame.configure(bg=bg)

    chat_area.configure(bg=chat_bg, fg=chat_fg, insertbackground=entry_fg)
    entry.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
    send_button.configure(bg="#007acc", fg="white")
    theme_button.configure(bg=btn_bg, fg=btn_fg)

    # Style the Combobox
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "TCombobox",
        fieldbackground=entry_bg,
        background=entry_bg,
        foreground=entry_fg
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", entry_bg)],
        foreground=[("readonly", entry_fg)]
    )

    # Update chat tags
    chat_area.tag_config("user", foreground="#4FC3F7" if is_dark_mode else "#007acc")
    chat_area.tag_config("bot", foreground=chat_fg)
    chat_area.tag_config("thinking", foreground="#aaaaaa" if is_dark_mode else "#999999")

# Main application setup
root = tk.Tk()
root.title("BetterChat")
root.geometry("720x600")

is_dark_mode = True

# Menus
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Configure API", command=configure_api)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_theme)
menu_bar.add_cascade(label="View", menu=view_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Category selection + theme button
category_frame = tk.Frame(root)
category_frame.pack(padx=15, pady=(15, 0), fill=tk.X)

category_label = tk.Label(
    category_frame,
    text="Select Chat Category:",
    font=("Segoe UI", 10)
)
category_label.pack(side=tk.LEFT)

selected_category = tk.StringVar(value="Car Dealership")
category_dropdown = ttk.Combobox(
    category_frame,
    textvariable=selected_category,
    values=list(CATEGORIES.keys()),
    state="readonly",
    font=("Segoe UI", 10),
    width=25
)
category_dropdown.pack(side=tk.LEFT, padx=(10, 0))

theme_button = tk.Button(
    category_frame,
    text="🌙",
    font=("Segoe UI", 12),
    command=toggle_theme,
    relief=tk.FLAT,
    bd=0
)
theme_button.pack(side=tk.RIGHT, padx=(0, 5))

# Chat display
chat_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
chat_frame.pack(padx=15, pady=(10, 5), fill=tk.BOTH, expand=True)

chat_area = tk.Text(
    chat_frame,
    font=("Segoe UI", 11),
    wrap=tk.WORD,
    state=tk.DISABLED,
    bd=0,
    padx=10,
    pady=10
)
chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(chat_frame, command=chat_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_area.config(yscrollcommand=scrollbar.set)

# Entry & send button
entry_frame = tk.Frame(root)
entry_frame.pack(padx=15, pady=(0, 15), fill=tk.X)

entry = tk.Entry(entry_frame, font=("Segoe UI", 11))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry.bind("<Return>", send_message)

send_button = tk.Button(
    entry_frame,
    text="Send",
    font=("Segoe UI", 10, "bold"),
    bg="#007acc",
    fg="white",
    command=send_message
)
send_button.pack(side=tk.RIGHT)

# Initial chat welcome
chat_area.config(state=tk.NORMAL)
chat_area.insert(
    tk.END,
    "BetterChat: 👋 Welcome to BetterChat! Select a category and say hi!\n",
    "bot"
)
chat_area.config(state=tk.DISABLED)

# Apply initial theme and start loop
toggle_theme()
root.mainloop()
