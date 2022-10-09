class CaseRarity:
    def __init__(self, name, prob):
        self.name = name
        self.prob = prob


RARITIES = [CaseRarity(name='common', prob=1), CaseRarity(name='rare', prob=5),
            CaseRarity(name='epic', prob=20), CaseRarity(name='legendary', prob=100)]

RARITY_TO_PROB = {case.name: case.prob for case in RARITIES}
