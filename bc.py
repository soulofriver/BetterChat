import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, font
import requests, json, os, io, emoji
from PIL import Image, ImageTk
from datetime import datetime

CONFIG_FILE = "config.json"

CATEGORIES = {
    "Car Dealership": "You are BetterChat, a helpful assistant working at a car dealership.",
    "Finance Advisor": "You are BetterChat, a smart and friendly finance advisor.",
    "Travel Assistant": "You are BetterChat, a cheerful travel assistant.",
    "Technical Support": "You are BetterChat, a knowledgeable tech support assistant.",
    "Image Generator": "You are BetterChat, an AI that generates images based on user prompts."
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f)

def configure_api():
    api_key = simpledialog.askstring("Configure API", "Enter your API key:", show='*')
    api_url = simpledialog.askstring("Configure API", "Enter the API endpoint URL:")
    model = simpledialog.askstring("Configure API", "Enter the model name (optional):")
    save_config({"api_key": api_key, "api_url": api_url, "model": model or ""})
    messagebox.showinfo("Success", "API settings saved!")

def chat_with_gpt(prompt, api_key, api_url, model):
    if not api_key:
        return "❌ API key not set."
    if not api_url:
        return "❌ API URL not set."
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    system = CATEGORIES.get(app.selected_category.get(), "")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt}
        ],
        "temperature": 0.7
    }
    try:
        r = requests.post(api_url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Chat error: {e}"

def generate_image(prompt, api_key):
    url = "https://api.openai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "n":1, "size":"512x512"}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["data"][0]["url"]
    except Exception as e:
        return f"⚠️ Image error: {e}"

class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title("BetterChat")
        root.geometry("800x650")
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        # ttk style for frames
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Custom.TFrame", background="#E8F1FA")

        # Menu
        menu = tk.Menu(root, bg="#E8F1FA", fg="#4A90E2")
        file_m = tk.Menu(menu, tearoff=0)
        file_m.add_command(label="Configure API", command=configure_api)
        file_m.add_separator()
        file_m.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=file_m)
        edit_m = tk.Menu(menu, tearoff=0)
        edit_m.add_command(label="Clear Chat", command=self.clear_chat)
        menu.add_cascade(label="Edit", menu=edit_m)
        root.config(menu=menu)

        # Top controls
        top = ttk.Frame(root, style="Custom.TFrame", padding=8)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        tk.Label(top, text="Category:", bg="#E8F1FA", fg="#4A90E2").grid(row=0, column=0, sticky="w")
        self.selected_category = tk.StringVar(value="Car Dealership")
        self.category_combobox = ttk.Combobox(
            top, textvariable=self.selected_category,
            values=list(CATEGORIES.keys()), state="readonly"
        )
        self.category_combobox.grid(row=0, column=1, sticky="ew", padx=(4,10))

        btns = ttk.Frame(top, style="Custom.TFrame")
        btns.grid(row=0, column=2)

        self.clear_btn = tk.Button(btns, text="🗑️ Clear", command=self.clear_chat,
                                   bd=0, padx=10, pady=5)
        self.clear_btn.pack(side="left", padx=5)

        self.theme_btn = tk.Button(btns, text="", font=("Segoe UI", 18),
                                   bd=0, padx=10, pady=5)
        self.theme_btn.pack(side="left")

        # Chat canvas for bubbles
        self.chat_frame = ttk.Frame(root, style="Custom.TFrame", relief="sunken", borderwidth=2)
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        self.chat_frame.rowconfigure(0, weight=1)
        self.chat_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.chat_frame, bg="#E8F1FA", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.message_container = ttk.Frame(self.canvas, style="Custom.TFrame")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_window = self.canvas.create_window((0,0), window=self.message_container, anchor="nw")
        self.message_container.bind("<Configure>", self.on_frame_configure)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Fonts
        self.bubble_font = font.Font(family="Segoe UI", size=11)
        self.time_font = font.Font(family="Segoe UI", size=8, slant="italic")

        # Entry & buttons
        entry_frame = ttk.Frame(root, style="Custom.TFrame", padding=8)
        entry_frame.grid(row=2, column=0, sticky="ew")
        entry_frame.columnconfigure(0, weight=1)

        self.entry = tk.Entry(entry_frame, bd=0)
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0,8))
        self.entry.insert(0, "Type your message here…")
        self.entry.bind("<FocusIn>", lambda e: self.entry.delete(0, "end") 
                        if self.entry.get().startswith("Type") else None)
        self.entry.bind("<FocusOut>", lambda e: self.entry.insert(0, "Type your message here…") 
                        if not self.entry.get() else None)
        self.entry.bind("<Return>", self.send_text)

        self.image_btn = tk.Button(entry_frame, text="🖼️ Image", command=self.send_image,
                                   bd=0, padx=10, pady=5)
        self.image_btn.grid(row=0, column=1, padx=4)

        self.send_btn = tk.Button(entry_frame, text="Send", command=self.send_text,
                                  bd=0, padx=10, pady=5)
        self.send_btn.grid(row=0, column=2)

        # Storage
        self.bubble_labels = []
        self.time_labels = []
        self.chat_images = []

        # Typing indicator
        self.typing_label = None
        self.typing_anim_id = None
        self.dot_count = 0

        # Shortcuts
        root.bind("<Control-Return>", lambda e: self.send_text())
        root.bind("<Control-Up>",    lambda e: self.canvas.yview_scroll(-3, "units"))
        root.bind("<Control-Down>",  lambda e: self.canvas.yview_scroll( 3, "units"))
        root.bind("<Control-plus>",  lambda e: self.adjust_font(1))
        root.bind("<Control-minus>", lambda e: self.adjust_font(-1))

        # Theme state: start in DARK mode
        self.is_dark = True
        self.theme_btn.config(command=self.toggle_theme)
        self.apply_theme(self.is_dark)

        # Welcome
        self.clear_chat()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def clear_chat(self):
        for w in self.message_container.winfo_children():
            w.destroy()
        self.bubble_labels.clear()
        self.time_labels.clear()
        self.chat_images.clear()
        self.push("BetterChat", ":wave: Welcome to BetterChat! Select a category and say hi.", "bot")

    def push(self, author, text, sender):
        text = emoji.emojize(text, language='alias')
        bubble_bg = "#DCF8C6" if sender=="user" else "#FFFFFF"
        align = "e" if sender=="user" else "w"
        padx = (50,5) if sender=="user" else (5,50)

        lbl = tk.Label(self.message_container, text=f"{author}: {text}",
                       bg=bubble_bg, font=self.bubble_font, wraplength=400,
                       justify="right" if sender=="user" else "left",
                       bd=1, relief="solid", padx=6, pady=4)
        lbl.pack(fill="x", anchor=align, padx=padx, pady=(5,0))
        self.bubble_labels.append(lbl)

        ts = datetime.now().strftime("%H:%M")
        time_lbl = tk.Label(self.message_container, text=ts,
                            bg=self.canvas["bg"], fg="#666666", font=self.time_font)
        time_lbl.pack(anchor=align, padx=padx, pady=(0,5))
        self.time_labels.append(time_lbl)

        self.canvas.yview_moveto(1.0)

    def send_text(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, tk.END)
        self.push("You", msg, "user")
        self.show_typing()
        self.root.after(100, lambda: self.handle_text(msg))

    def handle_text(self, prompt):
        cfg = load_config()
        resp = chat_with_gpt(prompt, cfg.get("api_key"), cfg.get("api_url"), cfg.get("model", ""))
        self.stop_typing()
        self.push("BetterChat", resp, "bot")

    def send_image(self):
        prompt = self.entry.get().strip()
        if not prompt:
            return
        self.entry.delete(0, tk.END)
        self.push("You", prompt, "user")
        self.show_typing()
        self.root.after(100, lambda: self.handle_image(prompt))

    def handle_image(self, prompt):
        cfg = load_config()
        url = generate_image(prompt, cfg.get("api_key"))
        self.stop_typing()
        if url.startswith("http"):
            self.push("BetterChat", ":art: Here's your image:", "bot")
            self.embed_image(url)
        else:
            self.push("BetterChat", url, "bot")

    def embed_image(self, src):
        try:
            resp = requests.get(src)
            img = Image.open(io.BytesIO(resp.content)).resize((256,256))
            photo = ImageTk.PhotoImage(img)
            self.chat_images.append(photo)
            img_label = tk.Label(self.message_container, image=photo, bg=self.canvas["bg"])
            img_label.pack(anchor="w", padx=5, pady=5)
            self.canvas.yview_moveto(1.0)
        except Exception as e:
            self.push("BetterChat", f"[Image load failed: {e}]", "bot")

    def show_typing(self):
        if self.typing_label:
            return
        self.typing_label = tk.Label(self.message_container,
                                     text="Bot is typing", fg="#888888",
                                     bg=self.canvas["bg"], font=self.bubble_font)
        self.typing_label.pack(anchor="w", padx=5, pady=5)
        self.animate_typing()

    def animate_typing(self):
        if not self.typing_label:
            return
        self.dot_count = (self.dot_count + 1) % 4
        dots = "." * self.dot_count
        self.typing_label.config(text=f"Bot is typing{dots}")
        self.typing_anim_id = self.root.after(400, self.animate_typing)

    def stop_typing(self):
        if self.typing_anim_id:
            self.root.after_cancel(self.typing_anim_id)
        if self.typing_label:
            self.typing_label.destroy()
            self.typing_label = None
            self.dot_count = 0

    def adjust_font(self, delta):
        new_size = max(8, self.bubble_font.cget("size") + delta)
        self.bubble_font.configure(size=new_size)
        for lbl in self.bubble_labels:
            lbl.config(font=self.bubble_font)

    def apply_theme(self, is_dark):
        if is_dark:
            bg, fg, btn_bg, btn_fg, icon = "#1E1E2E", "#E2E8F0", "#1E1E2E", "#E2E8F0", "🌙"
        else:
            bg, fg, btn_bg, btn_fg, icon = "#E8F1FA", "#4A90E2", "#4A90E2", "#FFFFFF", "☀️"

        self.style.configure("Custom.TFrame", background=bg)
        self.canvas.config(bg=bg)
        self.chat_frame.config(style="Custom.TFrame")
        for frame in (self.root,):
            frame.config(bg=bg)

        self.entry.config(bg=bg, fg=fg, insertbackground=fg)
        for btn in (self.clear_btn, self.theme_btn, self.image_btn, self.send_btn):
            btn.config(bg=btn_bg, fg=btn_fg)

        for lbl in self.bubble_labels + self.time_labels:
            lbl.config(bg=lbl.cget("bg"), fg=lbl.cget("fg"))

        self.theme_btn.config(text=icon)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme(self.is_dark)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
