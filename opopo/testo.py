import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time

class VoiceAssistantGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Assistant")

        self.label = tk.Label(self.root, text="Say something:")
        self.label.pack()

        self.response_label = tk.Label(self.root, text="")
        self.response_label.pack()

        self.listen_and_respond_button = tk.Button(self.root, text="Listen and Respond", command=self.listen_and_respond)
        self.listen_and_respond_button.pack()

        self.listening = False

    def listen_and_respond(self):
        if not self.listening:
            self.listening = True
            thread = Thread(target=self.listen_thread)
            thread.start()

    def listen_thread(self):
        user_input = self.listen()

        if user_input:
            response = self.respond(user_input)
            self.show_response(user_input, response)
        else:
            self.show_response("No input", "Sorry, I didn't hear anything.")

        self.listening = False

    def listen(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)

        try:
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    def respond(self, text):
        if "hello" in text:
            return "Hi there!"
        elif "how are you" in text:
            return "I'm a computer program, so I don't have feelings, but thanks for asking!"
        else:
            return "I didn't understand that."

    def show_response(self, user_input, response):
        messagebox.showinfo("User Input", f"You said: {user_input}\n\nResponse: {response}")
        self.response_label.config(text=f"Response: {response}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    assistant = VoiceAssistantGUI()
    assistant.run()
