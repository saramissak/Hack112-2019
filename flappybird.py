
import speech_recognition as sr
import pyaudio
import threading

def audioFunc(audio=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something: ")
        audio = r.listen(source)
        print("Time over. Thanks!")
        string=r.recognize_google(audio)
    try:
        print("TEXT: "+string)
    except:
        print("OOPS! Didn't catch that...")
    return string

# thread1=threading.Thread(target = audioFunc(), args = ())
# thread1.start()

def checkSet(commandSet=set()):
    audio=str(audioFunc())
    commandSet.add(audio)
    if(not (len(commandSet)==1 and ("jump" in commandSet))):
        return False
    return True

def mainFunc():
    ifJump=True
    commandSet=set()
    while(ifJump):
        ifJump = checkSet(commandSet)

mainFunc()