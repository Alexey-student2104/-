class Game:
    def slow_guess(self, number, start, end):
        tries = 0
        current_guess = start
        
        while current_guess <= end:
            tries += 1
            
            if current_guess == number:
                print(f"Это число {current_guess}")
                return current_guess, tries
            
            current_guess += 1
        
        # Если не нашли число
        print("Не смог найти число в указанном диапазоне")
        return None, tries


    def binary_guess(self, number, start, end):
        tries = 0
        low = start
        high = end
        
        
        while low <= high:
            tries += 1
            # тут расписан бин. поиск
            guess = (low + high) // 2           
            if guess == number:
                print(f"Нашел! Это число {guess}")
                return guess, tries
            elif guess < number:
                low = guess + 1
            else:
                high = guess - 1
        
        print("Не смог найти число в указанном диапазоне")
        return None, tries


    def get_number_from_user(self, prompt, min_val=None, max_val=None):
        while True:
            try:
                number = int(input(prompt))
                
                # Проверяем минимальное значение
                if min_val is not None and number < min_val:
                    print(f"Число должно быть не меньше {min_val}")
                    continue
                    
                # Проверяем максимальное значение
                if max_val is not None and number > max_val:
                    print(f"Число должно быть не больше {max_val}")
                    continue
                    
                return number
                
            except ValueError:
                print("Пожалуйста, введите целое число!")


    def main(self):
        # Получаем диапазон
        print("Введите диапазон:")
        start_range = self.get_number_from_user("От какого числа? ")
        end_range = self.get_number_from_user("До какого числа? ")
        
        # Проверяем что диапазон правильный
        if start_range > end_range:
            print("Начало больше конца!")
            return
        
        # Получаем загаданное число
        secret_number = self.get_number_from_user(
            f"Загадайте число от {start_range} до {end_range}: ",
            start_range,
            end_range
        )
        
        # Выбираем метод угадывания
        print("Выберите метод:")
        print("1 - Медленный перебор")
        print("2 - Бинарный поиск ")
        
        method_choice = self.get_number_from_user("Ваш выбор: ", 1, 2)

        # Запускаем выбранный метод
        if method_choice == 1:
            result, attempts = self.slow_guess(secret_number, start_range, end_range)
        else:
            result, attempts = self.binary_guess(secret_number, start_range, end_range)
        
        # Выводим результат
        if result is not None:
            print(f"Число {result}, попыток: {attempts}")
        else:
            print(f"Число не найдено за {attempts} попыток.")


# Код для запуска напрямую, но не при импорте
if __name__ == "__main__":
    game = Game()
    game.main()