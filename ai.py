import time
import re
import math


class Program():
    def __init__(self):
        super().__init__()
        self.active = True
        self.fullyAutomatic = False
        self.activeDeck = {"a": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "j": 4, "k": 4, "q": 4}

    def cardToValue(self, cards, removeFromDeck):
        value = 0
        i = 0
        a = 0
        # Calculating values of cards
        for card in cards:
            # Removing card from active deck
            if removeFromDeck and self.activeDeck[card] > 0:
                self.activeDeck[card] -= 1
            # Numerical cards
            if card.isnumeric():
                value += int(card)
            # Aces
            elif card == "a":
                if cards.count("a") > 1 and a != 0:
                    value += 1
                else:
                    value += 11
                a = i
            # Jacks, Kings, Queens
            else:
                value += 10
            i += 1
        return value

    def valueToCard(self, values, removeFromDeck):
        cards = []
        i = 0
        # Calculating cards corresponding to value
        for value in values:
            card = ""
            if 10 > value > 1:
                card = str(value)
            elif value == 1:
                card = "a"
            elif value == 10:
                card = "10"
            cards.append(card)
            # Removing value from active deck
            if removeFromDeck:
                self.activeDeck[card] -= 1

    def run(self, inputString):
        self.activeDeck = {"a": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "j": 4, "k": 4, "q": 4}
        print(str(self.activeDeck))
        myCards = []
        houseCards = []

        # Evaluating text
        splitInput = inputString.split(" ")
        myCards = re.findall("([0-9]*[a-z]?)[A-Z]", splitInput[0])
        houseCards = re.findall("([0-9]*[a-z]?)[A-Z]", splitInput[1])

        # Calculating card values according to blackjack
        myValue = self.cardToValue(myCards, True)
        houseValue = self.cardToValue(houseCards, True)

        if myValue != 21:
            print("2 Hits and no bust " + str(self.simulateHit(myValue, myCards, houseCards, -1, 1)))

            ### Calculating probability of win if stand
            houseNeededVal = 21 - houseValue
            houseUnknownCard = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "k", "q"]
            # Predicting house unknown card based on assumption of no blackjack
            if houseNeededVal < 10 and self.valueToCard([houseNeededVal], False) in houseUnknownCard:
                houseUnknownCard.remove(houseNeededVal)
            # Calculating probability of win on stand
            totalThreats = 0
            for card in houseUnknownCard:
                if houseValue + self.cardToValue(card, False) > myValue:
                    totalThreats += self.activeDeck[card]
            standProbability = 1 - (totalThreats / (52 - len(myCards + houseCards)))
        else:
            hitProbability = 0
            standProbability = 1

        #print("Hit and no bust: " + str(round(hitProbability * 100, 4)) + "%")
        print("Stand and win: " + str(round(standProbability * 100, 4)) + "%")
        print(str(myValue))

    def simulateHit(self, myValue, myCards, houseCards, noBustProbability, iterations):
        deck = {"a": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "j": 4, "k": 4, "q": 4}

        for card in myCards + houseCards:
            if deck[card] > 0:
                deck[card] -= 1

        if myValue < 21:
            ### Calculating my probability of no bust on hit
            myPossibleCards = []
            myValNeeded = 21 - myValue
            # Listing all possible cards that can be added without bust
            for val in range(1, myValNeeded + 1):
                if val == 1:
                    myPossibleCards.append("a")
                elif 1 < val < 10:
                    myPossibleCards.append(str(val))
                elif val >= 10:
                    myPossibleCards += ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "k", "q"]
            myPossibleCards = list(set(myPossibleCards))

            # Calculating probability of drawing any possible non-bust card
            totalPosCards = 0
            for card in myPossibleCards:
                totalPosCards += deck[card]

            if noBustProbability != -1:
                noBustProbability *= (totalPosCards) / (52 - len(myCards + houseCards) - 1)
            else:
                noBustProbability = (totalPosCards) / (52 - len(myCards + houseCards) - 1)

            print(str(myCards) + ": " + str(noBustProbability))

            for card in myPossibleCards:
                newCards = myCards + [card]
                newValue = self.cardToValue(newCards, False)
                if iterations > 0:
                    self.simulateHit(newValue, newCards, houseCards, noBustProbability, iterations - 1)
        else:
            print(str(myCards) + ": 0")

program = Program()
program.active = True

while program.active:
    inputString = input("Type my cards then house cards: ")
    if (inputString.lower() == "exit"):
        program.active = False
    else:
        program.run(inputString)
