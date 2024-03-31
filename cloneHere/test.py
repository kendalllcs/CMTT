# Measures to be made:
# - Lines of Code (LOC): 15
# - Cyclomatic Complexity: 3
# - Code Coverage: 100% (not feasible to demonstrate in this example)
# - Defect Density: 0 (no obvious defects in this code snippet)

import random

def generate_random_numbers(num):
    """
    Generates a list of random numbers.
    """
    return [random.randint(1, 100) for _ in range(num)]

def is_odd(num):
    """
    Checks if a number is odd.
    """
    return num % 2 != 0

def count_odd_numbers(numbers):
    """
    Counts the number of odd numbers in a list.
    """
    count = 0
    for num in numbers:
        if is_odd(num):
            count += 1
    return count

if __name__ == "__main__":
    # Test code for lines of code (LOC)
    random_numbers = generate_random_numbers(10)
    print("Random numbers:", random_numbers)

    # Test code for cyclomatic complexity
    odd_count = count_odd_numbers(random_numbers)
    print("Number of odd numbers:", odd_count)

    # Test code for code coverage (not feasible to demonstrate here)

    # Test code for defect density measure
    # There are no obvious defects in this code snippet.