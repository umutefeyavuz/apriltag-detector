from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import datetime
import psutil
import difflib

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
device = torch.device("cpu")
model.to(device)

memory = {}
personality = "neutral"

valid_commands = [
    "time", "what time is it", "current time",
    "date", "what is the date", "today's date",
    "temperature", "cpu temp", "temp",
    "learn", "remember", "set personality",
    "how are you", "hello", "hi"
]

def correct_command(cmd):
    words = cmd.lower().split()
    corrected = []
    for word in words:
        match = difflib.get_close_matches(word, valid_commands, n=1, cutoff=0.75)
        corrected.append(match[0] if match else word)
    return " ".join(corrected)

def generate_text(prompt, max_new_tokens=50):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    input_ids = inputs.input_ids.to(device)

    output = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )
    generated = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated[len(prompt):].strip()

def respond_to_command(command):
    global personality
    command = correct_command(command)
    cmd = command.lower().strip()

    if cmd.startswith("learn "):
        try:
            qa = command[6:].split("=", 1)
            question = qa[0].strip().lower()
            answer = qa[1].strip()
            memory[question] = answer
            return f"Learned response for '{question}'."
        except Exception:
            return "Learn command format error. Use: learn question=answer"

    if cmd.startswith("remember "):
        question = command[9:].strip().lower()
        return memory.get(question, "I don't remember that.")

    if cmd.startswith("set personality "):
        personality = cmd.replace("set personality ", "").strip()
        return f"Personality set to {personality}."

    if cmd in ["exit", "quit"]:
        return "exit"

    if cmd in ["time", "what time is it", "current time"]:
        return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."

    if cmd in ["date", "what is the date", "today's date"]:
        return f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}."

    if cmd in ["temperature", "cpu temp", "temp"]:
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return "Sorry, I can't read the CPU temperature."
            for name, entries in temps.items():
                for entry in entries:
                    if entry.current:
                        return f"The CPU temperature is {entry.current:.1f}°C."
            return "Sorry, temperature info not found."
        except Exception:
            return "Sorry, I couldn't read the CPU temperature."

    if cmd in memory:
        return memory[cmd]

    if personality == "friendly":
        if "how are you" in cmd:
            return "I'm doing great, thanks for asking!"
        elif "hello" in cmd or "hi" in cmd:
            return "Hey there, friend! How can I help you today?"
    elif personality == "funny":
        if "how are you" in cmd:
            return "Better now that you asked!"
        elif "hello" in cmd or "hi" in cmd:
            return "Yo! What's up?"
    else:
        if "how are you" in cmd:
            return "I'm just a bunch of code, but thanks for asking."
        elif "hello" in cmd or "hi" in cmd:
            return "Hello."

    return "Sorry, I don't understand that yet."

def main():
    print("Techtonic AI Assistant started. Type 'exit' to quit.")
    imagine_mode = False

    while True:
        user_input = input("You: ").strip()

        if imagine_mode:
            if user_input.lower() in ["exit", "quit"]:
                imagine_mode = False
                print("Assistant: Exiting imagine mode.")
                continue
            continuation = generate_text(user_input)
            print("Assistant:", continuation)
            continue

        if user_input.lower() == "imagine":
            imagine_mode = True
            print("Assistant: Imagine mode activated. Type 'exit' to quit this mode.")
            continue

        response = respond_to_command(user_input)
        if response == "exit":
            print("Assistant: Goodbye!")
            break
        print("Assistant:", response)
