# vim: set fileencoding=utf-8:

from carioca import *
import unittest

class Trios(unittest.TestCase):
    # valid trios
    def test_trio_different_suits(self):
        self.assertTrue(is_trio(Cs(u'A♠ A♥ A♦')))
    def test_trio_one_repeated_suit(self):
        self.assertTrue(is_trio(Cs(u'7♣ 7♠ 7♣')))
    def test_just_one_suit(self):
        self.assertTrue(is_trio(Cs(u'K♥ K♥ K♥')))
    def test_joker_at_beginning(self):
        self.assertTrue(is_trio(Cs(u'jkr 10♠ 10♦')))
    def test_joker_in_the_middle(self):
        self.assertTrue(is_trio(Cs(u'2♦ jkr 2♣')))

    # invalid trios
    def test_three_different_ranks(self):
        self.assertFalse(is_trio(Cs(u'2♦ 5♠ J♣')))
    def test_two_different_ranks(self):
        self.assertFalse(is_trio(Cs(u'Q♠ A♥ Q♥')))
    def test_two_jokers(self):
        self.assertFalse(is_trio(Cs(u'10♥ jkr jkr')))
    def test_three_jokers(self):
        self.assertFalse(is_trio(Cs(u'jkr jkr jkr')))
    def test_too_short(self):
        self.assertFalse(is_trio(Cs(u'4♣ 4♠')))
    def test_too_long(self):
        self.assertFalse(is_trio(Cs(u'8♥ 8♠ 8♣ 8♦')))


class Straights(unittest.TestCase):
    # valid straights
    def test_simple_straight(self):
        self.assertTrue(is_straight(Cs(u'3♥ 4♥ 5♥ 6♥')))
    def test_with_monkeys(self):
        self.assertTrue(is_straight(Cs(u'9♠ 10♠ J♠ Q♠')))
    def test_start_with_ace(self):
        self.assertTrue(is_straight(Cs(u'A♦ 2♦ 3♦ 4♦')))
    def test_end_with_ace(self):
        self.assertTrue(is_straight(Cs(u'J♣ Q♣ K♣ A♣')))
    def test_wrap_around(self):
        # This decision is based on the results of an informal poll on twitter.
        # Some say this isn't a valid straight.
        self.assertTrue(is_straight(Cs(u'K♥ A♥ 2♥ 3♥')))
    def test_start_with_joker(self):
        self.assertTrue(is_straight(Cs(u'jkr 7♠ 8♠ 9♠')))
    def test_end_with_joker(self):
        self.assertTrue(is_straight(Cs(u'3♠ 4♠ 5♠ jkr')))
    def test_joker_in_the_middle(self):
        self.assertTrue(is_straight(Cs(u'9♣ 10♣ jkr Q♣')))

    # invalid straights
    def test_non_consecutive_ranks(self):
        self.assertFalse(is_straight(Cs(u'2♠ 4♠ 9♠ 10♠')))
    def test_off_by_one(self):
        self.assertFalse(is_straight(Cs(u'5♥ 7♥ 8♥ 9♥')))
    def test_repeated_rank(self):
        self.assertFalse(is_straight(Cs(u'A♦ 2♦ 2♦ 3♦')))
    def test_one_different_suit(self):
        self.assertFalse(is_straight(Cs(u'9♣ 10♣ J♥ Q♣')))
    def test_all_different_suits(self):
        self.assertFalse(is_straight(Cs(u'J♣ Q♠ K♦ A♥')))
    def test_wrong_order(self):
        self.assertFalse(is_straight(Cs(u'2♦ 3♦ 5♦ 4♦')))
    def test_joker_misplaced(self):
        self.assertFalse(is_straight(Cs(u'7♣ 8♣ jkr 9♣')))
    def test_two_jokers(self):
        self.assertFalse(is_straight(Cs(u'4♥ jkr 6♥ jkr')))
    def test_four_jokers(self):
        self.assertFalse(is_straight(Cs(u'jkr jkr jkr jkr')))
    def test_too_short(self):
        self.assertFalse(is_straight(Cs(u'3♠ 4♠ 5♠')))
    def test_too_long(self):
        self.assertFalse(is_straight(Cs(u'3♠ 4♠ 5♠ 6♠ 7♠')))

class CardSubsets(unittest.TestCase):
    # valid subsets
    def test_empty_subset(self):
        self.assertTrue(is_card_subset(Cs(u''), Cs(u'3♥ 5♠ 6♦ J♦')))
    def test_full_subset(self):
        self.assertTrue(is_card_subset(Cs(u'3♥ 5♠ 6♦ J♦'), Cs(u'3♥ 5♠ 6♦ J♦')))
    def test_ordinary_subset(self):
        self.assertTrue(is_card_subset(Cs(u'J♦ 5♠'), Cs(u'3♥ 5♠ 6♦ J♦')))
    def test_repeated_card_in_superset(self):
        self.assertTrue(is_card_subset(Cs(u'10♥ A♠'), Cs(u'A♠ 5♦ Q♣ A♠ 10♥')))
    def test_repeated_card_in_subset_and_superset(self):
        self.assertTrue(is_card_subset(Cs(u'10♥ A♠ A♠'), Cs(u'A♠ 5♦ Q♣ A♠ 10♥')))

    # invalid subsets
    def test_one_card_not_in_superset(self):
        self.assertFalse(is_card_subset(Cs(u'10♥ 3♠ 2♣'), Cs(u'3♠ 10♥ 10♥ K♠')))
    def test_all_cards_not_in_superset(self):
        self.assertFalse(is_card_subset(Cs(u'jkr 3♠ K♦ 2♣'), Cs(u'Q♦ A♠ Q♦ 7♥')))
    def test_empty_superset(self):
        self.assertFalse(is_card_subset(Cs(u'6♣ 7♣ 8♦'), Cs(u'')))
    def test_repeated_card_in_subset(self):
        self.assertFalse(is_card_subset(Cs(u'Q♥ 4♠ Q♥'), Cs(u'4♠ J♦ J♦ Q♥')))


class ConstructorAndRepr(unittest.TestCase):
    def setUp(self):
        self.deck = create_deck()

    def test_invertability(self):
        self.assertEqual(self.deck, [C(card_repr(card)) for card in self.deck])


class Decks(unittest.TestCase):
    def setUp(self):
        self.deck = create_deck()

    def test_deck_size(self):
        self.assertEqual(len(self.deck), 54)
    def test_nr_jokers(self):
        jokers = [card for card in self.deck if card.rank == JOKER]
        self.assertEqual(len(jokers), 2)
    def test_nr_ranks(self):
        ranks = set(card.rank for card in self.deck)
        self.assertEqual(len(ranks), 14)
    def test_all_suits_present(self):
        suits = set(card.suit for card in self.deck if card.suit)
        self.assertEqual(len(suits), 4)


class GameRoundSimpleOperations(unittest.TestCase):
    def setUp(self):
        self.g = GameRound(nr_players=4,
                           nr_trios=1, nr_straights=1,
                           first_turn=3, nr_decks=1)

    def test_card_peeking(self):
        well = self.g.well
        well_size_before = len(well)
        card = self.g.peek_well_card()
        well_size_after = len(well)
        self.assertEqual(card, self.g.well[-1])
        self.assertEqual(well_size_before, well_size_after)

    def _simulate_turn_with_take_function(self, take_fn):
        '''Simulate a turn with a given function
        to take a card (one of take_from_{stack,well})'''

        current_player = self.g.player_in_turn
        hand = self.g.hands[current_player]
        nr_cards_before = len(hand)

        card = take_fn()
        nr_cards_during = len(hand)
        self.assert_(card in hand)

        card_to_drop = hand[0]
        self.g.drop_to_well(card_to_drop)
        nr_cards_after = len(hand)
        self.assertEqual(nr_cards_during, nr_cards_before + 1)
        self.assertEqual(nr_cards_before, nr_cards_after)
        self.assertEqual(card_to_drop, self.g.peek_well_card())
        self.assertNotEqual(current_player, self.g.player_in_turn)

    def test_turn_taking_from_well(self):
        self._simulate_turn_with_take_function(self.g.take_from_well)

    def test_turn_taking_from_stack(self):
        self._simulate_turn_with_take_function(self.g.take_from_stack)


class Lowering(unittest.TestCase):
    def setUp(self):
        g = GameRound(nr_players=2, nr_trios=2, nr_straights=1)

        # cook hands
        g.hands = [Cs(u'5♣ 6♣ 7♣ 8♣   2♥ 2♠ jkr  J♦ J♥ J♦   Q♠ A♣'),
                   Cs(u'3♥ 4♥ 5♥ jkr  A♠ A♣ A♥   7♠ 7♣ 7♦  10♣ K♦')]



if __name__ == "__main__":
    unittest.main()
