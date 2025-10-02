class BinTree:
    
    def gen_bin_tree(self, height=6, root=9):
        # Базовый случай - если высота 0, возвращаем None
        if height == 0:
            return None
        
        # Создаем узел с текущим корнем
        tree = {
            'root': root,
            'left': None,
            'right': None
        }
        
        # Если высота больше 1, строим потомков рекурсивно
        if height > 1:
            # Вычисляем левого и правого потомка по формулам
            left_root = root * 2 + 1
            right_root = 2 * root - 1
            
            # Рекурсивно строим левое и правое поддеревья
            tree['left'] = self.gen_bin_tree(height - 1, left_root)
            tree['right'] = self.gen_bin_tree(height - 1, right_root)
        
        return tree


if __name__ == "__main__":
    # Создаем объект класса
    tree_generator = BinTree()
    
    # Ввод параметров
    print("Введите параметры для построения бинарного дерева")
    
    # Запрашиваем высоту дерева
    height_input = input("Введите высоту дерева (нажмите Enter для значения по умолчанию 6): ")
    if height_input == "":
        height = 6  # значение по умолчанию
    else:
        height = int(height_input)  # преобразуем введенный текст в число
    
    # Запрашиваем значение корня
    root_input = input("Введите значение корня (нажмите Enter для значения по умолчанию 9): ")
    if root_input == "":
        root = 9  # значение по умолчанию
    else:
        root = int(root_input)  # преобразуем введенный текст в число
    
    # Строим дерево с введенными параметрами
    trees = tree_generator.gen_bin_tree(height, root)
    
    # Выводим результат
    print(f"Бинарное дерево с высотой {height} и корнем {root}:")
    print(trees)