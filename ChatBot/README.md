# 🤖 CodeAlpha Chatbot Project

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![NLTK](https://img.shields.io/badge/NLTK-3.8.1-orange)

A simple text-based chatbot built with Python's NLTK library for the CodeAlpha internship program.

## Features

- **Natural Language Processing**: Basic pattern matching and response generation
- **Conversational Flow**: Handles greetings, goodbyes, and common queries
- **Customizable Responses**: Easy to extend with new dialogue patterns
- **Error Handling**: Graceful exit on keyboard interrupts
- **🌤 Weather Updates**: Ask “what’s the weather in [city]?” to get real-time weather info using the OpenWeatherMap API.
- **🕒 Current Time**: Type “what’s the time?” to get the current local time.
- **😂 Jokes** : Ask for a joke with “tell me a joke” and enjoy a laugh.
- **🤓 Fun Facts** : Learn something new with “give me a fun fact”.
- **⏳ Auto Timeout** : Chat session automatically ends after 60 seconds of inactivity.
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HITMAN949/codealpha_tasks/tree/main/ChatBot
   cd codealpha_tasks-chatbot

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Download NLTK data:
   ```python
   import nltk
    nltk.download('punkt')

4. Usage:
   ```bash
   python chatbot.py