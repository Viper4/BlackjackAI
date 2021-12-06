import time
import re

simulationDepth = 3


class Program():
    def __init__(self):
        super().__init__()
        self.active = True
        self.fullyAutomatic = False
        self.activeDeck = {"a": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "j": 4, "k": 4, "q": 4}

    def cardToValues(self, cards):
        values = 0
        i = 0
        # Calculating valuess of cards
        for card in cards:
            if card != "x":
                # Numerical cards
                if card.isnumeric():
                    values += int(card)
                # Aces
                elif card == "a":
                    if i == 0:
                        values += 11
                    else:
                        values += 1
                # Jacks, Kings, Queens
                else:
                    values += 10
                i += 1
        return values

    def valuesToCard(self, valuess):
        # Resetting active deck
        self.activeDeck = {"a": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "j": 4, "k": 4, "q": 4}

        cards = []
        # Calculating cards corresponding to values
        for values in valuess:
            if 10 > values > 1:
                cards.append(str(values))
            elif values == 1 or values == 11:
                cards.append("a")
            elif values == 10:
                cards.append += ["10", "j", "k", "q"]

    def hitProbability(self, myValue, unknownCards, deck):
        valNeeded = 21 - myValue
        myPossibleCards = []
        hitProbabilities = []

        # Listing all possible cards that can be added without bust
        for i in range(1, valNeeded + 1):
            if i == 1:
                myPossibleCards.append("a")
            elif 1 < i < 10:
                myPossibleCards.append(str(i))
            elif i >= 10:
                myPossibleCards += ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "k", "q"]
        myPossibleCards = list(set(myPossibleCards))

        # Calculating probability of drawing any possible card
        totalPosCards = 0
        for card in myPossibleCards:
            totalPosCards += deck[card]
        # Assuming that unknown cards are not in totalPosCards
        hitProbabilities.append(totalPosCards / (sum(deck.values()) - unknownCards))
        # Assuming that i unknown cards are in totalCards
        if unknownCards > 0:
            for i in range(1, unknownCards):
                hitProbabilities.append((totalPosCards - i) / (sum(deck.values()) - unknownCards + i))
        # Averaging hitProbabilities
        return sum(hitProbabilities) / len(hitProbabilities)

    # Simulating probability of dealer winning
    def simulateDealerHit(self, myCards, myValue, houseCards, houseValue, otherCards, layer):
        time.sleep(0.001)
        unknownCards = 0
        housePossibleCards = []
        valNeeded = 21 - myValue

        # Creating simulated deck based on cards already taken
        simulatedDeck = {"a": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "j": 4, "k": 4, "q": 4}
        for card in myCards + houseCards + otherCards:
            if card != "x":
                simulatedDeck[card] -= 1
            else:
                unknownCards += 1

        # Listing all possible cards that can be added without bust
        for i in range(1, valNeeded + 1):
            if i == 1:
                housePossibleCards.append("a")
            elif 1 < i < 10:
                housePossibleCards.append(str(i))
            elif i >= 10:
                housePossibleCards += ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "k", "q"]
        housePossibleCards = list(set(housePossibleCards))

        # Probability of getting any possible card that would exceed player values
        totalWinCards = 0
        for card in housePossibleCards:
            if houseValue + self.cardToValues(card) > myValue:
                totalWinCards += self.activeDeck[card]
        winProbability = totalWinCards / sum(simulatedDeck.values())

        # Simulate another hit based on below conditions. Dealer usually hits until at least 17 val
        if winProbability < 0.1 and len(housePossibleCards) > 0 and layer < simulationDepth and houseValue < 17:
            for card in housePossibleCards:
                value = self.cardToValues(card)
                winProbability += self.simulateDealerHit(myCards, myValue, houseCards + [card], houseValue + value, otherCards, layer + 1)
            # Averaging win probabilities from all possibilities
            return winProbability / (len(housePossibleCards) + 2)
        else:
            return winProbability

    def run(self, inputString):
        self.activeDeck = {"a": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "j": 4, "k": 4, "q": 4}
        hands = {}
        values = {}
        unknownCards = 0

        # Evaluating text and storing the hands of all players
        splitInput = inputString.split(" ")
        for string in splitInput:
            if "H:" in string:
                hands["House"] = re.sub("H:", "", string).split(",")
                # Calculating card values according to blackjack
                values["House"] = self.cardToValues(hands["House"])
                for card in hands["House"]:
                    if card != "x":
                        self.activeDeck[card] -= 1
                    else:
                        unknownCards += 1
            else:
                key = re.match("P[0-9]*", string).group()
                hands[key] = re.sub("P[0-9]*:", "", string).split(",")
                # Calculating card values according to blackjack
                values[key] = self.cardToValues(hands[key])
                for card in hands[key]:
                    if card != "x":
                        self.activeDeck[card] -= 1
                    else:
                        unknownCards += 1

        for player, cards in hands.items():
            if player != "House":
                if values[player] < 21:
                    # Calculating this player's probability of win on hit
                    hitProbability = self.hitProbability(values[player], unknownCards, self.activeDeck)

                    # Calculating probability of win if stand
                    otherCards = []
                    # Getting cards of all other players besides house and this player
                    for key, val in hands.items():
                        if key != player and key != "House":
                            otherCards += val
                    standProbability = 1 - self.simulateDealerHit(cards, values[player], hands["House"], values["House"], otherCards, 0)

                    # Calculating probability of win on double down
                    doubleDownProbability = 0
                    if "a" not in hands["House"]:
                        if values[player] == 11:
                            doubleDownProbability = 0.99
                        elif values[player] == 10:
                            doubleDownProbability = 0.8
                        elif values[player] == 9:
                            doubleDownProbability = 0.4
                        elif "a" in hands[player] and 18 >= values[player] >= 16:
                            if values["House"] <= 6:
                                doubleDownProbability = 0.7
                    # Subtracting probability of dealer getting ace
                    doubleDownProbability *= self.activeDeck["a"] / sum(self.activeDeck.values())
                else:
                    hitProbability = 0
                    standProbability = 1
                    doubleDownProbability = 0
                print("------------\n" + player + " Results\n Hit: " + str(round(hitProbability * 100, 3)) + "%\n Stand: " + str(round(standProbability * 100, 3)) + "%\n Double down: " + str(round(doubleDownProbability * 100, 3)) + "%")

program = Program()
program.active = True

while program.active:
    inputString = input("Type my cards then house cards: ")
    if inputString.lower() == "exit" or inputString.lower() == "/e":
        print("Exiting\n------------")
        program.active = False
    elif inputString.lower() == "help" or inputString.lower() == "/h":
        print("------------\nHelp\nSyntax:\n a=ace (1 or 11)\n 2-10=respective number\n j=jack (10)\n k=king (10)\n q=queen (10)\n x=unknown card\nHow to use: Type players cards denoting yourself as 'P1' and house cards.\n Ex: 'P1:6,a P2:3,j H:k,x'\nHow to play: https://bicyclecards.com/how-to-play/blackjack/\n------------")
    else:
        program.run(inputString)
    time.sleep(0.01)
