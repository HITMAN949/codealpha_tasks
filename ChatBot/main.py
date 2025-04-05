import nltk
import random
from nltk.chat.util import Chat, reflections
from datetime import datetime

nltk.download('punkt')

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

def chatbot():
    print("Chatbot: Hi! I'm Your ChatBot. Type 'quit' to exit.")
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    chatbot()