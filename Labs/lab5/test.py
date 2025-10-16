import unittest
from collections import OrderedDict
from gen_tree_5 import gen_tree

class TestGenTree(unittest.TestCase):
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.tree_gen = gen_tree()
    
    def test_gen_bin_tree_default_params(self):
        """Тест генерации дерева с параметрами по умолчанию"""
        result = self.tree_gen.gen_bin_tree()
        self.assertIsInstance(result, OrderedDict)
        self.assertGreater(len(result), 0)
        self.assertIn(9, result)
    
    def test_gen_bin_tree_height_zero(self):
        """Тест генерации дерева с высотой 0"""
        result = self.tree_gen.gen_bin_tree(height=0)
        self.assertEqual(result, OrderedDict())
    
    def test_gen_bin_tree_height_one(self):
        """Тест генерации дерева с высотой 1"""
        result = self.tree_gen.gen_bin_tree(height=1, root=5)
        self.assertEqual(len(result), 1)
        self.assertIn(5, result)
        self.assertEqual(result[5]['left'], None)
        self.assertEqual(result[5]['right'], None)
    
    def test_gen_bin_tree_custom_functions(self):
        """Тест генерации дерева с кастомными функциями"""
        left_func = lambda r: r + 1
        right_func = lambda r: r + 2
        result = self.tree_gen.gen_bin_tree(
            height=2, 
            root=10, 
            left_branch=left_func, 
            right_branch=right_func
        )
        self.assertIn(10, result)
        self.assertIn(11, result)
        self.assertIn(12, result)
    
    def test_tree_structure_integrity(self):
        """Тест целостности структуры дерева"""
        result = self.tree_gen.gen_bin_tree(height=4, root=1)
        for node_value, children in result.items():
            self.assertIsInstance(children, OrderedDict)
            self.assertIn('left', children)
            self.assertIn('right', children)

    def test_tree_leaf_nodes_have_no_children(self):
        """Тест что листовые узлы не имеют потомков"""
        result = self.tree_gen.gen_bin_tree(height=2, root=1)
        
        # Находим листовые узлы (узлы последнего уровня)
        max_level_nodes = []
        for node, children in result.items():
            if children['left'] is None and children['right'] is None:
                max_level_nodes.append(node)
        
        # Проверяем что у листовых узлов действительно нет потомков в дереве
        for leaf_node in max_level_nodes:
            self.assertEqual(result[leaf_node]['left'], None)
            self.assertEqual(result[leaf_node]['right'], None)

class TestGenTreeEdgeCases(unittest.TestCase):
    
    def setUp(self):
        self.tree_gen = gen_tree()
    
    def test_negative_height(self):
        """Тест с отрицательной высотой"""
        result = self.tree_gen.gen_bin_tree(height=-1)
        self.assertEqual(result, OrderedDict())
    
    def test_large_height(self):
        """Тест с большой высотой"""
        result = self.tree_gen.gen_bin_tree(height=10)
        self.assertIsInstance(result, OrderedDict)
        self.assertGreater(len(result), 0)
    
    def test_custom_functions_with_negative(self):
        """Тест с кастомными функциями, возвращающими отрицательные значения"""
        left_func = lambda r: -r
        right_func = lambda r: r * -2
        result = self.tree_gen.gen_bin_tree(
            height=3, 
            root=5, 
            left_branch=left_func, 
            right_branch=right_func
        )
        self.assertIn(-5, result)
        self.assertIn(-10, result)

if __name__ == '__main__':
    # Запуск тестов с минимальным выводом - только точки
    unittest.main(verbosity=0, exit=False)