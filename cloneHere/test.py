# test1.py

def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

# Test the function
if __name__ == "__main__":
    print(is_even(4))  # Expected: True
    print(is_even(5))  # Expected: False
