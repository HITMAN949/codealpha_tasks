# 🤖 CodeAlpha Chatbot Project

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![NLTK](https://img.shields.io/badge/NLTK-3.8.1-orange)

A simple text-based chatbot built with Python's NLTK library for the CodeAlpha internship program.

## Features

- **Natural Language Processing**: Basic pattern matching and response generation
- **Conversational Flow**: Handles greetings, goodbyes, and common queries
- **Customizable Responses**: Easy to extend with new dialogue patterns
- **Error Handling**: Graceful exit on keyboard interrupts

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