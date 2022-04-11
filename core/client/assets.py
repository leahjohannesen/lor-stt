import json

LOCALIZATION = 'en_us'
SUBDIR = 'core/client/assets/'
SET_JSON_FP = SUBDIR + 'set{set_n}-lite-{loc}/{loc}/data/set{set_n}-{loc}.json'

class AssetManager():
    '''
    manages translating assets, mostly for development
    '''
    n_sets = 5

    def __init__(self):
        self.cardlist, errors = self.load_fresh()
        if errors:
            print('shits whack yo')
            for file_n, card_n, error in errors:
                print(f'{file_n} | {card_n} | {error}')

    def get_card(self, card_code):
        return self.cardlist.get(card_code)

    #def load_cardlist(self):


    def load_fresh(self):
        output = {}
        errors = []
        for set_n in range(1, self.n_sets + 1):
            cardlist, error = self.load_file(set_n)
            # if file load error, bail on the file
            if error is not None:
                errors.append(error)
                continue
            output, set_errors = self.parse_cardlist(set_n, cardlist, output)
            errors += set_errors
        return output, errors

    def parse_cardlist(self, set_n, cardlist, output):
        errors = []
        for i, card in enumerate(cardlist):
            try:
                output[card['cardCode']] = card['name']
            except e:
                errors.append((set_n, i, e))
        return output, errors

    def load_file(self, set_n):
        try:
            with open(SET_JSON_FP.format_map({'set_n': set_n, 'loc': LOCALIZATION}), 'r', encoding='utf-8') as f:
                return json.load(f), None
        except e:
            return None, (set_n, None, e)

             
if __name__ == '__main__':
    full, errors = AssetManager().load_fresh()