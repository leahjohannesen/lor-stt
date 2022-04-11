import json
import requests
from collections import defaultdict

from core.mouse.mouse import LORMouse
from core.client.assets import AssetManager
from settings import POSITION_URL

# rough boundaries for board zones
ZONES = {
    'hand': (50, 100),
    'board': (260, 260),
    'combat': (450, 450),
    'stack': (595, 605),
    'bgcenter': (720, 720),
    'center': (730, 730),
    'combat|opp': (790, 790),
    'board|opp': (980, 980),
    'hand|opp': (1245, 1255),
    }

ZONE_ORDER = ['hand|opp', 'board|opp', 'combat|opp', 'stack', 'bgcenter', 'center', 'combat', 'board', 'hand']

class LORClient():
    '''
    class for managing the connection to the LOR client
    mostly representing current gamestate
    '''
    def __init__(self):
        self.assman = AssetManager()

    def get_boardstate(self):
        r = requests.get(POSITION_URL)
        return r.json()

    def visualize_boardstate(self, boardstate):
        named = self.add_names(boardstate)
        zoned = self.assign_zones(named)
        srted = self.sort_in_zone(zoned)
        for zone in ZONE_ORDER:
            cardlist = srted.get(zone)
            if cardlist is None:
                continue
            print(zone)
            print(' | '.join((card['name'] for card in cardlist)))
            print('-'*10)

    def sort_in_zone(self, zoned):
        output = {}
        for zone, cardlist in zoned.items():
            output[zone] = sorted(cardlist, key=lambda x: x['TopLeftX'])
        return output

    def add_names(self, boardstate):
        output = []
        for card in boardstate['Rectangles']:
            card_name = self.assman.get_card(card['CardCode'])
            if card_name is None:
                continue
            card['name'] = card_name
            output.append(card)
        return output

    def assign_zones(self, cardlist):
        zoned = defaultdict(list)
        for card in cardlist:
            zone = self.guess_zone(card)
            if zone is None:
                print(f"{card['name']} | ZONE UNDETERMINED, HALP")
                continue
            zoned[zone].append(card)
        return zoned

    def guess_zone(self, card):
        for key, (low, high) in ZONES.items():
            if low <= card['TopLeftY'] <= high:
                return key
        return

    def trace_bs_card(self, ms, bs, idx):
        ms.trace_card(bs['Rectangles'][idx])

    def disp_raw_boardstate(self, boardstate):
        srted = sorted(boardstate['Rectangles'], key=lambda x: x['TopLeftY'])
        for card in srted:
            card_name = self.assman.get_card(card['CardCode'])
            if card_name is None:
                continue
            print(f"{card_name} | x {card['TopLeftX']} | y {card['TopLeftY']}")   

if __name__ == '__main__':
    lorc = LORClient()
    lorm = LORMouse()
    state = lorc.get_boardstate()
    lorc.visualize_boardstate(state)
            
