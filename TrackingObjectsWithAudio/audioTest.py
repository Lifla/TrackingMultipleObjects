import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound


def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)


def get_audio():
    r = sr.Recognizer()
    print("test ready")
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = " "

        # print(sr.Microphone(device_index=25))
        while True:
            try:
                audio = r.listen(source)
                said = r.recognize_google(audio, language="ko-KR")

                text = said.lower()
                print(text)

                if "안녕" in text:
                    print("Hey!")
                else:
                    print("You shall not pass")

            except Exception as e:
                print("Exception: " + str(e))

    return said


print("start")
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
speak("hello")

get_audio().lower()
# print(text)

# while True:
#     text = get_audio().lower()
#     print(text)
#     if "안녕" in text:
#         print("Hey!")
#     else:
#         print("You shall not pass")