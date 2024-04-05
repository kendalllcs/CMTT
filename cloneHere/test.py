# Example Python code for testing code metrics

def calculate_factorial(n):
    """
    Function to calculate the factorial of a number.
    """
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n-1)

def fibonacci(n):
    """
    Function to calculate the nth Fibonacci number.
    """
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def is_prime(n):
    """
    Function to check if a number is prime.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Example usage:
print("Factorial of 5:", calculate_factorial(5))
print("Fibonacci sequence up to 10:")
for i in range(10):
    print(fibonacci(i), end=" ")
print("\nIs 17 prime?", is_prime(17))