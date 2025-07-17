import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import json

# Replace with your API key
API_KEY = "Your Api Key"  # ← Place your API key here

API_URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def chat_with_gpt(prompt):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)

        print("Response Status Code:", response.status_code)  # Print the response status code
        print("Response Text:", response.text)  # Print the response text

        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content'].strip()

        elif response.status_code == 401:
            return "❌ Invalid API key or access not granted."
        elif response.status_code == 429:
            return "⛔️ You've exceeded your quota or sent too many requests."
        else:
            return f"❗ Unknown error: {response.status_code}\n{response.text}"

    except Exception as e:
        return f"⚠️ Program error: {str(e)}"


def send_message():
    user_input = entry.get()
    if not user_input.strip():
        return

    chat_area.insert(tk.END, "You: " + user_input + "\n", "user")

    entry.delete(0, tk.END)
    response = chat_with_gpt(user_input)
    chat_area.insert(tk.END, "GPT: " + response + "\n", "bot")
    chat_area.see(tk.END)

# Create the main window
root = tk.Tk()
root.title("Chat with GPT")
root.geometry("500x600")
root.configure(bg="#f0f0f0")

# Chat area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Tahoma", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.tag_config("user", foreground="blue")
chat_area.tag_config("bot", foreground="green")

# Input field
entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=10, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Tahoma", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(entry_frame, text="Send", command=send_message, font=("Tahoma", 12))
send_button.pack(side=tk.RIGHT)

# Start the GUI
root.mainloop()
