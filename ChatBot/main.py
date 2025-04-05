import nltk
import random
import time
import threading
import requests
import json
import re
from nltk.chat.util import Chat, reflections
from datetime import datetime
from config import OPENWEATHER_API_KEY

nltk.download('punkt')

SESSION_TIMEOUT = 60
last_activity = time.time()
shutdown_flag = threading.Event()

def get_weather(city):
    """Get weather data from OpenWeatherMap API"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return {
                'city': data.get('name', city),
                'temp': data['main'].get('temp', '?'),
                'description': data['weather'][0].get('description', '?'),
                'humidity': data['main'].get('humidity', '?')
            }
        else:
            return {'error': data.get('message', 'Unknown error')}

    except requests.exceptions.RequestException as e:
        return {'error': f"Connection error: {str(e)}"}
    except json.JSONDecodeError:
        return {'error': "Invalid API response"}
    except KeyError:
        return {'error': "Unexpected data format"}

pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey!"]
    ],
    [
        r"what is your name\??",
        ["I'm Your ChatBot!", "You can call me My Bot!"]
    ],
    [
        r"how are you ?",
        ["I'm doing great!", "I'm good, thanks for asking!"]
    ],
    [
        r"how are you( doing)?\??",
        [
            "I'm functioning optimally, thank you!",
            "All systems go! How about you?",
            "I'm a bot, so I'm always at 100%!"
        ]
    ],
    [
        r"(.*)(codealpha|internship)(.*)",
        ["CodeAlpha offers great tech internship programs!",
         "I was created for CodeAlpha's python internship program.",
         "This chatbot is part of a CodeAlpha project."]
    ],
    [
        r"thank(s| you)",
        ["You're welcome!",
         "Happy to help!",
         "Anytime!"]
    ],
    [
        r"what('s| is) the time\??",
        lambda _: f"The current time is {datetime.now().strftime('%I:%M %p')}"
    ],
    [
        r"I am (hungry|sleepy|tired|bored)",
        ["When humans feel %1, they should probably take a break!",
         "I don't experience %1, but I hear resting helps humans.",
         "%1? Maybe you should grab a snack or take a nap!"]
    ],
    [
        r"tell me a joke",
        ["Why don't scientists trust atoms? Because they make up everything!",
         "What do you get when you cross a snowman and a dog? Frostbite!",
         "Why did the computer go to therapy? Too many bytes of trauma!"]
    ],
    [
        r"give me a fun fact",
        ["Did you know? Honey never spoils.",
         "Octopuses have three hearts!",
         "Bananas are berries, but strawberries aren't."]
    ],
    [
        r"quit|bye|goodbye",
        ["Goodbye!", "It was nice talking to you!", "See you later!"]
    ],
    [
        r"help|what can you do",
        ["I can chat, tell you the time, share jokes or facts, and check the weather!",
         "Ask me about CodeAlpha, the weather, or just say hi!",
         "Try saying 'tell me a joke' or 'what's the weather in London?'"]
    ],
    [
        r"(.*)",
        ["I'm not sure I understand.", "Could you rephrase that?"]
    ]
]

def timeout_checker():
    global last_activity
    while not shutdown_flag.is_set():
        if time.time() - last_activity > SESSION_TIMEOUT:
            print("\nChatBot: Session timed out due to inactivity. Goodbye!")
            shutdown_flag.set()
            break
        time.sleep(1)

def chatbot():
    global last_activity

    timeout_thread = threading.Thread(target=timeout_checker)
    timeout_thread.daemon = True
    timeout_thread.start()

    timeout_msg = f"{SESSION_TIMEOUT // 60} minutes" if SESSION_TIMEOUT >= 60 else f"{SESSION_TIMEOUT} seconds"
    print(f"ChatBot: Hi! I'm Your ChatBot. (Timeout: {timeout_msg})")
    print("Type 'quit' to exit or wait for timeout\n")

    chat = Chat(pairs, reflections)

    try:
        while not shutdown_flag.is_set():
            try:
                user_input = input("You: ").strip().lower()
                last_activity = time.time()

                if not user_input:
                    continue

                if user_input in ['quit', 'exit', 'bye']:
                    print("ChatBot: Goodbye!")
                    shutdown_flag.set()
                    break

                weather_match = re.match(r"(what's|what is) the weather in (.+)", user_input)
                if weather_match:
                    city = weather_match.group(2).strip().title()
                    weather = get_weather(city)
                    if 'error' in weather:
                        response = f"Sorry, couldn't fetch weather: {weather['error']}"
                    else:
                        response = (f"Weather in {weather['city']}: {weather['temp']}°C, "
                                    f"{weather['description']}, humidity {weather['humidity']}%")
                else:
                    response = chat.respond(user_input)

                print(f"ChatBot: {response}")

            except EOFError:
                print("\nChatBot: Session ended.")
                shutdown_flag.set()
                break

    except KeyboardInterrupt:
        print("\nChatBot: Session interrupted. Goodbye!")
    finally:
        shutdown_flag.set()
        if timeout_thread.is_alive():
            timeout_thread.join()

if __name__ == "__main__":
    chatbot()
