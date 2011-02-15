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

class ScoreTest(unittest.TestCase):
    def test_get_score_for_empty_hand(self):
        self.assertEquals(get_score(Cs(u'')), 0)
    def test_get_score_for_one_card(self):
        self.assertEquals(get_score(Cs(u'2♣')), 2)
        self.assertEquals(get_score(Cs(u'3♥')), 3)
        self.assertEquals(get_score(Cs(u'J♠')), 10)
        self.assertEquals(get_score(Cs(u'Q♦')), 10)
        self.assertEquals(get_score(Cs(u'K♣')), 10)
        self.assertEquals(get_score(Cs(u'A♥')), 20)
        self.assertEquals(get_score(Cs(u'jkr')), 30)
    def test_get_score_hands_with_cards(self):
        self.assertEquals(get_score(Cs(u'A♥ 3♣ Q♥ jkr jkr 8♦ J♠')), 111)
        self.assertEquals(get_score(Cs(u'2♥ 3♣ 3♥ 2♦ 8♠ 9♦')), 27)
        self.assertEquals(get_score(Cs(u'7♠ 8♠ 9♠ 10♠  7♥ 7♠ 7♦  3♣ A♣ 9♦ 8♦ 7♦')), 102)

class Joker(unittest.TestCase):
    def test_jokers_not_too_close(self):
        self.assertFalse(has_jokers_too_close(Cs(u'jkr A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'jkr A♥ A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'jkr A♥ A♥ A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'A♥ jkr A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'A♥ jkr A♥ A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'A♥ jkr A♥ A♥ A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'A♥ A♥ jkr A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'A♥ A♥ jkr A♥ A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'A♥ A♥ jkr A♥ A♥ A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'jkr A♥ A♥ jkr A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'jkr A♥ A♥ jkr A♥ A♥ A♥ jkr')))
        self.assertFalse(has_jokers_too_close(Cs(u'jkr A♥ A♥ jkr A♥ A♥ A♥ A♥ jkr')))
    def test_jokers_too_close(self):
        self.assertTrue(has_jokers_too_close(Cs(u'jkr jkr')))
        self.assertTrue(has_jokers_too_close(Cs(u'jkr A♥ jkr')))
        self.assertTrue(has_jokers_too_close(Cs(u'jkr A♥ A♥ jkr jkr')))
        self.assertTrue(has_jokers_too_close(Cs(u'jkr A♥ A♥ jkr A♥ jkr')))

class CardContributor(unittest.TestCase):
    # valid trio contributions
    def test_valid_simple_contribution_to_trio(self):
        self.assertTrue(can_give_to_trio(C(u'4♠'), Cs(u'4♥ 4♦ 4♥')))
    def test_valid_joker_contribution_to_trio(self):
        self.assertTrue(can_give_to_trio(C(u'jkr'), Cs(u'4♥ 4♦ 4♥')))
    def test_valid_simple_contribution_to_trio_with_joker(self):
        self.assertTrue(can_give_to_trio(C(u'4♦'), Cs(u'jkr 4♦ 4♥')))
    def test_valid_joker_contribution_to_trio_with_joker(self):
        self.assertTrue(can_give_to_trio(C(u'jkr'), Cs(u'jkr 4♦ 4♥')))

    # invalid trio contributions
    def test_invalid_simple_contribution_to_trio(self):
        self.assertFalse(can_give_to_trio(C(u'3♠'), Cs(u'4♥ 4♦ 4♥')))
    def test_invalid_simple_contribution_to_trio_with_joker(self):
        self.assertFalse(can_give_to_trio(C(u'5♦'), Cs(u'jkr 4♦ 4♥')))

    # valid straight contributions on the left
    def test_valid_simple_contribution_to_straight_to_left(self):
        self.assertTrue(can_give_to_straight_at_left(C(u'5♦'), Cs(u'6♦ 7♦ 8♦ 9♦')));
        self.assertTrue(can_give_to_straight_at_left(C(u'K♠'), Cs(u'A♠ 2♠ 3♠ 4♠')));
        self.assertTrue(can_give_to_straight_at_left(C(u'J♥'), Cs(u'Q♥ K♥ A♥ 2♥')));
    def test_valid_simple_contribution_to_straight_to_left_with_joker(self):
        self.assertTrue(can_give_to_straight_at_left(C(u'5♦'), Cs(u'jkr 7♦ 8♦ 9♦')));
        self.assertTrue(can_give_to_straight_at_left(C(u'K♠'), Cs(u'jkr 2♠ 3♠ 4♠')));
        self.assertTrue(can_give_to_straight_at_left(C(u'K♠'), Cs(u'A♠ jkr 3♠ 4♠')));
        self.assertTrue(can_give_to_straight_at_left(C(u'J♥'), Cs(u'Q♥ K♥ jkr 2♥')));
        self.assertTrue(can_give_to_straight_at_left(C(u'J♥'), Cs(u'Q♥ K♥ A♥ jkr')));
    def test_valid_joker_contribution_to_straight_to_left(self):
        self.assertTrue(can_give_to_straight_at_left(C(u'jkr'), Cs(u'6♦ 7♦ 8♦ 9♦')));
        self.assertTrue(can_give_to_straight_at_left(C(u'jkr'), Cs(u'A♠ 2♠ 3♠ 4♠')));
        self.assertTrue(can_give_to_straight_at_left(C(u'jkr'), Cs(u'Q♥ K♥ A♥ 2♥')));
    def test_valid_joker_contribution_to_straight_to_left_with_joker(self):
        self.assertTrue(can_give_to_straight_at_left(C(u'jkr'), Cs(u'6♦ 7♦ jkr 9♦')));
        self.assertTrue(can_give_to_straight_at_left(C(u'jkr'), Cs(u'A♠ 2♠ 3♠ jkr')));
        self.assertTrue(can_give_to_straight_at_left(C(u'jkr'), Cs(u'Q♥ K♥ jkr 2♥')));

    # invalid straight contributions on the left
    def test_invalid_simple_contribution_to_straight_to_left(self):
        self.assertFalse(can_give_to_straight_at_left(C(u'6♦'), Cs(u'6♦ 7♦ 8♦ 9♦')));
        self.assertFalse(can_give_to_straight_at_left(C(u'K♥'), Cs(u'A♠ 2♠ 3♠ 4♠')));
        self.assertFalse(can_give_to_straight_at_left(C(u'3♥'), Cs(u'Q♥ K♥ A♥ 2♥')));
    def test_invalid_simple_contribution_to_straight_to_left_with_joker(self):
        self.assertFalse(can_give_to_straight_at_left(C(u'6♦'), Cs(u'jkr 7♦ 8♦ 9♦')));
        self.assertFalse(can_give_to_straight_at_left(C(u'K♥'), Cs(u'A♠ jkr 3♠ 4♠')));
        self.assertFalse(can_give_to_straight_at_left(C(u'3♥'), Cs(u'Q♥ K♥ jkr 2♥')));
        self.assertFalse(can_give_to_straight_at_left(C(u'3♣'), Cs(u'Q♥ K♥ A♥ jkr')));
    def test_invalid_joker_contribution_to_straight_to_left_with_joker(self):
        self.assertFalse(can_give_to_straight_at_left(C(u'jkr'), Cs(u'6♦ jkr 8♦ 9♦')));
        self.assertFalse(can_give_to_straight_at_left(C(u'jkr'), Cs(u'jkr 2♠ 3♠ 4♠')));
        self.assertFalse(can_give_to_straight_at_left(C(u'jkr'), Cs(u'Q♥ jkr A♥ 2♥')));

    # valid straight contributions on the right
    def test_valid_simple_contribution_to_straight_to_right(self):
        self.assertTrue(can_give_to_straight_at_right(C(u'10♦'), Cs(u'6♦ 7♦ 8♦ 9♦')));
        self.assertTrue(can_give_to_straight_at_right(C(u'A♠'),  Cs(u'10♠ J♠ Q♠ K♠')));
        self.assertTrue(can_give_to_straight_at_right(C(u'2♥'),  Cs(u'J♥ Q♥ K♥ A♥')));
    def test_valid_simple_contribution_to_straight_to_right_with_joker(self):
        self.assertTrue(can_give_to_straight_at_right(C(u'10♦'), Cs(u'6♦ 7♦ 8♦ jkr')));
        self.assertTrue(can_give_to_straight_at_right(C(u'A♠'),  Cs(u'10♠ J♠ Q♠ jkr')));
        self.assertTrue(can_give_to_straight_at_right(C(u'A♠'),  Cs(u'10♠ J♠ jkr K♠')));
        self.assertTrue(can_give_to_straight_at_right(C(u'2♥'),  Cs(u'J♥ jkr K♥ A♥')));
        self.assertTrue(can_give_to_straight_at_right(C(u'2♥'),  Cs(u'jkr Q♥ K♥ A♥')));
    def test_valid_joker_contribution_to_straight_to_right(self):
        self.assertTrue(can_give_to_straight_at_right(C(u'jkr'), Cs(u'6♦ 7♦ 8♦ 9♦')));
        self.assertTrue(can_give_to_straight_at_right(C(u'jkr'), Cs(u'10♠ J♠ Q♠ K♠')));
        self.assertTrue(can_give_to_straight_at_right(C(u'jkr'), Cs(u'J♥ Q♥ K♥ A♥')));
    def test_valid_joker_contribution_to_straight_to_right_with_joker(self):
        self.assertTrue(can_give_to_straight_at_right(C(u'jkr'), Cs(u'6♦ jkr 8♦ 9♦')));
        self.assertTrue(can_give_to_straight_at_right(C(u'jkr'), Cs(u'jkr J♠ Q♠ K♠')));
        self.assertTrue(can_give_to_straight_at_right(C(u'jkr'), Cs(u'J♥ jkr K♥ A♥')));


    # invalid straight contributions on the right
    def test_invalid_simple_contribution_to_straight_to_right(self):
        self.assertFalse(can_give_to_straight_at_right(C(u'10♣'), Cs(u'6♦ 7♦ 8♦ 9♦')));
        self.assertFalse(can_give_to_straight_at_right(C(u'2♠'),  Cs(u'10♠ J♠ Q♠ K♠')));
        self.assertFalse(can_give_to_straight_at_right(C(u'10♥'), Cs(u'J♥ Q♥ K♥ A♥')));
    def test_invalid_simple_contribution_to_straight_to_right_with_joker(self):
        self.assertFalse(can_give_to_straight_at_right(C(u'10♣'), Cs(u'6♦ 7♦ 8♦ jkr')));
        self.assertFalse(can_give_to_straight_at_right(C(u'2♠'),  Cs(u'10♠ J♠ Q♠ jkr')));
        self.assertFalse(can_give_to_straight_at_right(C(u'10♥'), Cs(u'J♥ jkr K♥ A♥')));
        self.assertFalse(can_give_to_straight_at_right(C(u'10♥'), Cs(u'jkr Q♥ K♥ A♥')));
    def test_invalid_joker_contribution_to_straight_to_right_with_joker(self):
        self.assertFalse(can_give_to_straight_at_right(C(u'jkr'), Cs(u'6♦ 7♦ jkr 9♦')));
        self.assertFalse(can_give_to_straight_at_right(C(u'jkr'), Cs(u'10♠ J♠ Q♠ jkr')));
        self.assertFalse(can_give_to_straight_at_right(C(u'jkr'), Cs(u'J♥ Q♥ jkr A♥')));

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
        g.hands = [Cs(u'5♣ 6♣ 7♣ 8♣   2♥ 2♠ jkr  J♦ J♥   10♦ Q♠ A♣'),
                   Cs(u'3♥ 4♥ 5♥ jkr  A♠ A♣ A♥   7♠ 7♣ 7♦   10♣ K♦')]
        g.well = Cs(u'J♦')
        self.g = g

    def test_lowering(self):

        # Dummy first turn
        self.g.take_from_well()
        self.g.drop_to_well(C(u'J♦'))
        self.g.take_from_well()
        self.g.drop_to_well(C(u'J♦'))

        # Now we start the real fun
        self.g.take_from_well()
        player = self.g.player_in_turn
        self.assertEqual(player, 0)

        # attempt to lowering without having one of the cards (2♣)
        self.assertRaises(GameRoundException, self.g.lower,
                          **dict(trios=[Cs(u'2♥ 2♠ 2♣'), Cs(u'J♦ J♥ J♦')],
                                 straights=[Cs(u'5♣ 6♣ 7♣ 8♣')]))

        # attempt to lowering with wrong number of items
        self.assertRaises(GameRoundException, self.g.lower,
                          **dict(trios=[Cs(u'2♥ 2♠ 2♣')],
                                 straights=[Cs(u'5♣ 6♣ 7♣ 8♣')]))

        # attempt to lowering with wrong number of items
        self.assertRaises(GameRoundException, self.g.lower,
                          **dict(trios=[Cs(u'2♥ 2♠ 2♣')],
                                 straights=[Cs(u'5♣ 6♣ 7♣ 8♣')]))

        # lower as God intended
        self.g.lower(trios=[Cs(u'2♠ jkr 2♥'), Cs(u'J♦ J♦ J♥')],
                     straights=[Cs(u'5♣ 6♣ 7♣ 8♣')])
        self.assertEqual(len(self.g.hands[player]), 3)
        self.assertEqual(len(self.g.lowered_trios[player][0]), 3)
        self.assertEqual(len(self.g.lowered_trios[player][1]), 3)
        self.assertEqual(len(self.g.lowered_straights[player][0]), 4)
        self.g.drop_to_well(C(u'Q♠'))

        self.g.take_from_well()
        player = self.g.player_in_turn
        self.assertEqual(player, 1)

        # lower as God intended
        self.g.lower(trios=[Cs(u'A♠ A♣ A♥'), Cs(u'7♠ 7♣ 7♦')],
                     straights=[Cs(u'3♥ 4♥ 5♥ jkr')])
        self.assertEqual(len(self.g.hands[player]), 3)
        self.assertEqual(len(self.g.lowered_trios[player][0]), 3)
        self.assertEqual(len(self.g.lowered_trios[player][1]), 3)
        self.assertEqual(len(self.g.lowered_straights[player][0]), 4)
        self.g.drop_to_well(C(u'10♣'))

        # TODO: improve this test


class TestGiveCards(unittest.TestCase):

    def test_give_card_to_trio(self):
        g = GameRound(nr_players=2, nr_trios=3, nr_straights=0)
        g.hands = [Cs(u'5♣ 6♣ 7♣   2♥ 2♠ jkr  J♦ J♥ J♣  10♦ 10♠ 10♣'),
                   Cs(u'2♥ 4♥ 5♥ jkr  A♠ A♣ A♥   7♠ 7♣ 7♦   10♥ K♦')]
        g.well = Cs(u'J♦')

        # Dummy first turn
        g.take_from_well()
        g.drop_to_well(C(u'J♦'))
        g.take_from_well()
        g.drop_to_well(C(u'J♦'))

        # First player lowers with 3 trios
        g.take_from_well()
        g.lower(trios=[Cs(u'2♥ 2♠ jkr'), Cs(u'J♦ J♥ J♣'), Cs(u'10♦ 10♠ 10♣')])
        g.drop_to_well(C(u'5♣'))
        cards_on_hand = len(g.hands[0])

        # Second player puts her 10♥ in the well
        g.take_from_stack()
        g.drop_to_well(C(u'10♥'))

        # First player takes it and tries to give it to the 10's trio
        g.take_from_well()

        # Try to give a card that is not in 1st player's hand
        self.assertRaises(GameRoundException, g.give_to,
                          **dict(card=C(u'10♦'), player=0,
                          lowered_set=Cs(u'10♦ 10♠ 10♣')))
        # Try to give a card to an unexisting lowered set
        self.assertRaises(GameRoundException, g.give_to,
                          **dict(card=C(u'7♣'), player=0,
                          lowered_set=Cs(u'7♦ 7♠ 7♣')))
        # This lowered set exists, but in the 1st player's sets, not 2nd's
        self.assertRaises(GameRoundException, g.give_to,
                          **dict(card=C(u'10♥'), player=1,
                          lowered_set=Cs(u'10♦ 10♠ 10♣')))
        # Try to give a card to the wrong set
        self.assertRaises(GameRoundException, g.give_to,
                          **dict(card=C(u'10♥'), player=1,
                          lowered_set=Cs(u'J♦ J♥ J♣')))

        # Finally, do it right. At the end of the turn, 1st player will have
        # one less card. After giving, and before dropping to the well, though,
        # she will have the same amount of cards
        g.give_to(C(u'10♥'), 0, Cs(u'10♦ 10♠ 10♣'))
        self.assertTrue( len(g.hands[0]) == cards_on_hand )
        g.drop_to_well(C(u'6♣'))
        self.assertTrue( len(g.hands[0]) == cards_on_hand - 1 )
        # TODO: check that the amount of cards lowered has increased by 1

        # 2nd player tries to give a card, but he hasn't lowered yet
        self.assertRaises(InvalidMoveException, g.give_to,
                          **dict(card=C(u'2♥'), player=0,
                          lowered_set=Cs(u'jkr 2♥ 2♠')))

    def test_give_card_to_straight(self):
        g = GameRound(nr_players=2, nr_trios=0, nr_straights=1)
        g.hands = [Cs(u'5♣ 6♣ 7♣ 8♣  2♥ jkr  J♦ J♥ J♣  10♦ 10♠ 10♣'),
                   Cs(u'2♥ 4♥ 5♥ jkr  A♠ A♣ A♥   jkr 9♣ 7♦   10♥ K♦')]
        g.well = Cs(u'J♦')

        # Dummy first turn
        g.take_from_well()
        g.drop_to_well(C(u'J♦'))
        g.take_from_well()
        g.drop_to_well(C(u'J♦'))

        # First player lowers with 1 straight
        g.take_from_well()
        g.lower(straights=[Cs(u'5♣ 6♣ 7♣ 8♣')])
        g.drop_to_well(C(u'10♠'))
        cards_on_hand = [None, None]
        cards_on_hand[0] = len(g.hands[0])

        # Second player lowers with 1 straight too
        g.take_from_well()
        g.lower(straights=[Cs(u'2♥ jkr 4♥ 5♥')])
        g.drop_to_well(C(u'9♣'))
        cards_on_hand[1] = len(g.hands[1])

        # First player takes 9♣ from the well and gives it to his straight
        g.take_from_well()

        # Try to give a card that is not in 1st player's hand
        self.assertRaises(GameRoundException, g.give_to,
                          **dict(card=C(u'10♥'), player=0,
                          lowered_set=Cs(u'5♣ 6♣ 7♣ 8♣')))
        # Try to give a card to an unexisting lowered set
        self.assertRaises(GameRoundException, g.give_to,
                          **dict(card=C(u'9♣'), player=0,
                          lowered_set=Cs(u'J♦ Q♦ K♦ A♦')))
        # This lowered set exists, but in the 1st player's sets, not 2nd's
        self.assertRaises(GameRoundException, g.give_to,
                          **dict(card=C(u'9♣'), player=1,
                          lowered_set=Cs(u'5♣ 6♣ 7♣ 8♣')))
        # Try to give a card to the wrong set
        self.assertRaises(GameRoundException, g.give_to,
                          **dict(card=C(u'9♣'), player=1,
                          lowered_set=Cs(u'J♦ J♥ J♣')))
        # Trying to put it in the wrong side!
        self.assertRaises(GameRoundException, g.give_to,
                          **dict(card=C(u'9♣'), player=1,
                          lowered_set=Cs(u'5♣ 6♣ 7♣ 8♣'),
                          where='left'))

        # Finally, do it right. At the end of the turn, 1st player will have
        # one less card. After giving, and before dropping to the well, though,
        # she will have the same amount of cards
        g.give_to(C(u'9♣'),  0, Cs(u'5♣ 6♣ 7♣ 8♣'))
        g.give_to(C(u'10♣'), 0, Cs(u'5♣ 6♣ 7♣ 8♣ 9♣'), where='right')
        g.give_to(C(u'jkr'), 0, Cs(u'5♣ 6♣ 7♣ 8♣ 9♣ 10♣'), where='left')
        g.give_to(C(u'J♣'),  0, Cs(u'jkr 5♣ 6♣ 7♣ 8♣ 9♣ 10♣'), where='right')
        self.assertTrue( len(g.hands[0]) == cards_on_hand[0] - 3 )
        g.drop_to_well(C(u'10♦'))
        self.assertTrue( len(g.hands[0]) == cards_on_hand[0] - 4 )
        # TODO: check that the amount of cards lowered has increased by 3

        # 2nd player gives himself a joker
        g.take_from_well()
        g.give_to(C(u'jkr'), 1, Cs(u'2♥ jkr 4♥ 5♥'))
        self.assertTrue( len(g.hands[1]) == cards_on_hand[1] )
        g.drop_to_well(C(u'7♦'))
        self.assertTrue( len(g.hands[1]) == cards_on_hand[1] - 1 )

class TestFullGameRound(unittest.TestCase):
    def setUp(self):
        g = GameRound(nr_players=2, nr_trios=3, nr_straights=0)
        g.hands = [Cs(u'5♣ 6♣ 7♣   2♥ 2♠ jkr  J♦ J♥ J♣  10♦ 10♠ 10♣'),
                   Cs(u'3♥ 4♥ 5♥ jkr  A♠ A♣ A♥   7♠ 7♣ 7♦   10♥ K♦')]
        g.well = Cs(u'J♦')
        self.g = g

    def test_invalid_modes(self):

        # Players haven't started their turn yet, so some things
        # cannot be done
        self.assertRaises(InvalidMoveException, self.g.give_to,
                          **dict(card=C(u'jkr'), player=1,
                          lowered_set=Cs(u'7♠ 7♣ 7♦')))
        self.assertRaises(InvalidMoveException, self.g.lower,
                          **dict(straights=Cs(u'2♥ 2♠ jkr')))
        self.assertRaises(InvalidMoveException, self.g.drop_to_well,
                          **dict(card=C(u'J♦')))

        # OK, take a card from the well
        self.g.take_from_well()
        self.assertRaises(InvalidMoveException, self.g.take_from_well)
        self.assertRaises(InvalidMoveException, self.g.take_from_stack)

        # we can't lower yet (first turn), we can't give either, of course
        self.assertRaises(InvalidMoveException, self.g.lower,
                          **dict(straights=Cs(u'2♥ 2♠ jkr')))
        self.assertRaises(InvalidMoveException, self.g.give_to,
                          **dict(card=C(u'jkr'), player=1,
                          lowered_set=Cs(u'7♠ 7♣ 7♦')))

        # Just end the turn, then we can't do anything again
        self.g.drop_to_well(C(u'J♦'))
        self.assertRaises(InvalidMoveException, self.g.give_to,
                          **dict(card=C(u'jkr'), player=1,
                          lowered_set=Cs(u'7♠ 7♣ 7♦')))
        self.assertRaises(InvalidMoveException, self.g.lower,
                          **dict(straights=Cs(u'2♥ 2♠ jkr')))
        self.assertRaises(InvalidMoveException, self.g.drop_to_well,
                          **dict(card=C(u'J♦')))

    def test_game_round_is_over(self):
        # No plays so far
        self.assertFalse(self.g.is_over())

        # Dummy first turn
        self.g.take_from_well()
        self.g.drop_to_well(C(u'J♦'))
        self.g.take_from_well()
        self.g.drop_to_well(C(u'J♦'))

        # First player lowers with 3 trios
        self.g.take_from_well()
        self.g.lower(trios=[Cs(u'2♥ 2♠ jkr'), Cs(u'J♦ J♥ J♣'), Cs(u'10♦ 10♠ 10♣')])
        self.g.drop_to_well(C(u'5♣'))

        # Not over yet, still 2 cards remaining in 1st player hand
        self.assertFalse(self.g.is_over())

        # 2nd player's turn, be stupid and give a good card to 1st player
        self.g.take_from_stack()
        self.g.drop_to_well(C(u'10♥'))
        self.assertFalse(self.g.is_over())

        # 1st player takes the card from the well, puts it, together with the
        # first card that she tool from the well, and finally drops one to the well
        # (still one card in the hand)
        self.g.take_from_well()
        self.g.give_to(C(u'10♥'), 0, Cs(u'10♦ 10♠ 10♣'))
        self.g.give_to(C(u'J♦'), 0, Cs(u'J♦ J♥ J♣'))
        self.g.drop_to_well(C(u'6♣'))
        self.assertFalse(self.g.is_over())

        # 2nd player again drops an important card
        self.g.take_from_stack()
        self.g.drop_to_well(C(u'jkr'))
        self.assertFalse(self.g.is_over())

        # 1st player takes it, puts is somewhere, and wins
        self.g.take_from_well()
        self.g.give_to(C(u'jkr'), 0, Cs(u'2♥ 2♠ jkr'))
        self.g.drop_to_well(C(u'7♣'))

        # Game is over!
        self.assertTrue(self.g.is_over())

if __name__ == "__main__":
    unittest.main()

# vim: set tabstop=4 expandtab:
