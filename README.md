BetterChat
BetterChat is a versatile desktop chat application built with Python's Tkinter, allowing users to interact with AI models for various purposes, including general conversations, specialized assistance (e.g., car dealership, finance, travel, tech support), and image generation. It features a modern UI with chat bubbles, a typing indicator, adjustable font sizes, and a dark/light theme toggle.

Features
Multi-Category AI Chat: Engage with the AI in different roles:

Car Dealership Assistant

Finance Advisor

Travel Assistant

Technical Support

Image Generator

API Configuration: Easily set up your API key, endpoint URL, and model name through a user-friendly interface.

Text Generation: Send text prompts to the AI and receive intelligent responses.

Image Generation: Generate images based on your text prompts (requires an image generation API, e.g., OpenAI DALL-E).

Dynamic Chat Interface: Messages are displayed in intuitive chat bubbles with timestamps.

Typing Indicator: See when the AI is generating a response.

Adjustable Font Size: Increase or decrease the chat font size for better readability.

Theme Toggle: Switch between a light and dark theme.

Clear Chat: Easily clear the conversation history.

Keyboard Shortcuts:

Ctrl + Return: Send message

Ctrl + Up/Down: Scroll chat

Ctrl + Plus/Minus: Adjust font size

Installation
To run BetterChat, you need Python 3.x installed on your system.

Clone the repository (or download bc.py):

git clone https://github.com/soulofriver/betterchat.git
cd betterchat

(If you just have bc.py, simply navigate to its directory.)

Install dependencies:
Open your terminal or command prompt and run:

pip install requests Pillow emoji

Usage
Run the application:

python bc.py

Configure API Settings:

Upon first launch or anytime you need to change settings, go to File > Configure API in the application menu.

Enter your API Key (e.g., from OpenAI).

Enter your API Endpoint URL (e.g., https://api.openai.com/v1/chat/completions for chat, or https://api.openai.com/v1/images/generations for images, though the code handles separate endpoints internally).

Enter the Model Name (e.g., gpt-3.5-turbo, gpt-4).

Click "OK" to save. These settings will be stored in config.json.

Start Chatting:

Select a Category from the dropdown menu at the top.

Type your message in the input field at the bottom.

Click the "Send" button or press Ctrl + Return to send your message.

Generate Images:

Select "Image Generator" as the category.

Type your image prompt in the input field.

Click the "🖼️ Image" button. The AI will generate an image based on your prompt and display it in the chat.

Toggle Theme:

Click the 🌙 or ☀️ icon button at the top right to switch between dark and light themes.

API Configuration Details
BetterChat is designed to work with APIs that follow the OpenAI API structure for chat completions and image generation.

api_key: Your authentication token for the AI service.

api_url: The base URL for the chat completion endpoint (e.g., https://api.openai.com/v1/chat/completions). The image generation uses a hardcoded OpenAI image generation URL (https://api.openai.com/v1/images/generations).

model: The specific model identifier you wish to use for chat (e.g., gpt-3.5-turbo).

Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please feel free to open an issue or submit a pull request.

License
This project is open-source and available under the MIT License.
