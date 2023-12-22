# custom_actions.py

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import speech_recognition as sr

class ActionFetchWeather(Action):
    def name(self):
        return "action_fetch_weather"

    def run(self, dispatcher, tracker, domain):
        # Initialize the speech recognition recognizer
        recognizer = sr.Recognizer()

        try:
            # Activate listening to user's speech
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                print("Recognizing...")

            # Use Google Web Speech API to convert speech to text
            user_input = recognizer.recognize_google(audio).lower()

            # Get user location from the recognized text
            location = self.extract_location(user_input)

            if location:
                # Call an external weather API and get the result
                weather_data = self.fetch_weather(location)

                # Send the weather information back to the user
                dispatcher.utter_message(text=f"The weather in {location} is {weather_data}.")
            else:
                dispatcher.utter_message(text="I couldn't determine your location. Please provide a valid location.")

        except sr.UnknownValueError:
            dispatcher.utter_message(text="Sorry, I couldn't understand your speech. Please try again.")
        except sr.RequestError as e:
            dispatcher.utter_message(text=f"Error connecting to the speech recognition service: {e}")
        
        return []

    def extract_location(self, user_input):
        # Implement your logic to extract the location from the user's input
        # For simplicity, let's assume the location is the last word in the input
        words = user_input.split()
        return words[-1]

    def fetch_weather(self, location):
        # Replace with your actual weather API endpoint and API key
        api_key = "YOUR_WEATHER_API_KEY"
        api_endpoint = f"https://api.example.com/weather?location={location}&api_key={api_key}"
        
        # Make a request to the weather API
        response = requests.get(api_endpoint)
        
        if response.status_code == 200:
            # Extract relevant weather information from the API response
            weather_data = response.json().get("weather_description")
            return weather_data
        else:
            return "Sorry, I couldn't retrieve the weather information at the moment."
