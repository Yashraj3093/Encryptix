import tkinter as tk
from tkinter import scrolledtext
import datetime
import wikipedia
import subprocess
import webbrowser
import os

def speak(audio):
    chat_window.insert(tk.END, f"Bot: {audio}\n")
    chat_window.yview(tk.END)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your Chit ChatBot, How may I help you?")

def takeCommand():
    query = command_entry.get()
    chat_window.insert(tk.END, f"You: {query}\n")
    chat_window.yview(tk.END)
    command_entry.delete(0, tk.END)
    return query

def processCommand():
    query = takeCommand().lower()
    
    # general commands
    if 'hello'in query or 'how are you' in query:
        speak("Hello!")
        speak("How are you?")
    elif 'fine' in query or "good" in query:
        speak("It's good to know that you're fine.")
    elif 'my name' in query:
        speak("Your name is Yashraj.")
    elif 'your name' in query:
        speak("My name is Chit Chatbot.")
    elif "who made you" in query or "who created you" in query:
        speak("I have been created by my master Yashraj.")
    elif "who are you" in query:
        speak("I am a rule-based chatbot.")

    # time
    elif 'time' in query and 'date' in query:
        strDateTime = datetime.datetime.now().strftime("%d-%m-%y %I:%M:%S %p")
        speak(f"The Date and Time is {strDateTime}.")
    
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
        speak(f"The Time is {strTime}.")
    
    elif 'date' in query:
        strDate = datetime.datetime.now().strftime("%d-%m-%y")
        speak(f"The Date is {strDate}.")


    # search
    elif 'search' in query or 'play' in query:
        query = query.replace("search", "")
        query = query.replace("play", "")
        webbrowser.open(query)
        speak(f"Here are the search results for {query}.")
    elif 'what' in query:
        speak('Searching...')
        query = query.replace("what is", "").strip()
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia,")
        speak(results)

    # open websites
    elif 'open google' in query:
        speak("Here you go to Google.")
        webbrowser.open("https://www.google.com")
    elif 'open youtube' in query:
        speak("Here you go to YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open map" in query:
        speak("Here you go to Maps.")
        webbrowser.open_new_tab("https://www.google.com/maps")
    elif "open gmail" in query:
        speak("Here you go to Gmail.")
        webbrowser.open_new_tab("https://mail.google.com")

    # open system applications  
    elif "open camera" in query:
        speak("Opening Camera.")
        os.system("start microsoft.windows.camera:")
    elif "open screen keyboard" in query or "open on screen keyboard" in query:
        speak("Opening on-screen keyboard.")
        os.system("osk")
    elif "open calculator" in query:
        speak("Opening Calculator.")
        os.system("calc")
    elif "open notepad" in query:
        speak("Opening Notepad.")
        os.system("notepad")
    elif "open terminal" in query or "open cmd" in query:
        speak("Opening Terminal.")
        subprocess.call('cmd.exe')
    elif "open control panel" in query:
        speak("Opening Control Panel.")
        os.system("control panel")
    elif "open task manager" in query:
        speak("Opening Task Manager.")
        os.system("taskmgr")
    elif "open microsoft store" in query:
        speak("Opening Microsoft Store.")
        os.system("start ms-windows-store:")

    # exit
    elif "exit" in query or "quit" in query or "shut up" in query or "bye" in query or "goodbye" in query:
        print("Sure, as you wish. Goodbye!")
        root.quit()

root = tk.Tk()
root.title("Rule Based Chatbot")

# Text area to display conversation
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 14))
chat_window.pack(pady=10)

# Entry widget to type command
command_entry = tk.Entry(root, width=50, font=("Arial", 14))
command_entry.pack(pady=10)
command_entry.bind("<Return>", lambda event: processCommand())

# Send button
send_button = tk.Button(root, text="Send", command=processCommand, font=("Arial", 14))
send_button.pack(pady=10)

wishMe()

root.mainloop()
