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


if __name__ == "__main__":
    unittest.main()
