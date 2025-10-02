import unittest
from game import Game

class TestGame(unittest.TestCase):
    
    def test_slow_guess_found(self):
        game = Game()
        result, tries = game.slow_guess(5, 1, 10)
        self.assertEqual(result, 5)
        self.assertEqual(tries, 5)
    
    def test_slow_guess_not_found(self):
        game = Game()
        result, tries = game.slow_guess(15, 1, 10)
        self.assertIsNone(result)
        self.assertEqual(tries, 10)
    
    def test_slow_guess_start_boundary(self):
        game = Game()
        result, tries = game.slow_guess(1, 1, 10)
        self.assertEqual(result, 1)
        self.assertEqual(tries, 1)
    
    def test_slow_guess_end_boundary(self):
        game = Game()
        result, tries = game.slow_guess(10, 1, 10)
        self.assertEqual(result, 10)
        self.assertEqual(tries, 10)
    
    def test_binary_guess_found(self):
        game = Game()
        result, tries = game.binary_guess(5, 1, 10)
        self.assertEqual(result, 5)
        self.assertLessEqual(tries, 4)
    
    def test_binary_guess_not_found(self):
        game = Game()
        result, tries = game.binary_guess(15, 1, 10)
        self.assertIsNone(result)
        self.assertLessEqual(tries, 4)
    
    def test_binary_guess_start_boundary(self):
        game = Game()
        result, tries = game.binary_guess(1, 1, 10)
        self.assertEqual(result, 1)
    
    def test_binary_guess_end_boundary(self):
        game = Game()
        result, tries = game.binary_guess(10, 1, 10)
        self.assertEqual(result, 10)
    
    def test_slow_guess_single_element(self):
        game = Game()
        result, tries = game.slow_guess(5, 5, 5)
        self.assertEqual(result, 5)
        self.assertEqual(tries, 1)
    
    def test_binary_guess_single_element(self):
        game = Game()
        result, tries = game.binary_guess(5, 5, 5)
        self.assertEqual(result, 5)
        self.assertEqual(tries, 1)
    
    def test_slow_guess_empty_range(self):
        game = Game()
        result, tries = game.slow_guess(5, 10, 1)
        self.assertIsNone(result)
        self.assertEqual(tries, 0)
    
    def test_binary_guess_empty_range(self):
        game = Game()
        result, tries = game.binary_guess(5, 10, 1)
        self.assertIsNone(result)
        self.assertEqual(tries, 0)
    
    def test_binary_guess_efficiency(self):
        game = Game()
        result, tries = game.binary_guess(500, 1, 1000)
        self.assertEqual(result, 500)
        self.assertLessEqual(tries, 10)
    
    def test_slow_vs_binary_efficiency(self):
        game = Game()
        number, start, end = 750, 1, 1000
        
        result_binary, tries_binary = game.binary_guess(number, start, end)
        result_slow, tries_slow = game.slow_guess(number, start, end)
        
        self.assertEqual(result_binary, number)
        self.assertEqual(result_slow, number)
        self.assertLess(tries_binary, tries_slow)
    
    def test_binary_guess_large_range(self):
        game = Game()
        result, tries = game.binary_guess(999999, 1, 1000000)
        self.assertEqual(result, 999999)
        self.assertLessEqual(tries, 20)

if __name__ == '__main__':
    unittest.main()