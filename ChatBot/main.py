import nltk
import random
from nltk.chat.util import Chat, reflections


nltk.download('punkt')


pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey!"]
    ],
    [
        r"what is your name?",
        ["I'm Your ChatBot!", "You can call me My Bot!"]
    ],
    [
        r"how are you ?",
        ["I'm doing great!", "I'm good, thanks for asking!"]
    ],
    [
        r"(.*) (hungry|sleepy|tired)",
        ["I'm a bot, I don't feel %2!", "Maybe you should take a break?"]
    ],
    [
        r"quit|bye|goodbye",
        ["Goodbye!", "It was nice talking to you!", "See you later!"]
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