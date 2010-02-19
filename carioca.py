# vim: set fileencoding=utf-8:

from collections import namedtuple

JOKER = 0
A, J, Q, K = 1, 11, 12, 13
MONKEYS = (J, Q, K)
SUITES = (SPADES, HEARTS, CLUBS, DIAMONDS) = u'♠♥♣♦'
RANKS = range(1, 14)

Card = namedtuple('Card', ['rank', 'suit'])

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


class InvalidRank(Exception): pass

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
    #nr_jokers = len([card for card in cards
    different_ranks = set(card.rank for card in cards if card.rank != JOKER)
    return (len(cards) >= 3 and len(different_ranks) == 1)

