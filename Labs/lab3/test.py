from bintree import BinTree
import unittest


class TestBinTreeGenerator(unittest.TestCase):
    def setUp(self):
        # Этот метод вызывается перед каждым тестом
        # Создаем объект генератора деревьев для использования в тестах
        self.generator = BinTree()

    def test_default_parameters(self):
        """Тест работы функции с параметрами по умолчанию"""
        # Вызываем метод без параметров - должны использоваться значения по умолчанию
        tree = self.generator.gen_bin_tree()

        # Проверяем что дерево не пустое
        self.assertIsNotNone(tree)
        # Проверяем что корень равен значению по умолчанию (9)
        self.assertEqual(tree['root'], 9)

    def test_height_zero(self):
        """Тест случая когда высота дерева равна 0"""
        # При высоте 0 дерево должно быть пустым (None)
        tree = self.generator.gen_bin_tree(height=0, root=5)

        # Проверяем что возвращается None
        self.assertIsNone(tree)

    def test_height_one(self):
        """Тест случая когда высота дерева равна 1"""
        # При высоте 1 должно быть только корень без потомков
        tree = self.generator.gen_bin_tree(height=1, root=5)

        # Проверяем значение корня
        self.assertEqual(tree['root'], 5)
        # Проверяем что левый потомок отсутствует
        self.assertIsNone(tree['left'])
        # Проверяем что правый потомок отсутствует
        self.assertIsNone(tree['right'])

    def test_custom_parameters(self):
        """Тест работы с пользовательскими параметрами"""
        # Создаем дерево высотой 2 с корнем 5
        tree = self.generator.gen_bin_tree(height=2, root=5)

        # Проверяем корневой узел
        self.assertEqual(tree['root'], 5)
        # Проверяем левого потомка: 5*2+1 = 11
        self.assertEqual(tree['left']['root'], 11)
        # Проверяем правого потомка: 2*5-1 = 9
        self.assertEqual(tree['right']['root'], 9)

    def test_formulas_calculation(self):
        """Тест правильности вычислений по формулам"""
        # Создаем дерево для проверки формул вычисления потомков
        tree = self.generator.gen_bin_tree(height=2, root=10)

        # Проверяем левого потомка: root*2+1
        self.assertEqual(tree['left']['root'], 10*2+1)  # Должно быть 21
        # Проверяем правого потомка: 2*root-1
        self.assertEqual(tree['right']['root'], 2*10-1)  # Должно быть 19

    def test_negative_root(self):
        """Тест работы с отрицательным значением корня"""
        tree = self.generator.gen_bin_tree(height=2, root=-3)

        # Проверяем корень
        self.assertEqual(tree['root'], -3)
        # Проверяем левого потомка: -3*2+1 = -5
        self.assertEqual(tree['left']['root'], -5)
        # Проверяем правого потомка: 2*(-3)-1 = -7
        self.assertEqual(tree['right']['root'], -7)

    def test_large_height(self):
        """Тест работы с большой высотой дерева"""
        tree = self.generator.gen_bin_tree(height=4, root=1)

        # Проверяем что дерево создано
        self.assertIsNotNone(tree)
        # Проверяем что структура дерева правильная
        self.assertEqual(tree['root'], 1)
        # Проверяем что есть потомки на всех уровнях
        self.assertIsNotNone(tree['left']['left']['left'])
        self.assertIsNotNone(tree['right']['right']['right'])

    def test_zero_root(self):
        """Тест работы с нулевым корнем"""
        tree = self.generator.gen_bin_tree(height=2, root=0)

        # Проверяем корень
        self.assertEqual(tree['root'], 0)
        # Проверяем левого потомка: 0*2+1 = 1
        self.assertEqual(tree['left']['root'], 1)
        # Проверяем правого потомка: 2*0-1 = -1
        self.assertEqual(tree['right']['root'], -1)

    def test_tree_structure_integrity(self):
        """Тест целостности структуры дерева"""
        tree = self.generator.gen_bin_tree(height=3, root=2)

        # Проверяем что все узлы имеют правильную структуру
        self.assertIn('root', tree)
        self.assertIn('left', tree)
        self.assertIn('right', tree)

        # Проверяем что потомки тоже имеют правильную структуру
        self.assertIn('root', tree['left'])
        self.assertIn('left', tree['left'])
        self.assertIn('right', tree['left'])

    def test_different_height_values(self):
        """Тест разных значений высоты"""
        # Высота 1
        tree1 = self.generator.gen_bin_tree(height=1, root=7)
        self.assertEqual(tree1['root'], 7)
        self.assertIsNone(tree1['left'])
        self.assertIsNone(tree1['right'])

        # Высота 3
        tree3 = self.generator.gen_bin_tree(height=3, root=7)
        self.assertEqual(tree3['root'], 7)
        self.assertIsNotNone(tree3['left'])
        self.assertIsNotNone(tree3['right'])
        # Проверяем что есть потомки второго уровня
        self.assertIsNotNone(tree3['left']['left'])
        self.assertIsNotNone(tree3['right']['right'])

    def test_recursive_properties(self):
        """Тест рекурсивных свойств дерева"""
        tree = self.generator.gen_bin_tree(height=3, root=4)

        # Проверяем что формулы применяются рекурсивно
        # Первый уровень: 4 → left=9, right=7
        self.assertEqual(tree['left']['root'], 9)
        self.assertEqual(tree['right']['root'], 7)

        # Второй уровень: 9 → left=19, right=17; 7 → left=15, right=13
        self.assertEqual(tree['left']['left']['root'], 19)
        self.assertEqual(tree['left']['right']['root'], 17)
        self.assertEqual(tree['right']['left']['root'], 15)
        self.assertEqual(tree['right']['right']['root'], 13)


if __name__ == "__main__":
    # Запускаем все тесты
    unittest.main()
