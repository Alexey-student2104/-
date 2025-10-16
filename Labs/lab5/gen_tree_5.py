from collections import deque, OrderedDict

class gen_tree:
    def __init__(self):
        pass
    
    def gen_bin_tree(self, height=6, root=9, left_branch=lambda r: r*2+1, right_branch=lambda r: 2*r-1):
        """
        Строит бинарное дерево нерекурсивным способом
        height - высота дерева
        root - значение в корне
        left_branch - функция для вычисления левого потомка
        right_branch - функция для вычисления правого потомка
        """
        if height <= 0:
            return OrderedDict()
        
        # Используем OrderedDict для сохранения порядка узлов
        tree = OrderedDict()
        
        # Используем deque для очереди
        queue = deque()
        queue.append((root, 1, "root"))  # (значение, уровень, тип)
        
        while queue:
            current_value, current_level, node_type = queue.popleft()
            
            # Добавляем текущий узел в дерево
            tree[current_value] = OrderedDict()
            
            # Если не достигли максимальной высоты, добавляем потомков
            if current_level < height:
                left_child = left_branch(current_value)
                right_child = right_branch(current_value)
                
                # Добавляем потомков в дерево
                tree[current_value]['left'] = left_child
                tree[current_value]['right'] = right_child
                
                # Добавляем потомков в очередь для дальнейшей обработки
                queue.append((left_child, current_level + 1, "left"))
                queue.append((right_child, current_level + 1, "right"))
            else:
                # Если это лист, потомков нет
                tree[current_value]['left'] = None
                tree[current_value]['right'] = None
        
        return tree

    def get_user_input(self):
        """Получает параметры дерева от пользователя"""
        print("Введите параметры бинарного дерева (или нажмите Enter для значений по умолчанию):")
        
        height_input = input(f"Высота дерева (по умолчанию {6}): ")
        height = int(height_input) if height_input.strip() else 6
        
        root_input = input(f"Значение корня (по умолчанию {9}): ")
        root = int(root_input) if root_input.strip() else 9
        
        use_custom = input("Использовать пользовательские формулы для потомков? (y/n): ").lower().strip()
        
        if use_custom == 'y':
            print("Введите формулы в виде Python выражений с переменной 'r' (например: r*2+1):")
            left_formula = input("Левый потомок: ")
            right_formula = input("Правый потомок: ")
            
            # Создаем функции из введенных формул
            left_branch = eval(f"lambda r: {left_formula}")
            right_branch = eval(f"lambda r: {right_formula}")
        else:
            left_branch = lambda r: r*2+1
            right_branch = lambda r: 2*r-1
        
        return height, root, left_branch, right_branch

    def main(self):
        """Основная программа"""
        # Получаем параметры от пользователя
        height, root, left_func, right_func = self.get_user_input()
        
        # Строим дерево
        binary_tree = self.gen_bin_tree(height, root, left_func, right_func)
        
        # Выводим результаты
        print(binary_tree)
        print(f"Высота: {height}")
        print(f"Корень: {root}")
        print(f"Количество узлов: {len(binary_tree)}")
        
        # Демонстрация использования других структур из collections
        print("Использование других структур из collections:")
        
        # Использование deque для обхода дерева
        print("\nОбход дерева в ширину с помощью deque:")
        bfs_queue = deque([root])
        visited = OrderedDict()
        
        while bfs_queue:
            node = bfs_queue.popleft()
            if node in binary_tree and node not in visited:
                visited[node] = binary_tree[node]
                children = binary_tree[node]
                if children['left'] is not None:
                    bfs_queue.append(children['left'])
                if children['right'] is not None:
                    bfs_queue.append(children['right'])
        
        print("Порядок обхода в ширину:", list(visited.keys()))

# Запуск программы
if __name__ == "__main__":
    tree_generator = gen_tree()
    tree_generator.main()