import math
import time

def get_number():
    while True:
        try:
            n = int(input("Enter an integer to factor: "))
            if is_prime(n):
                print("Please enter a composite number greater than 1.")
            elif n > 1:
                return n
            else:
                print("Please enter an integer greater than 1.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True  # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check up to √n using 6k ± 1 optimization
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def pick_factoring_algorithm():
    print("Choose a factoring algorithm:")
    print("1. Trial Division")
    print("2. Pollard's Rho Algorithm")
    print("3. Quadratic Sieve")
    print("4, All Algorithms")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ")
    while choice not in ['1', '2', '3', '4', '5']:
        print("Invalid choice. Please select a valid option.")
        choice = input("Enter your choice (1-5): ")
    return choice



def trial_division(n):
    factors = []
    for i in range(2, int(math.isqrt(n)) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)  
    return factors


#this is a probabilistic algorithm, it may not always find a factor, this function only returns one factor
def pollards_rho(n):
    if n % 2 == 0:
        return 2
    f = lambda x: (x*x + 1) % n
    x, y, d = 2, 2, 1
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
    if d == n:
        return None  # failure
    return d

#we use this function to recursively call pollards_rho to find all factors
def factor_all(n):
    if n <= 1:
        return []
    if is_prime(n):
        return [n]
    
    factor = pollards_rho(n)
    if factor is None:
        return [n]  # failed to factor; assume prime
    # Recursively factor both sides
    return factor_all(factor) + factor_all(n // factor)


def quadratic_sieve(n):
    # Placeholder for Quadratic Sieve
    pass




# Example




number = get_number()

choice  = pick_factoring_algorithm()


if choice == '1':
    print("Using Trial Division...")
    start_time = time.time()
    factors = trial_division(number)
    end_time = time.time()
    print(f"Factors of {number}: {factors}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")


if choice == '2':
    print("Using Pollard's Rho Algorithm...")
    start_time = time.time()
    factors = factor_all(number)
    end_time = time.time()
    print(f"Factors of {number}: {factors}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    

if choice == '3':
    print("Using Quadratic Sieve...")
    start_time = time.time()
    factors = quadratic_sieve(number)
    end_time = time.time()
    print(f"Factors of {number}: {factors}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    

if choice == '4':
    print("Using all algorithms...")
    start_time = time.time()
    factors = trial_division(number)
    end_time = time.time()
    print(f"Factors of {number} using Trial Division: {factors}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    
    start_time = time.time()
    factors = factor_all(number)
    end_time = time.time()
    print(f"Factors of {number} using Pollard's Rho Algorithm: {factors}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    
    start_time = time.time()
    factors = quadratic_sieve(number)
    end_time = time.time()
    print(f"Factors of {number} using Quadratic Sieve: {factors}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")


if choice == '5':
    print("Exiting the program.")
    exit()



