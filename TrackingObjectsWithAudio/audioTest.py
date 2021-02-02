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


def get_audio():
    r = sr.Recognizer()
    print("test ready")
    connected = False
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = " "

        # print(sr.Microphone(device_index=25))
        while True:
            if not connected:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.setblocking(0)
                try:
                    sock.connect('\0user.audio.test')
                    connected = True
                    print('connected to video server')
                except ConnectionRefusedError:
                    pass
                except BlockingIOError:
                    pass

            try:
                audio = r.listen(source)
                said = r.recognize_google(audio, language="ko-KR")

                print("in audio process: ", said)

                if "안녕" in said:
                    print("Hey!")
                    if connected:
                        try:
                            sock.sendall(said.encode())
                        except:
                            sock.close()
                            connected = False
                            print('disconnected from video server')
                else:
                    print("You shall not pass")

            except Exception as e:
                print("Exception: " + str(e))

    return said

def audio_loop():
    print("start")
    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    speak("hello")

    get_audio()
    # print(text)

    # while True:
    #     text = get_audio().lower()
    #     print(text)
    #     if "안녕" in text:
    #         print("Hey!")
    #     else:
    #         print("You shall not pass")

if __name__ == '__main__':
    audio_loop()
    s.close()