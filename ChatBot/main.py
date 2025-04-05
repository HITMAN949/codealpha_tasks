import nltk
import random
import time
import threading
from nltk.chat.util import Chat, reflections
from datetime import datetime, timedelta

nltk.download('punkt')

SESSION_TIMEOUT = 60
last_activity = time.time()
shutdown_flag = threading.Event()

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
        [
            lambda _: f"The current time is {datetime.now().strftime('%H:%M')}",
            f"Right now it's {datetime.now().strftime('%I:%M %p')}"
        ]
    ],
    [
        r"I am (hungry|sleepy|tired|bored)",
        ["When humans feel %1, they should probably take a break!",
         "I don't experience %1, but I hear resting helps humans.",
         "%1? Maybe you should grab a snack or take a nap!"]
    ],
    [
        r"quit|bye|goodbye",
        ["Goodbye!", "It was nice talking to you!", "See you later!"]
    ],
    [
        r"help|what can you do",
        ["I can chat about various topics, tell time, and discuss CodeAlpha!",
         "Try asking me about myself, the time, or how I'm doing.",
         "I'm here to have conversations. Ask me anything!"]
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

    print(f"ChatBot: Hi! I'm Your ChatBot. (Timeout: {SESSION_TIMEOUT // 60} mins)")
    print("Type 'quit' to exit or wait for timeout\n")

    chat = Chat(pairs, reflections)

    try:
        while not shutdown_flag.is_set():
            try:
                user_input = input("You: ").strip()
                last_activity = time.time()  # Update activity timestamp

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("ChatBot: Goodbye!")
                    shutdown_flag.set()
                    break

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