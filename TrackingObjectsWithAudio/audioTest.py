import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound
import socket


def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)


def get_audio(sock):
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

                print("in audio process: ", said)

                if "안녕" in said:
                    print("Hey!")
                    sock.sendall(said.encode())
                else:
                    print("You shall not pass")

            except Exception as e:
                print("Exception: " + str(e))

    return said

def audio_loop(sock):
    print("start")
    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    speak("hello")

    get_audio(sock)
    # print(text)

    # while True:
    #     text = get_audio().lower()
    #     print(text)
    #     if "안녕" in text:
    #         print("Hey!")
    #     else:
    #         print("You shall not pass")

if __name__ == '__main__':
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect('\0user.audio.test')
        audio_loop(s)