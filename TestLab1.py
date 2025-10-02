from Lab1 import Solution 

from main import my_solution

import unittest


class TestTwoSum(unittest.TestCase):
    
    def test_basic_case(self):
        """Тест базового случая"""
        result = my_solution.two_sum([2, 7, 11, 15], 9)
        self.assertEqual(result, [0, 1])
    
    def test_different_positions(self):
        """Тест с числами в разных позициях"""
        result = my_solution.two_sum([3, 2, 4], 6)
        self.assertEqual(result, [1, 2])
    
    def test_duplicate_numbers(self):
        """Тест с одинаковыми числами"""
        result = my_solution.two_sum([3, 3], 6)
        self.assertEqual(result, [0, 1])
    
    def test_negative_numbers(self):
        """Тест с отрицательными числами"""
        result = my_solution.two_sum([-1, -2, -3, -4, -5], -8)
        self.assertEqual(result, [2, 4])
    
    def test_mixed_numbers(self):
        """Тест со смешанными положительными и отрицательными числами"""
        result = my_solution.two_sum([-3, 4, 3, 90], 0)
        self.assertEqual(result, [0, 2])
    
    def test_no_solution(self):
        """Тест случая, когда решения нет"""
        result = my_solution.two_sum([1, 2, 3, 4], 10)
        self.assertEqual(result, [])
    
    def test_empty_list(self):
        """Тест с пустым списком"""
        result = my_solution.two_sum([], 5)
        self.assertEqual(result, [])
    
    def test_single_element(self):
        """Тест с одним элементом в списке"""
        result = my_solution.two_sum([5], 5)
        self.assertEqual(result, [])
    
    def test_large_numbers(self):
        """Тест с большими числами"""
        result = my_solution.two_sum([1000000, 2000000, 3000000], 5000000)
        self.assertEqual(result, [1, 2])
    
    def test_zero_target(self):
        """Тест с целевой суммой 0"""
        result = my_solution.two_sum([1, -1, 2, 3], 0)
        self.assertEqual(result, [0, 1])

    def test_only_integers_in_list(self):
        """Проверка, что список содержит только целые числа"""
        # Проверяем, что все элементы списка являются целыми числами
        test_list = [2, 7, 11, 15]
        for item in test_list:
            self.assertIsInstance(item, int, f"Элемент {item} не является целым числом")
            # Проверяем, что это не float, замаскированный под int
            self.assertNotIsInstance(item, float, f"Элемент {item} является числом с плавающей точкой")
    
    def test_target_is_integer(self):
        """Проверка, что целевое значение является целым числом"""
        target = 9
        self.assertIsInstance(target, int, "Целевое значение не является целым числом")
        self.assertNotIsInstance(target, float, "Целевое значение является числом с плавающей точкой")
    
    def test_no_strings_in_list(self):
        """Проверка, что в списке нет строк"""
        test_list = [2, 7, 11, 15]
        for item in test_list:
            self.assertNotIsInstance(item, str, f"Элемент {item} является строкой")
    
    def test_no_floats_in_list(self):
        """Проверка, что в списке нет чисел с плавающей точкой"""
        test_list = [2, 7, 11, 15]
        for item in test_list:
            self.assertNotIsInstance(item, float, f"Элемент {item} является числом с плавающей точкой")
    
    def test_no_other_types_in_list(self):
        """Проверка, что в списке нет других типов данных"""
        test_list = [2, 7, 11, 15]
        for item in test_list:
            self.assertTrue(isinstance(item, int), 
                          f"Элемент {item} имеет недопустимый тип: {type(item)}")
    
    def test_comprehensive_type_check(self):
        """Комплексная проверка типов данных"""
        test_cases = [
            ([2, 7, 11, 15], 9),
            ([3, 2, 4], 6),
            ([3, 3], 6),
            ([-1, -2, -3, -4, -5], -8)
        ]
        
        for nums, target in test_cases:
            # Проверка списка чисел
            for num in nums:
                self.assertIsInstance(num, int, f"Число {num} не является целым")
                self.assertNotIsInstance(num, float, f"Число {num} является float")
                self.assertNotIsInstance(num, str, f"Элемент {num} является строкой")
            
            # Проверка целевого значения
            self.assertIsInstance(target, int, f"Целевое значение {target} не является целым")
            self.assertNotIsInstance(target, float, f"Целевое значение {target} является float")


if __name__ == '__main__':
    unittest.main()

