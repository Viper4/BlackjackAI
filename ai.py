import time
import pynput.keyboard
import re
import math


class Program():
    def __init__(self):
        super().__init__()
        self.active = True
        self.fullyAutomatic = False
        self.standardDeckVals = {"a": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "j": 4, "k": 4, "q": 4}
        self.activeDeckVals = self.standardDeckVals

    def calculateCardVal(self, cards):
        value = 0
        i = 0
        # Calculating value of my and house cards
        for card in cards:
            # Removing card from active deck
            self.activeDeckVals[card] -= 1
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

    def run(self, inputString):
        myCards = []
        houseCards = []
        possibleCards = []

        # Evaluating text
        splitInput = inputString.split(" ")
        myCards = re.findall("([0-9]*[a-z]?)[A-Z]", splitInput[0])
        houseCards = re.findall("([0-9]*[a-z]?)[A-Z]", splitInput[1])

        # Calculating card values according to blackjack
        myValue = self.calculateCardVal(myCards)
        houseValue = self.calculateCardVal(houseCards)

        # Calculating my probability of win
        winProbability = 0
        if myValue != 21:
            valueNeeded = 21 - myValue
            # Listing all possible cards that can be added without bust
            for i in range(1, valueNeeded + 1):
                if i == 1:
                    possibleCards.append("a")
                elif 1 < i < 10:
                    possibleCards.append(str(i))
                elif i >= 10:
                    possibleCards += ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "k", "q"]
            possibleCards = list(set(possibleCards))

            # Calculating probability of drawing any possible card
            totalCards = 0
            for card in possibleCards:
                totalCards += self.activeDeckVals[card]
            probability = totalCards / (52 - len(myCards + houseCards) - 1)
            print("Probability: " + str(probability * 100))
        else:
            winProbability = 1

        print(str(myCards) + ": " + str(myValue) + " | " + str(houseCards) + ": " + str(houseValue) + "\n" + str(winProbability * 100))

program = Program()
program.active = True

while program.active:
    inputString = input("Type my cards then house cards: ")
    if (inputString.lower() == "exit"):
        program.active = False
    else:
        program.run(inputString)
