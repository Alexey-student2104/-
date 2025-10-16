import timeit
import matplotlib.pyplot as plt
from collections import deque

class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

def build_tree_recursive(height, root_val=9):
    """Рекурсивное построение бинарного дерева"""
    if height <= 0:
        return None
    
    def build_node(current_val, current_height):
        if current_height >= height:
            return None
            
        node = TreeNode(current_val)
        node.left = build_node(current_val * 2 + 1, current_height + 1)
        node.right = build_node(current_val * 2 - 1, current_height + 1)
        return node
    
    return build_node(root_val, 0)

def build_tree_iterative(height, root_val=9):
    """Итеративное построение бинарного дерева с использованием очереди"""
    if height <= 0:
        return None
    
    root = TreeNode(root_val)
    queue = deque([(root, 0)])  # (node, current_height)
    
    while queue:
        node, current_height = queue.popleft()
        
        if current_height + 1 < height:
            # Создаем левого потомка
            left_val = node.val * 2 + 1
            node.left = TreeNode(left_val)
            queue.append((node.left, current_height + 1))
            
            # Создаем правого потомка
            right_val = node.val * 2 - 1
            node.right = TreeNode(right_val)
            queue.append((node.right, current_height + 1))
    
    return root

def tree_to_dict(node):
    """Преобразует дерево в словарь для удобства просмотра"""
    if node is None:
        return None
    return {
        'val': node.val,
        'left': tree_to_dict(node.left),
        'right': tree_to_dict(node.right)
    }

def get_user_input():
    """Получает параметры дерева от пользователя"""
    print("Параметры построения дерева:")
    print("-" * 30)
    
    height_input = input("Введите высоту дерева (по умолчанию 6): ").strip()
    height = int(height_input) if height_input else 6
    
    root_input = input("Введите значение корня дерева (по умолчанию 9): ").strip()
    root_val = int(root_input) if root_input else 9
        
    return root_val, height

def demonstrate_trees(root_val, height):
    """Демонстрирует построение деревьев обоими методами"""
    print(f"корень: {root_val}, высота: {height}")
    
    # Рекурсивное построение
    print("Дерево построенное рекурсивным методом:")
    recursive_tree = build_tree_recursive(height, root_val)
    recursive_dict = tree_to_dict(recursive_tree)
    print(recursive_dict)
    
    # Итеративное построение
    print("Дерево построенное итеративным методом:")
    iterative_tree = build_tree_iterative(height, root_val)
    iterative_dict = tree_to_dict(iterative_tree)
    print(iterative_dict)

# Функции для измерения времени
def time_recursive(height, root_val):
    return timeit.timeit(lambda: build_tree_recursive(height, root_val), number=10)

def time_iterative(height, root_val):
    return timeit.timeit(lambda: build_tree_iterative(height, root_val), number=10)

def compare_performance(root_val):
    """Сравнивает производительность и строит график"""
    heights = list(range(1, 10))
    recursive_times = []
    iterative_times = []
    
    print("Измерение времени для построения графиков...")
    
    for height in heights:
        # Измеряем время в миллисекундах
        rec_time = time_recursive(height, root_val) * 1000
        iter_time = time_iterative(height, root_val) * 1000
        
        recursive_times.append(rec_time)
        iterative_times.append(iter_time)
    
    # Построение графика
    plt.figure(figsize=(12, 8))
    
    # Убраны маркеры, оставлены только линии
    plt.plot(heights, recursive_times, 'b-', label='Рекурсивный метод', linewidth=2)
    plt.plot(heights, iterative_times, 'r-', label='Итеративный метод', linewidth=2)
    
    plt.xlabel('Высота дерева', fontsize=12)
    plt.ylabel('Время построения (мс)', fontsize=12)
    plt.title('Зависимость времени построения от высоты дерева', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    plt.tight_layout()
    plt.show()

def main():
    """Основная функция программы"""
    # Получаем параметры от пользователя
    root_val, height = get_user_input()
    
    # Демонстрация построения деревьев
    demonstrate_trees(root_val, height)
    
    # Построение графика сравнения производительности
    compare_performance(root_val)

if __name__ == "__main__":
    main()