import module_manager
module_manager.review()
import speech_recognition as sr
import pyaudio
import threading

# def callibrator():
r=sr.Recognizer()
print("Callibrating Microphone. Please wait...")
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=5)
# print(thresholdVal)


def audioFunc(audio=None):
    # r = sr.Recognizer()
    # r.energy_threshold=thresholdVal
    with sr.Microphone() as source:
        print("Say something: ")
        audio = r.listen(source)
        print("Time over. Thanks!")
        string="wrong"
        string=r.recognize_google(audio)
    try:
        print("TEXT: "+string)
    except:
        print("OOPS! Didn't catch that...")
    return string

def checkSet():
    audio=str(audioFunc())
    # commandSet.add(audio)
    allowedCommands={"jump", "jumps", "dump", "dumb", 
                    "job", "John", "john", "jump jump", 
                    "jump jump jump", "jump jump jump jump"}
    if(audio not in allowedCommands):
        print("here")
        return False
    return True

def mainFunc():
    ifJump=True
    # thresholdVal=callibrator()
    while(ifJump):
        ifJump = checkSet()

# thread1=threading.Thread(target = audioFunc, args = ())
# thread2=threading.Thread(target = mainFunc(), args = ())
# thread1.start()
# thread2.start()
mainFunc()