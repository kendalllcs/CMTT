# test2.py

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def print_numbers(n):
    for i in range(1, n+1):
        print(i)

# Test the functions
if __name__ == "__main__":
    print(factorial(5))  # Expected: 120
    print_numbers(5)
