#Nathan Thompson
#Blackjack



import random
from copy import *
from graphics import *
import os
os.chdir('playing-cards')

win = None


#Loads the graphwin interface, cards, and maintains the chipcount
def main():
    global win
    cards = [2,3,4,5,6,7,8,9,10,"J","Q","K","A",2,3,4,5,6,
             7,8,9,10,"J","Q","K","A",2,3,4,5,6,7,8,9,10,"J","Q",
             "K","A",2,3,4,5,6,7,8,9,10,"J","Q","K", "A"]
    suits = ["S","S","S","S","S","S","S","S","S","S","S","S", "S",
             "C","C","C","C","C","C","C","C","C","C","C","C","C",
             "H","H","H","H","H","H","H","H","H","H","H","H","H",
             "D","D","D","D","D","D","D","D","D","D","D", "D", "D"]
    cards1 = [2,3,4,5,6,7,8,9,10,"J","Q","K","A",2,3,4,5,6,
             7,8,9,10,"J","Q","K","A",2,3,4,5,6,7,8,9,10,"J","Q",
             "K","A",2,3,4,5,6,7,8,9,10,"J","Q","K", "A"]
    suits1 = ["S","S","S","S","S","S","S","S","S","S","S","S", "S",
             "C","C","C","C","C","C","C","C","C","C","C","C","C",
             "H","H","H","H","H","H","H","H","H","H","H","H","H",
             "D","D","D","D","D","D","D","D","D","D","D", "D", "D"]

    win = GraphWin("Blackjack", 800, 500)
    interface(win)
    winobjects = []
    totalchips = 0
    totalwinnings = 0
    handsplayed = 0
    p4 = Point(400, 170)
    message = Text(p4, '')
    message.setSize(21)
    message.setText('How many chips to start with?')
    message.draw(win)
    one = Button(2, '1', win)
    ten = Button(3, '10', win)
    hundred = Button(4, '100', win)
    enter = Button(5, 'Enter', win)
    one.draw()
    ten.draw()
    hundred.draw()
    enter.draw()
    yes = Button(2, 'Yes', win)
    no = Button(3, 'No', win)
    p5 = Point(655, 170)
    chipsmessage = Text(p5, '')
    chipsmessage.setSize(21)
    chipsmessage.draw(win)
    chips = 0
    done = False
    while not done:
        p1 = win.getMouse()
        if one.inrange(p1) == True:
            chips = chips + 1
        if ten.inrange(p1) == True:
            chips = chips + 10
        if hundred.inrange(p1) == True:
            chips = chips + 100
        if enter.inrange(p1) == True:
            done = True
        chipsmessage.setText(commas(str(chips)))
    one.undraw()
    ten.undraw()
    hundred.undraw()
    enter.undraw()
    while True:
        one.draw()
        ten.draw()
        hundred.draw()
        enter.draw()
        finished = False
        done = False
        out = False
        if chips == 0:
            one.undraw()
            ten.undraw()
            hundred.undraw()
            enter.undraw()
            
            while not out: 
                message.setText("Do you want More chips?")
                p1 = win.getMouse()
                if yes.inrange(p1):
                    out = True
                    yes.undraw()
                    no.undraw()
                    one.draw()
                    ten.draw()
                    hundred.draw()
                    enter.draw()
                    ready = False
                    while not ready:
                        message.setText('How many chips?')
                        p1 = win.getMouse()
                        if one.inrange(p1) == True:
                            chips = chips + 1
                        if ten.inrange(p1) == True:
                            chips = chips + 10
                        if hundred.inrange(p1) == True:
                            chips = chips + 100
                        if enter.inrange(p1) == True:
                            ready = True
                        chipsmessage.setText(commas(str(chips)))              
                if no.inrange(p1) == True:
                    print ("Thanks for playing")
                    win.close()
                    return
        out = False
        chipsmessage.setText('')
        while not done:
            bet = 0
            while not out:
                message.setText("You have %s chips. How much do you bet?" % chips)
                p1 = win.getMouse()
                if one.inrange(p1) == True:
                    bet = bet + 1
                if ten.inrange(p1) == True:
                    bet = bet + 10
                if hundred.inrange(p1) == True:
                    bet = bet + 100
                if enter.inrange(p1) == True:
                    out = True
                chipsmessage.setText(commas(str(bet))) 
                if bet > chips:
                    chipsmessage.setText('')
                    bet = 0
                    out = False
                if bet == 0:
                    out = False
                else:
                    done = True
        one.undraw()
        ten.undraw()
        hundred.undraw()
        enter.undraw()
        chipsmessage.setText('')
        message.setText('')
        chips = chips - bet
        hand = blackjack(cards, suits, win, winobjects)
        if hand == "You won!":
            bet = bet + bet * 3 / 2
        if hand == "Dealer Busts." or hand == "You won":
            bet = bet * 2
        if hand == "Bust." or hand == "You lose.":
            bet = 0
        chips = chips + bet
        while not finished:
            message.setText("%s Play Annother hand?" % hand)
            yes.draw()
            no.draw()
            playing = False
            while not playing:
                p1 = win.getMouse()
                if yes.inrange(p1) == True:
                    play = "Y"
                    playing = True
                if no.inrange(p1) == True:
                    play = "N"
                    playing = True
            if play == "Y":
                finished = True
            if play == "N":
                print ("Thanks for playing")
                win.close()
                return
        if len(cards) <= 9:
            cards = copy(cards1)
            suits = copy(suits1)
            print ("Deck reshuffled")
        for obj in winobjects:
            obj.undraw()
        winobjects = []
        
#Plays through one hand of blackjack. It draws from the two list parameters,
# draws in the graph window, and edits a list of winobject for the main()
# function to undraw.
def blackjack(cards, suits, win, winobjects):
    dealer = []
    player = []
    hit = Button(1, 'Hit', win)
    stand = Button(2, 'Stand', win)
    count = Button(7, 'Count', win)
    card1 = random.randint(0,len(cards)-1)
    card2 = random.randint(0,len(cards)-2)
    dealer.append(cards.pop(card1))
    dealer.append(suits.pop(card1))
    dealer.append(cards.pop(card2))
    dealer.append(suits.pop(card2))
    card3 = random.randint(0,len(cards)-1)
    card4 = random.randint(0,len(cards)-2)
    player.append(cards.pop(card3))
    player.append(suits.pop(card3))
    player.append(cards.pop(card4))
    player.append(suits.pop(card4))
    playervalues = handtotal(player)
    total = highestvalue(handtotal(player))
    dealerdrawcard('facedown', 0, win, winobjects)
    dealerdrawcard(str(dealer[2])+dealer[3], 1, win, winobjects)
    playerdrawcard(str(player[0])+player[1], 0, win, winobjects)
    playerdrawcard(str(player[2])+player[3], 1, win, winobjects)
    p1 = Point(75, 425)
    playertotal = Text(p1, '')
    playertotal.setSize(16)
    playertotal.draw(win)
    winobjects.append(playertotal)
    p2 = Point(400,275)
    message = Text(p2, '')
    message.setSize(20)
    message.draw(win)
    winobjects.append(message)
    p3 = Point(742, 251)
    countmsg = Text(p3, '')
    countmsg.setSize(17)
    countmsg.draw(win)
    winobjects.append(message)
    if total == 21:
        return "You won!"
    done = False
    nthcard = 2
    countdraw = False
    hit.draw()
    stand.draw()
    count.draw()
    while not done:
        playertotal.setText(str(total))
        play = ''
        out = False
        message.setText('Hit or Stand?')
        while not out:
            p1 = win.getMouse()
            if hit.inrange(p1) == True:
                play = "hit"
                out = True
            if stand.inrange(p1) == True:
                play = 'stand'
                out = True
            if count.inrange(p1) == True:
                if countdraw == False:
                    countmsg.setText(countcards(cards))
                    countdraw = True
                else:
                    countdraw = False
                    countmsg.setText('')
        if play == "hit":
            newcard = random.randint(0, len(cards)-1)
            player.append(cards.pop(newcard))
            player.append(suits.pop(newcard))
            card = player[-2]
            cardsuit = player[-1]
            playerdrawcard(str(player[-2])+player[-1], nthcard, win, winobjects)
            nthcard = nthcard+1
            if card == "A":
                playervalues = playervalues * 2
                for i in range(len(playervalues)/2):
                    playervalues[i] = playervalues[i]+1
                for i in range(len(playervalues)/2):
                    playervalues[len(playervalues)-i-1] = playervalues[len(playervalues)-i-1] + 11
            else:
                if card == "J" or card == "Q" or card == "K":
                    card = 10
                for i in range(len(playervalues)):
                    playervalues[i] = playervalues[i] + card
            total = highestvalue(playervalues)
            if total == 21:
                done = True
            if total > 21:
                message.setText('')
                hit.undraw()
                stand.undraw()
                count.undraw()
                return "Bust."        
        if play == "stand":
            done = True
    playertotal.setText(str(total))
    hit.undraw()
    stand.undraw()
    count.undraw()
    countmsg.undraw()
    dealervalues = handtotal(dealer)
    dealertotal = highestvalue(handtotal(dealer))
    p3 = Point(75, 125)
    dealertotalscr = Text(p3, '')
    dealertotalscr.setSize(16)
    dealertotalscr.draw(win)
    dealertotalscr.setText(str(dealertotal))
    winobjects.append(dealertotalscr)
    done = False
    nthcard = 2
    dealerdrawcard(str(dealer[0])+dealer[1], 0, win, winobjects)
    message.setText('')
    while not done:
        if dealertotal >= 17:
            done = True
        else:
            newcard = random.randint(0, len(cards)-1)
            dealer.append(cards.pop(newcard))
            dealer.append(suits.pop(newcard))
            card = dealer[-2]
            cardsuit = dealer[-1]
            dealerdrawcard(str(dealer[-2])+dealer[-1], nthcard, win, winobjects)
            nthcard = nthcard +1
            if card == "A":
                dealervalues = dealervalues * 2
                for i in range(len(dealervalues)/2):
                    dealervalues[i] = dealervalues[i]+1
                for i in range(len(dealervalues)/2):
                    dealervalues[len(dealervalues)-i-1] = dealervalues[len(dealervalues)-i-1] + 11
            else:
                if card == "J" or card == "Q" or card == "K":
                    card = 10
                for i in range(len(dealervalues)):
                    dealervalues[i] = dealervalues[i] + card
            dealertotal = highestvalue(dealervalues)
            dealertotalscr.setText(str(dealertotal))
            if dealertotal == 21:
                done = True
            if dealertotal > 21:
                return "Dealer Busts."
    if dealertotal > total:
        return "You lose."
    if dealertotal < total:
        return "You won."
    if dealertotal == total:
        return "Push."

# Takes the inital list of the player's or dealer's hand and returns a list of
# possible values.
    
def handtotal(hand):
    card1 = hand[0]
    card2 = hand[2]
    values = []
    if card1 == "J" or card1 == "Q" or card1 == "K":
        card1= 10
    if card2 == "J" or card2 == "Q" or card2 == "K":
        card2 = 10
    if card1 != "A" and card2 != "A":
        values.append(card1+card2)        
    if card1 == "A" and card2 != "A":
        values.append(11+card2)
        values.append(1+card2)
    if card2 == "A" and card1 != "A":
        values.append(11+card1)
        values.append(1+card1)
    if card2 == "A" and card1 == "A":
        values = [2, 12]
    return values

# Takes a list of values and returns the highest value equal to or less than 21

def highestvalue(values):
    highest = 0
    for value in values:
        if value > highest and value <= 21:
            highest = value
    if highest == 0:
        for value in values:
            if value > highest:
                highest = value
    return highest

# Takes a graphwin object and draws the interface colors and labels

def interface(win):
    p1 = Point(0,0)
    p2 = Point(800,500)
    background = Rectangle(p1,p2)
    background.setFill("Green4")
    background.draw(win)
    p3 = Point(75,75)
    dealer = Text(p3, "Dealer" )
    dealer.setSize(36)
    dealer.draw(win)
    p3 = Point(75,375)
    player = Text(p3, "Player")
    player.setSize(36)
    player.draw(win)
    p4 = Point(0,195)
    p5 = Point(800,220)

# Takes a string that corresponds to a card label, retrives the .gif image,
# and draws it on the graph win at the nth position at the dealer's level.

def dealerdrawcard(card, nthcard, graphwin, winobjects):
    if nthcard < 6:
        p1 = Point(200+100*nthcard, 75)
        Card = Image(p1, card+'.gif')
        Card.draw(graphwin)
        winobjects.append(Card)

# Does the same as the function above, but at the player's level.

def playerdrawcard(card, nthcard, graphwin, winobjects):
    if nthcard <6:
        p1 = Point(200+100*nthcard, 375)
        Card = Image(p1, card+'.gif')
        Card.draw(graphwin)
        winobjects.append(Card)

# Creates an object that will draw a 'button' on the grapwhin at a specific
# position.

class Button(object):

    def __init__(self, pos, label, graphwin):
        self.pos = pos
        self.label = label
        self.graphwin = graphwin

# Draws the button on the grapwin.

    def draw(self):
        x = 100 * self.pos
        self.leftx = x
        self.rightx = x+84
        self.uppery = 200
        self.lowery = 240
        p1 = Point(x,200)
        p2 = Point(x+84,240)
        p3 = Point(x+42,220)
        rec = Rectangle(p1,p2)        
        rec.setFill('Black')
        text = Text(p3, self.label)
        text.setSize(22)
        text.setTextColor('Green4')
        rec.draw(self.graphwin)
        text.draw(self.graphwin)
        self.objects = [rec, text]
        
# Undraws the object

    def undraw(self):
        for obj in self.objects:
            obj.undraw()

# Returns a True or False value if a point object (from a getMouse() operation)
# is in the button's area.

    def inrange(self, point):
        x = point.getX()
        y = point.getY()
        if x > self.leftx and x < self.rightx and y > self.uppery and y < self.lowery:
            return True
        else:
            return False

# Takes a list of card value and returns the hi-low count.
        
def countcards(cards):
    count = 0
    for card in cards:
        if card == 10 or card == 'J' or card == 'Q' or card == 'K' or card == 'A':
            count = count - 1
        elif card < 7:
            count = count + 1
    return str(count)

# Inserts commas into a string of numbers where needed.

def commas(digits):
    if len(digits) <= 3:
        return digits
    else:
        return commas(digits[:-3]) + "," + digits[-3:]
