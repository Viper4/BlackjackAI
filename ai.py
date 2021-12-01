import time
import re
import math


class Program():
    def __init__(self):
        super().__init__()
        self.active = True
        self.fullyAutomatic = False
        self.standardDeck = {"a": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "j": 4, "k": 4, "q": 4}
        self.activeDeck = self.standardDeck

    def cardToValue(self, cards, removeFromDeck):
        value = 0
        i = 0
        # Calculating values of cards
        for card in cards:
            # Removing card from active deck
            if removeFromDeck:
                self.activeDeck[card] -= 1
            # Numerical cards
            if card.isnumeric():
                value += int(card)
            # Aces
            elif card == "a":
                if i == 0:
                    value += 11
                else:
                    value += 1
            # Jacks, Kings, Queens
            else:
                value += 10
            i += 1
        return value

    def valueToCard(self, values, removeFromDeck):
        # Resetting active deck
        self.activeDeck = self.standardDeck
        print(str(self.activeDeck))

        cards = []
        i = 0
        # Calculating cards corresponding to value
        for value in values:
            if 10 > value > 1:
                cards.append(str(value))
            elif value == 1:
                cards.append("a")
            elif value == 10:
                cards.append += ["10", "j", "k", "q"]
            # Removing value from active deck
            if removeFromDeck:
                self.activeDeck[card] -= 1

    def run(self, inputString):
        self.activeDeck = self.standardDeck
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

        hitProbability = 0
        standProbability = 0
        if myValue != 21:
            ### Calculating my probability of win on hit
            myPossibleCards = []
            myValNeeded = 21 - myValue
            # Listing all possible cards that can be added without bust
            for i in range(1, myValNeeded + 1):
                if i == 1:
                    myPossibleCards.append("a")
                elif 1 < i < 10:
                    myPossibleCards.append(str(i))
                elif i >= 10:
                    myPossibleCards += ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "k", "q"]
            myPossibleCards = list(set(myPossibleCards))

            #print(str(self.activeDeck))

            # Calculating probability of drawing any possible card
            totalCards = 0
            for card in myPossibleCards:
                totalCards += self.activeDeck[card]
            hitProbability = (totalCards - 1) / (52 - len(myCards + houseCards) - 1)

            ### Calculating probability of win if stand
            houseNeededVal = 21 - houseValue
            houseUnknownCard = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "k", "q"]
            # Predicting house unknown card based on assumption of no blackjack
            if houseNeededVal < 10 and self.valueToCard([houseNeededVal], False) in houseUnknownCard:
                houseUnknownCard.remove(houseNeededVal)
            # Calculating probability of win on stand
            totalThreats = 0
            for value in houseUnknownCard:
                if houseValue + self.cardToValue(value, False) > myValue:
                    totalThreats += self.activeDeck[value]
            standProbability = 1 - (totalThreats / (52 - len(myCards + houseCards)))
        else:
            hitProbability = 1

        print("Hit and no bust: " + str(round(hitProbability * 100, 4)) + "%")
        print("Stand and win: " + str(round(standProbability * 100, 4)) + "%")

program = Program()
program.active = True

while program.active:
    inputString = input("Type my cards then house cards: ")
    if (inputString.lower() == "exit"):
        program.active = False
    else:
        program.run(inputString)
