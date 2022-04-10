import requests
import keyboard
import speech_recognition as sr
import mouse

PORT = 21337
LOCAL_BASE = f'http://127.0.0.1:{PORT}'
POSITION_URL = f'{LOCAL_BASE}/positional-rectangles'
PUSH_TO_TALK_KEY = 'q'
TIMEOUT = 10000


def check_api():
    r = requests.get(POSITION_URL)
    return r

def test_mic():
    r = sr.Recognizer()
    # number of seconds to wait before bailing
    r.pause_threshold = 2
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
    try:
        print(r.recognize_google(audio))
    except sr.RequestError:
        print('sr | api unreachable')
    except sr.UnknownValueError:
        print('sr | unable to recognize')
    return

def test_keyboard():
    i = 0
    while i < TIMEOUT:
        if keyboard.is_pressed(PUSH_TO_TALK_KEY):
            print('keypress detected, bailing')
            break
    return

def test_mouse():
    # right -> down -> left -> up, relative
    mouse.move( 100,   0, absolute=False, duration=0.1)
    mouse.move(   0, 100, absolute=False, duration=0.1)
    mouse.move(-100,   0, absolute=False, duration=0.1)
    mouse.move(   0,-100, absolute=False, duration=0.1)
    return

if __name__ == '__main__':
    pass