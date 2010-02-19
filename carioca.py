# vim: set fileencoding=utf-8:

from collections import namedtuple

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

