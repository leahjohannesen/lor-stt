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
    return r.json()

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
            print(i)
            print('keypress detected, bailing')
            break
        i += 1
    return

def test_mouse():
    # right -> down -> left -> up, relative
    n = 500
    t = 1
    mouse.move( n, 0, absolute=False, duration=t)
    mouse.move( 0, n, absolute=False, duration=t)
    mouse.move(-n, 0, absolute=False, duration=t)
    mouse.move( 0,-n, absolute=False, duration=t)
    return

if __name__ == '__main__':
    pass