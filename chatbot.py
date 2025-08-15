import requests
import datetime
import random
import platform
import wikipedia

# Joke and quote data
jokes = [
    "Why did the math book look sad? Because it had too many problems.",
    "Parallel lines have so much in common… It’s a shame they’ll never meet.",
    "I told my computer I needed a break, and it said 'No problem, I’ll go to sleep!'"
]

quotes = [
    "Push yourself, because no one else is going to do it for you.",
    "Start where you are. Use what you have. Do what you can.",
    "The best way to get started is to quit talking and begin doing."
]

# Chatbot prompt template
template = """
Today is: {today}
Current time is: {time}

Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y"), now.strftime("%I:%M %p")

def query_ollama(context, question):
    today, current_time = get_current_datetime()
    prompt = template.format(today=today, time=current_time, context=context, question=question)

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"]

def handle_builtin_commands(user_input):
    user_input = user_input.lower().strip()

    if user_input == "date":
        today, _ = get_current_datetime()
        return f"📅 Today's date is {today}."

    elif user_input == "time":
        _, time = get_current_datetime()
        return f"⏰ Current time is {time}."

    elif user_input == "joke":
        return f"😂 {random.choice(jokes)}"

    elif user_input == "quote":
        return f"💡 {random.choice(quotes)}"

    elif user_input == "weather":
        return "☁️ It's currently 27°C with light clouds in Mumbai (demo)."

    elif user_input == "system":
        return f"🖥️ OS: {platform.system()} {platform.release()}, Python: {platform.python_version()}"

    elif user_input.startswith("calc "):
        try:
            expr = user_input[5:]
            result = eval(expr)
            return f"🧮 Result: {result}"
        except:
            return "⚠️ Invalid math expression."

    elif user_input.startswith("wiki "):
        topic = user_input[5:]
        try:
            summary = wikipedia.summary(topic, sentences=2)
            return f"📚 {summary}"
        except Exception as e:
            return f"❌ Wikipedia error: {str(e)}"

    elif user_input == "help":
        return (
            "🤖 Available commands:\n"
            "- `date` → Show today's date\n"
            "- `time` → Show current time\n"
            "- `joke` → Tell a joke\n"
            "- `quote` → Show motivational quote\n"
            "- `weather` → Show mock weather\n"
            "- `system` → Show system info\n"
            "- `calc <expr>` → Do math (e.g., `calc 2+5*3`)\n"
            "- `wiki <topic>` → Wikipedia summary\n"
            "- Ask anything else to AI\n"
            "- `exit` → Quit chatbot"
        )

    return None  # Not a command

def handle_conversation():
    context = ""
    print("🤖 Welcome to your Smart AI Assistant!")
    print("Type 'help' to see available commands.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break

        # Check for built-in command
        local_response = handle_builtin_commands(user_input)
        if local_response:
            print("Bot:", local_response)
            context += f"\nUser: {user_input}\nAI: {local_response}"
            continue

        # If not command, go to LLaMA
        try:
            response = query_ollama(context, user_input)
            print("Bot:", response)
            context += f"\nUser: {user_input}\nAI: {response}"
        except Exception as e:
            print("❌ Error talking to model:", str(e))

if __name__ == "__main__":
    handle_conversation()

