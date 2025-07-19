import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import requests
import json
import threading

# --- Configuration ---
CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        
        return {"api_key": "YOUR API KEY", "api_url": "YOUR API URL"} #Your api and api key must be filled
    except json.JSONDecodeError:
        messagebox.showerror("Configuration Error", "Error reading config.json. Please ensure it's valid JSON.")
        return {"api_key": "YOUR API KEY", "api_url": "YOUR API URL"} #Your api and api key must be filled

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

config = load_config()
API_KEY = config.get("api_key")
API_URL = config.get("api_url")

# --- API Interaction ---
def chat_with_gpt(prompt, api_key, api_url):
    if not api_key:
        return "❌ API Key is not configured. Please go to File > Configure API."
    if not api_url:
        return "❌ API URL is not configured. Please go to File > Configure API."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        payload = {
            "model": "YOUR API MODEL", #MAKE SURE TO REPLACE THIS PART
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(api_url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            # Ensure the path to the content is correct, usually data['choices'][0]['message']['content']
            if 'choices' in data and len(data['choices']) > 0 and 'message' in data['choices'][0] and 'content' in data['choices'][0]['message']:
                return data['choices'][0]['message']['content'].strip()
            else:
                return f"❗ Unexpected API response format. Data: {json.dumps(data, indent=2)}"
        elif response.status_code == 401:
            return "❌ Invalid API key or access not granted. Please check your API key."
        elif response.status_code == 429:
            return "⛔️ You've exceeded your quota or sent too many requests. Please try again later."
        elif response.status_code == 404:
            # More specific 404 for Nebius might be "model not found" or incorrect endpoint
            return f"❗ API endpoint or model not found (Status: 404). Please verify API URL and model name: {api_url}"
        elif response.status_code >= 400: # Catch other client errors
            return f"❗ API error (Status: {response.status_code}): {response.text}"
        else: # Catch any other unexpected status codes
            return f"❗ Unknown error (Status: {response.status_code})\n{response.text}"

    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. The server took too long to respond."
    except requests.exceptions.ConnectionError:
        return "⚠️ Connection error. Please check your internet connection and API URL."
    except json.JSONDecodeError:
        return f"⚠️ Failed to decode JSON response from the server. Raw response: {response.text if 'response' in locals() else 'No response received'}"
    except Exception as e:
        return f"⚠️ An unexpected program error occurred: {str(e)}"

# --- GUI Functions ---
def send_message_thread():
    user_input = entry.get()
    if not user_input.strip() or user_input == "Type your message here...":
        messagebox.showwarning("Empty Message", "Please enter a message before sending.")
        return

    chat_area.config(state=tk.NORMAL) # Enable to insert
    chat_area.insert(tk.END, "You: " + user_input + "\n", "user")
    chat_area.config(state=tk.DISABLED) # Disable again
    entry.delete(0, tk.END)
    
    chat_area.config(state=tk.NORMAL) # Enable to insert
    chat_area.insert(tk.END, "BetterChat: Thinking...\n", "thinking") # Changed "GPT" to "BetterChat"
    chat_area.see(tk.END)
    chat_area.config(state=tk.DISABLED) # Disable again

    send_button.config(state=tk.DISABLED)
    entry.config(state=tk.DISABLED)

    def api_call_task():
        global API_KEY, API_URL
        response = chat_with_gpt(user_input, API_KEY, API_URL)
        root.after(0, lambda: update_chat_after_api_call(response))

    threading.Thread(target=api_call_task).start()

def update_chat_after_api_call(response):
    chat_area.config(state=tk.NORMAL) # Enable to modify

    # Attempt to remove "Thinking..." message
    try:
        # Find the start of the last line
        last_line_start = chat_area.index(f"{tk.END} - 2 lines linestart")
        last_line_content = chat_area.get(last_line_start, f"{last_line_start} lineend")
        if "BetterChat: Thinking..." in last_line_content: # Changed "GPT" to "BetterChat"
            chat_area.delete(last_line_start, f"{last_line_start} lineend + 1c") # +1c to include the newline
    except Exception:
        pass # Ignore if "Thinking..." wasn't found as expected

    chat_area.insert(tk.END, "BetterChat: " + response + "\n", "bot") # Changed "GPT" to "BetterChat"
    chat_area.see(tk.END)
    chat_area.config(state=tk.DISABLED) # Disable again

    send_button.config(state=tk.NORMAL)
    entry.config(state=tk.NORMAL)
    entry.focus_set()


def configure_api():
    global API_KEY, API_URL, config
    new_api_key = simpledialog.askstring("Configure API Key", "Enter your AI API Key:", initialvalue=API_KEY)
    if new_api_key is not None:
        API_KEY = new_api_key
        config["api_key"] = API_KEY
        save_config(config)

    new_api_url = simpledialog.askstring("Configure API URL", "Enter your Chat Completions URL:", initialvalue=API_URL)
    if new_api_url is not None:
        API_URL = new_api_url
        config["api_url"] = API_URL
        save_config(config)

def show_about():
    messagebox.showinfo("About BetterChat", "A simple desktop chat application using AI models via API.\n\nDeveloped with Tkinter.") # Changed "Chat with GPT" to "BetterChat"

# --- Main Window Setup ---
root = tk.Tk()
root.title("BetterChat") # Changed window title to "BetterChat"
root.geometry("650x700")
root.configure(bg="#e8e8e8")

# Menu Bar
menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Configure API", command=configure_api)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

# Chat area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Segoe UI", 11), bg="#ffffff", relief=tk.FLAT, borderwidth=5)
chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
chat_area.tag_config("user", foreground="#007bff", font=("Segoe UI", 11, "bold"))
chat_area.tag_config("bot", foreground="#28a745", font=("Segoe UI", 11))
chat_area.tag_config("thinking", foreground="#6c757d", font=("Segoe UI", 11, "italic"))
chat_area.config(state=tk.DISABLED)

# Input frame
entry_frame = tk.Frame(root, bg="#e8e8e8")
entry_frame.pack(padx=15, pady=(0, 15), fill=tk.X)

entry = tk.Entry(entry_frame, font=("Segoe UI", 11), relief=tk.FLAT, borderwidth=2, highlightbackground="#cccccc", highlightthickness=1)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry.bind("<Return>", lambda event: send_message_thread())
entry.insert(0, "Type your message here...")
entry.bind("<FocusIn>", lambda event: entry.delete(0, tk.END) if entry.get() == "Type your message here..." else None)
entry.bind("<FocusOut>", lambda event: entry.insert(0, "Type your message here...") if not entry.get() else None)


send_button = tk.Button(entry_frame, text="Send", command=send_message_thread, font=("Segoe UI", 11, "bold"), bg="#007bff", fg="white", relief=tk.FLAT, padx=10, pady=5)
send_button.pack(side=tk.RIGHT)
send_button.bind("<Enter>", lambda e: send_button.config(bg="#0056b3"))
send_button.bind("<Leave>", lambda e: send_button.config(bg="#007bff"))

# Initial focus
entry.focus_set()

# Start the GUI
root.mainloop()