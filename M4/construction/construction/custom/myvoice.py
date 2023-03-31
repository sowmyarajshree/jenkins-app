import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

# Capture voice input
with sr.Microphone() as source:
    print("Speak now...")
    audio = r.listen(source)

# Convert voice input to text
try:
    text = r.recognize_google_cloud(audio, language="en-US")
    print("You said:", text)
except sr.UnknownValueError:
    print("Google Cloud Speech-to-Text could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech-to-Text service; {0}".format(e))

# Process text input
# Add your code here
