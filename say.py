import pyttsx
engine = pyttsx.init()
engine.setProperty('rate', 70)

def speak(message):
    if not message:
        engine.say('Please provide intput.')
        print('Please provide intput.')
    else:
        engine.say(message)
        print(message)
    engine.runAndWait()
