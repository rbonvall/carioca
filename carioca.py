# vim: set fileencoding=utf-8:

from collections import namedtuple
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


def C(r):
    '''Convenient constructor for cards from a string argument.

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
    '''Human-friendly card representation.

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

    def take_from_well():
        'Make the player in turn take a card from the well'
        pass
        # [...]
        self.card_taken = True

    def take_from_stack():
        'Make the player in turn take a card from the stack'
        pass
        # [...]
        self.card_taken = True

    def lower(trios=None, straights=None, royal_straights=None):
        'Make the player in turn lower her hands'
        pass

    def drop_to_well(card):
        'Make the player in turn end his turn by dropping a card to the well'
        pass
        # [...]
        self.card_taken = False
        self.player_in_turn += 1
        self.player_in_turn %= self.nr_players

    def discard_to(card, player, lowered_set):
        'Make the player in turn discard one hand to a lowered_set'
        pass

    def _hands_repr(self):
        return [' '.join(map(card_repr, hand)) for hand in self.hands]

    def __repr__(self):
        round = ('ER' if self.nr_royal_straights
                      else '%dT %dE' % (self.nr_trios, self.nr_straights))
        return '<%s instance, %d players, %s, %d decks>' % (
                self.__class__.__name__, self.nr_players, round, self.nr_decks)


