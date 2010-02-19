from carioca import *
import unittest

class Trios(unittest.TestCase):
    # valid trios
    def test_trio_different_suites(self):
        cards = [Card(A, SPADES), Card(A, HEARTS), Card(A, DIAMONDS)]
        self.assertTrue(is_trio(cards))
    def test_trio_one_repeated_suit(self):
        cards = [Card(7, CLUBS), Card(7, SPADES), Card(7, CLUBS)]
        self.assertTrue(is_trio(cards))
    def test_just_one_suit(self):
        cards = [Card(K, HEARTS), Card(K, HEARTS), Card(K, HEARTS)]
        self.assertTrue(is_trio(cards))
    def test_joker_at_beginning(self):
        cards = [Card(JOKER, None), Card(10, SPADES), Card(10, DIAMONDS)]
        self.assertTrue(is_trio(cards))
    def test_joker_in_the_middle(self):
        cards = [Card(2, DIAMONDS), Card(JOKER, None), Card(2, CLUBS)]
        self.assertTrue(is_trio(cards))

    # invalid trios
    def test_three_different_ranks(self):
        cards = [Card(2, DIAMONDS), Card(5, SPADES), Card(J, CLUBS)]
        self.assertFalse(is_trio(cards))
    def test_two_different_ranks(self):
        cards = [Card(Q, SPADES), Card(A, HEARTS), Card(Q, HEARTS)]
        self.assertFalse(is_trio(cards))
    def test_two_jokers(self):
        cards = [Card(10, HEARTS), Card(JOKER, None), Card(JOKER, None)]
        self.assertFalse(is_trio(cards))
    def test_three_jokers(self):
        cards = [Card(JOKER, None), Card(JOKER, None), Card(JOKER, None)]
        self.assertFalse(is_trio(cards))


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
    def test_all_suites_present(self):
        suites = set(card.suit for card in self.deck if card.suit)
        self.assertEqual(len(suites), 4)


if __name__ == "__main__":
    unittest.main()
