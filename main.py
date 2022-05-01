
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card():
    '''
    Card representation.
    '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[self.rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit + ': ' + str(self.value)


class Deck():
    '''
    Deck representation.
    '''

    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.cards.append(card)

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        deck_comp = ""
        for card in self.cards:
            deck_comp += '\n'+str(card)

        return deck_comp

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        single_card = self.cards.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self, total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips you wanna bet: '))
            if chips.bet > chips.total:
                print(
                    f'Inssuficient chips. Sorry. You have available: {chips.total}')
            else:
                break
        except:
            print('Sorry please provide an integer')


def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input('Hit or Stand ? Enter h or s')
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print('Player stands. Dealers turn')
            playing = False
        else:
            print('Sorry i did not understand that')
            continue

        break


def show_some(player, dealer):
    print(f"\nDealer's cards: ")
    print(f"First card is hidden ")
    print(dealer.cards[1])

    print(f"\nPlayer's cards: ")

    for card in player.cards:
        print(card)


def show_all(player, dealer):

    print(f"\nDealers's cards: ", *dealer.cards, sep="\n")
    print(f'Value of dealer cards: {dealer.value}')
    print(f"\nPlayer's cards: ", *player.cards)
    print(f'Value of player cards: {player.value}', sep="\n")


def player_busts(player, dealer, chips):
    print('BUST PLAYER')
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print('WIN PLAYER')
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print('BUST DEALER')
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print('WIN DEALER')
    chips.lose_bet()


def push(player, dealer):
    print('Dealer and Player tie! PUSH!')


while True:
    # Print an opening statement
    print('Welcome to blackjack')
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    # Inform Player of their chips total
    print(f'Total Chips:{player_chips.total}')
    # Ask to play again
    new_game = input('Would you like another hand? y/n')
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        'Thanks for playing'
        break
