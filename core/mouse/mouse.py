import mouse

MOVE_DUR = 0.001
TRACE_DUR = 0.05
RESOLUTION = (1920, 1080)

def tr(x, y):
    '''
    short name cause gonna ref it a lot
    mouse package refs off top left
    lor refs bot left
    this translates between the two
    '''
    print(x)
    print(y)
    return (x, RESOLUTION[1] - y)

class LORMouse():
    def __init__(self):
        pass

    def trace_card(self, card):
        # move to starting position
        orig_x, orig_y = tr(card['TopLeftX'], card['TopLeftY'])
        mouse.move(orig_x, orig_y, duration=MOVE_DUR)
        card_w = card['Width']
        card_h = card['Height']
        # right -> down -> left -> up, relative
        mouse.move( card_w, 0, absolute=False, duration=TRACE_DUR)
        mouse.move( 0, card_h, absolute=False, duration=TRACE_DUR)
        mouse.move(-card_w, 0, absolute=False, duration=TRACE_DUR)
        mouse.move( 0,-card_h, absolute=False, duration=TRACE_DUR)
        return