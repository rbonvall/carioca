# vim: set fileencoding=utf-8:

from collections import namedtuple, defaultdict
from random import shuffle

JOKER = 0
A, J, Q, K = 1, 11, 12, 13
MONKEYS = (J, Q, K)
SUITS = (SPADES, HEARTS, CLUBS, DIAMONDS) = u'♠♥♣♦'
RANKS = range(1, 14)

LETTER_REPRS = {A: u'A', J: u'J', Q: u'Q', K: u'K'}
LETTER_RANKS = {u'A': A, u'J': J, u'Q': Q, u'K': K, u'D': 10, u'T': 10}

Card = namedtuple('Card', ['rank', 'suit'])

class InvalidRank(ValueError): pass
class InvalidSuit(ValueError): pass
class GameRoundException(StandardError): pass


def C(r):
    u'''Convenient constructor for cards from a string argument.

    >>> C(u'2♥')
    Card(rank=2, suit=u'\\u2665')
    >>> C(u'K♠')
    Card(rank=13, suit=u'\\u2660')
    >>> C(u'10♣')
    Card(rank=10, suit=u'\\u2663')
    >>> C(u'JOKER')
    Card(rank=0, suit=None)
    '''

    r = unicode(r).strip().upper()
    if r.upper().startswith((u'JO', u'JK')):
        return Card(JOKER, None)
    rank_repr, suit = r[:-1], r[-1]
    if suit not in SUITS:
        raise InvalidSuit(u'%s is not a valid suit' % suit)
    if rank_repr in LETTER_RANKS:
        rank = LETTER_RANKS[rank_repr]
    else:
        rank = int(rank_repr)
    if rank not in RANKS:
        raise InvalidRank(u'%s is not a valid rank' % rank)

    return Card(rank, suit)


def Cs(r):
    'Convenient constructor for a list of cards'
    return map(C, r.split())


def card_repr(card):
    u'''Human-friendly card representation.

    >>> card_repr(Card(rank=2, suit=HEARTS))
    u'2♥'
    >>> Card(rank=13, suit=SPADES)
    u'K♠'
    >>> Card(rank=10, suit=CLUBS)
    u'10♣'
    >>> Card(rank=0, suit=None)
    u'JOKER'
    '''

    if card.rank == JOKER:
        return u'JOKER'
    if card.rank in LETTER_REPRS:
        r = LETTER_REPRS[card.rank]
    else:
        r = unicode(card.rank)
    return u'%s%s' % (r, card.suit)


def value(card):
    if 2 <= card.rank <= 10:
        return card.rank
    if card.rank in MONKEYS:
        return 10
    if card.rank == A:
        return 20
    if card.rank == JOKER:
        return 30
    raise InvalidRank('%d is not a valid rank' % card.rank)

def create_deck():
    jokers = [Card(JOKER, None)] * 2
    return [Card(rank, suit) for rank in RANKS for suit in SUITS] + jokers

def are_ranks_consecutive(cards):
    straight_ranks = set((card.rank - n) % 13
                         for n, card in enumerate(cards) if card.rank != JOKER)
    return len(straight_ranks) <= 1

def are_suits_equal(cards):
    different_suits = set(card.suit for card in cards if card.rank != JOKER)
    return len(different_suits) <= 1

def are_ranks_equal(cards):
    different_ranks = set(card.rank for card in cards if card.rank != JOKER)
    return len(different_ranks) <= 1

def count_jokers(cards):
    return len([card for card in cards if card.rank == JOKER])

def is_trio(cards):
    return (len(cards) == 3 and are_ranks_equal(cards) and count_jokers(cards) <= 1)

def is_straight(cards):
    return (len(cards) == 4 and are_suits_equal(cards) and
            are_ranks_consecutive(cards) and count_jokers(cards) <= 1)

def can_give_to_trio(card):
    pass

def can_give_to_straight_at_left(card):
    pass

def can_give_to_straight_at_right(card):
    pass

def is_card_subset(subset, superset):
    '''Check whether all cards in subset are in superset'''

    # in python 2.7 and 3.1, this will be simply:
    # subset_counter   = collections.Counter(subset_counter)
    # superset_counter = collections.Counter(superset_counter)

    subset_counter = defaultdict(int)
    for card in subset:
        subset_counter[card] += 1

    superset_counter = defaultdict(int)
    for card in superset:
        superset_counter[card] += 1

    return all(subset_counter[card] <= superset_counter[card]
               for card in subset_counter)


class GameRound(object):
    def __init__(self, nr_players,
                 nr_trios=0, nr_straights=0, nr_royal_straights=0,
                 first_turn=0, nr_decks=2):
        self.nr_trios = nr_trios
        self.nr_straights = nr_straights
        self.nr_royal_straights = nr_royal_straights
        self.nr_players = nr_players
        self.nr_decks = nr_decks

        self.stack = nr_decks * create_deck()
        shuffle(self.stack)
        self.hands = [[self.stack.pop() for _ in range(12)]
                      for player in range(nr_players)]
        self.lowered_sets = [[[] for _ in range(nr_trios + nr_straights + nr_royal_straights)]
                             for pl in range(nr_players)]
        self.well = [self.stack.pop()]
        self.player_in_turn = first_turn
        self.card_taken = False

    def peek_well_card(self):
        'Peek the card can be taken from the well, without taking it'

        return self.well[-1]

    def take_from_well(self):
        'Make the player in turn take a card from the well'

        taken_card = self.well.pop()
        self.hands[self.player_in_turn].append(taken_card)
        self.card_taken = True
        return taken_card

    def take_from_stack(self):
        'Make the player in turn take a card from the stack'

        taken_card = self.stack.pop()
        self.hands[self.player_in_turn].append(taken_card)
        self.card_taken = True
        return taken_card

    def lower(self, trios=None, straights=None, royal_straights=None):
        'Make the player in turn lower her hands'
        pass

    def drop_to_well(self, card):
        'Make the player in turn end his turn by dropping a card to the well'

        if not self.card_taken:
            raise GameRoundException('Player %d must take a card before dropping' % self.player_in_turn)
        hand = self.hands[self.player_in_turn]
        if card not in hand:
            raise GameRoundException("%s is not in player %d's hand" % (card, self.player_in_turn))

        # drop the card
        self.well.append(card)
        hand.remove(card)

        # end the turn
        self.card_taken = False
        self.player_in_turn += 1
        self.player_in_turn %= self.nr_players

    def give_to(self, card, player, lowered_set):
        'Make the player in turn give one of her cards to a lowered hand'
        pass

    def _hands_repr(self):
        return [' '.join(map(card_repr, hand)) for hand in self.hands]

    def __repr__(self):
        round = ('ER' if self.nr_royal_straights
                      else '%dT %dE' % (self.nr_trios, self.nr_straights))
        return '<%s instance, %d players, %s, %d decks>' % (
                self.__class__.__name__, self.nr_players, round, self.nr_decks)


