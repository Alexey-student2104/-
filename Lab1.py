class Solution:
    def two_sum(self, nums, target):
        for num in nums:
            if not isinstance(num, int):
                raise TypeError(
                    f"Все элементы массива должны быть целыми числами. Найден элемент типа {type(num).__name__}: {num}")

        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


my_solution = Solution()

# Тестовые случаи
print(my_solution.two_sum([2, 7, 11, 15], 9))
print(my_solution.two_sum([3, 2, 4], 6))
print(my_solution.two_sum([3, 2, 4], 6))
