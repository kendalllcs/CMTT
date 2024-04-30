# test3.py

def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
        return None

def is_prime(number):
    if number > 1:
        for i in range(2, number):
            if (number % i) == 0:
                return False
        else:
            return True
    else:
        return False

# Test the functions
if __name__ == "__main__":
    print(divide(10, 2))  # Expected: 5.0
    print(divide(10, 0))  # Expected: Error message + None
    print(is_prime(11))   # Expected: True
    print(is_prime(4))    # Expected: False
