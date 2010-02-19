# vim: set fileencoding=utf-8:

from collections import namedtuple

JOKER = 0
A, J, Q, K = 1, 11, 12, 13
MONKEYS = (J, Q, K)
SUITES = (SPADES, HEARTS, CLUBS, DIAMONDS) = u'♠♥♣♦'
RANKS = range(1, 14)

Card = namedtuple('Card', ['rank', 'suit'])

class InvalidRank(Exception): pass
class InvalidSuit(Exception): pass


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
    if suit not in SUITES:
        raise InvalidSuit(u'%s is not a valid suit' % suit)
    letter_values = {u'A': A, u'J': J, u'Q': Q, u'K': K, u'D': 10, u'T': 10}
    if rank_repr in letter_values:
        rank = letter_values[rank_repr]
    else:
        rank = int(rank_repr)
    if rank not in RANKS:
        raise InvalidRank(u'%s is not a valid rank' % rank)

    return Card(rank, suit)


def card_repr(card):
    if card.rank == JOKER:
        return u'JOKER'
    if   card.rank == A: r = u'A'
    elif card.rank == J: r = u'J'
    elif card.rank == Q: r = u'Q'
    elif card.rank == K: r = u'K'
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
    return [Card(rank, suit) for rank in RANKS for suit in SUITES] + jokers

def is_trio(cards):
    nr_jokers = len([card for card in cards if card.rank == JOKER])
    different_ranks = set(card.rank for card in cards if card.rank != JOKER)
    return (len(cards) >= 3 and len(different_ranks) == 1 and nr_jokers <= 1)

