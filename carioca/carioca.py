# vim: set fileencoding=utf-8 tabstop=4 expandtab:

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

TURN_SETS = [
 (2,0,0),
 (1,1,0),
 (0,2,0),
 (3,0,0),
 (2,1,0),
 (1,2,0),
 (4,0,0),
 (0,3,0),
 (0,0,1)
]

class InvalidRank(ValueError): pass
class InvalidSuit(ValueError): pass
class GameRoundException(StandardError): pass
class InvalidMoveException(StandardError): pass

############################
# Convenience constructors #
############################
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
    if r.startswith((u'JO', u'JK')):
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


#####################
# Auxiliary methods #
#####################
def is_joker(card):
    return card.rank == JOKER

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

    if is_joker(card):
        return u'JOKER'
    if card.rank in LETTER_REPRS:
        r = LETTER_REPRS[card.rank]
    else:
        r = unicode(card.rank)
    return r + card.suit

def card_set_repr(cards):
    return u'[' + ','.join(map(card_repr, cards)) + u']'

def value(card):
    if 2 <= card.rank <= 10:
        return card.rank
    if card.rank in MONKEYS:
        return 10
    if card.rank == A:
        return 20
    if is_joker(card):
        return 30
    raise InvalidRank('%d is not a valid rank' % card.rank)

def get_score(cards):
    '''Calculates the score corresponding to a card set'''
    score = 0
    for card in cards:
        score += value(card)
    return score

def create_deck():
    jokers = [Card(JOKER, None)] * 2
    return [Card(rank, suit) for rank in RANKS for suit in SUITS] + jokers

def are_ranks_consecutive(cards):
    straight_ranks = set((card.rank - n) % 13
                         for n, card in enumerate(cards) if not is_joker(card))
    return len(straight_ranks) <= 1

def are_suits_equal(cards):
    different_suits = set(card.suit for card in cards if not is_joker(card))
    return len(different_suits) <= 1

def are_ranks_equal(cards):
    different_ranks = set(card.rank for card in cards if not is_joker(card))
    return len(different_ranks) <= 1

def count_jokers(cards):
    return len([card for card in cards if is_joker(card)])

def is_trio(cards):
    return (len(cards) == 3 and are_ranks_equal(cards) and count_jokers(cards) <= 1)

def is_straight(cards):
    return (len(cards) == 4 and are_suits_equal(cards) and
            are_ranks_consecutive(cards) and count_jokers(cards) <= 1)

def is_royal_straight(cards):
    cards.sort(cmp=lambda x,y: cmp(x.rank, y.rank))
    return (len(cards) == 13 and are_suits_equal(cards) and
            are_ranks_consecutive(cards) and count_jokers(cards) <= 1)

def can_give_to_trio(card, trio):
    return are_ranks_equal(trio + [card])

def has_jokers_too_close(cards):
    lastJoker = None
    for n, card in enumerate(cards):
        if is_joker(card):
            if lastJoker is not None and n - lastJoker <= 2:
                return True
            lastJoker = n
    return False

def can_give_to_straight_at_left(card, straight):
    cards = [card] + straight
    return (not has_jokers_too_close(cards) and are_suits_equal(cards)
            and are_ranks_consecutive(cards))

def can_give_to_straight_at_right(card, straight):
    cards = straight + [card]
    return (not has_jokers_too_close(cards) and are_suits_equal(cards)
            and are_ranks_consecutive(cards))

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

class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.trios = []
        self.straights = []

    def clear(self):
        self.hand[:] = []
        self.trios[:] = []
        self.straights[:] = []

    def deal(self, cards):
        self.hand.extend(cards)

    def __repr__(self):
        return '<Player %s>' % self.name


class GameRound(object):
    def __init__(self, nr_players,
                 nr_trios=0, nr_straights=0, nr_royal_straights=0,
                 first_turn=0, nr_decks=2):

        self.nr_trios = nr_trios
        self.nr_straights = nr_straights
        self.nr_royal_straights = nr_royal_straights
        self.nr_players = nr_players
        self.nr_decks = nr_decks

        # Information about lowered cards and players
        self.did_lower = [False for pl in range(nr_players)]
        self.lowered_trios = [None for pl in range(nr_players)]
        self.lowered_straights = [None for pl in range(nr_players)]
        self.lowered_royal_straights = [None for pl in range(nr_players)]

        # Initialize the cards for this round
        self.stack = nr_decks * create_deck()
        shuffle(self.stack)
        self.hands = [[self.stack.pop() for _ in range(12)]
                      for player in range(nr_players)]
        self.well = [self.stack.pop()]

        # Setup initial playing conditions
        self.played_first_turn = [False for pl in range(nr_players)]
        self.player_in_turn = first_turn
        self.card_taken = False

        self.scores = [None for pl in range(nr_players)]

    def peek_well_card(self):
        'Peek the card can be taken from the well, without taking it'

        return self.well[-1]

    def take_from_well(self):
        'Make the player in turn take a card from the well'

        if self.card_taken:
            raise InvalidMoveException('Cannot take another card, already took one')

        taken_card = self.well.pop()
        self.hands[self.player_in_turn].append(taken_card)
        self.card_taken = True
        return taken_card

    def take_from_stack(self):
        'Make the player in turn take a card from the stack'

        if self.card_taken:
            raise InvalidMoveException('Cannot take another card, already took one')

        taken_card = self.stack.pop()
        self.hands[self.player_in_turn].append(taken_card)
        self.card_taken = True
        return taken_card

    def lower(self, trios=[], straights=[], royal_straights=[]):
        'Make the player in turn lower her hands'

        if not self.card_taken:
            raise InvalidMoveException('Cannot lower without taking a card first')

        player = self.player_in_turn

        if not self.played_first_turn[self.player_in_turn]:
            raise InvalidMoveException('Cannot lower during the first turn, have to wait until the second at least')

        if self.did_lower[player]:
            raise GameRoundException('Player %d already lowered' % player)

        if self.nr_trios:
            if any(not is_trio(cards) for cards in trios):
                raise GameRoundException('Invalid trio in %s' % card_set_repr(cards))
            if len(trios) != self.nr_trios:
                raise GameRoundException('%d trios are needed, only %d provided' %
                                         (self.nr_trios, len(trios)))
        if self.nr_straights:
            if any(not is_straight(cards) for cards in straights):
                raise GameRoundException('Invalid straight in %s' % card_set_repr(cards))
            if len(straights) != self.nr_straights:
                raise GameRoundException('%d straights are needed, only %d provided' %
                                         (self.nr_straights, len(straights)))
        if self.nr_royal_straights:
            if any(not is_royal_straight(cards) for cards in royal_straights):
                raise GameRoundException('Invalid royal straight in %s' % card_set_repr(rcards))
            if len(royal_straights) != self.nr_royal_straights:
                raise GameRoundException('%d royal straights are needed, only %d provided' %
                                         (self.nr_royal_straights, len(royal_straights)))

        hand = self.hands[player]

        cards_to_lower = [card for item in (trios, straights, royal_straights)
                               for cards in item
                               for card in cards]
        if not is_card_subset(cards_to_lower, hand):
            raise GameRoundException('Not all cards are in hand')
        self.lowered_trios[player] = trios
        self.lowered_straights[player] = straights
        for card in cards_to_lower:
            hand.remove(card)
        self.did_lower[player] = True


    def drop_to_well(self, card):
        'Make the player in turn end his turn by dropping a card to the well'

        if not self.card_taken:
            raise InvalidMoveException('Player %d must take a card before dropping' % self.player_in_turn)
        hand = self.hands[self.player_in_turn]
        if card not in hand:
            raise GameRoundException("%s is not in player %d's hand" % (card_repr(card), self.player_in_turn))

        # drop the card
        self.well.append(card)
        hand.remove(card)

        # end the turn
        self.card_taken = False
        self.played_first_turn[self.player_in_turn] = True
        self.player_in_turn += 1
        self.player_in_turn %= self.nr_players

    def give_to(self, card, player, lowered_set, where=None):
        'Make the player in turn give one of her cards to a lowered hand'

        if not self.card_taken:
            raise InvalidMoveException('Cannot give cards without taking a card first')

        # Players that haven't lowered any cards can't give cards
        if not self.did_lower[self.player_in_turn]:
            raise InvalidMoveException('Player %d hasn\'n lowered yet' % player)

        # Check that given card is in the current player's hand
        hand = self.hands[self.player_in_turn]
        if card not in hand:
            raise GameRoundException("%s is not in player %d's hand" % (card_repr(card), self.player_in_turn))

        # Check that given lowered set in in the given player's lowered sets
        found = False
        if self.lowered_trios[player] is not None:
            for sset in self.lowered_trios[player]:
                if is_card_subset(lowered_set, sset) and len(lowered_set) == len(sset):
                    lowered_set = sset
                    found = True
                    break
        if not found:
            if self.lowered_straights[player] is not None:
                for sset in self.lowered_straights[player]:
                    if is_card_subset(lowered_set, sset) and len(lowered_set) == len(sset):
                        lowered_set = sset
                        found = True
                        break
        if not found:
            raise GameRoundException("Given set of cards %s not in player %d's lowered sets" % (lowered_set, player))

        # Give card
        if can_give_to_trio(card, lowered_set):
            lowered_set.append(card)
            hand.remove(card)
        elif (where is None or where == 'left') and can_give_to_straight_at_left(card, lowered_set):
            lowered_set.insert(0,card)
            hand.remove(card)
        elif (where is None or where == 'right') and can_give_to_straight_at_right(card, lowered_set):
            lowered_set.append(card)
            hand.remove(card)
        else:
            raise GameRoundException("Cannot put %s in the lowered set %s of player %d" % (card_repr(card), lowered_set, player))


    def is_over(self):
        'Checks if the current game round is over'

        for hand in self.hands:
            if len(hand) == 0:
                return True
        return False

    def calculate_scores(self):
        'Calculates the final scores for all players on this turn'

        if not self.is_over():
            raise GameRoundException('Round is not over yet, cannot calculate each player\'s score')

        for i in range(self.nr_players):
            self.scores[i] = get_score(self.hands[i])

    def __repr__(self):
        round = ('ER' if self.nr_royal_straights
                      else '%dT %dE' % (self.nr_trios, self.nr_straights))
        return '<%s instance, %d players, %s, %d decks>' % (
                self.__class__.__name__, self.nr_players, round, self.nr_decks)



'''
A CariocaGame drives the process of playing a round,
finish it, and finally check that the game is over.
'''
class CariocaGame(object):

    def __init__(self, nr_players, nr_decks=2):
        self._nr_players = nr_players
        self._current_round = None
        self._current_round_nr = 0
        self._nr_decks = nr_decks
        self._first_turn = 1 # random() % nr_players

    def is_over(self):
        return (self._current_round_nr > len(TURN_SETS))

    def go_to_next_round(self):

        if self.is_over():
            raise GameException('No more rounds available, cannot go to a next round')

        # Create new round, and update who's going to play first in the next round
        current_set = TURN_SETS[self._current_round_nr]
        self._current_round = GameRound(self._nr_players,
                               current_set[0], current_set[1], current_set[2],
                               self._first_turn, self._nr_decks)
        self._current_round_nr += 1
        self._first_turn += 1

        return self._current_round

    def get_current_game(self):
        return self._current_round
