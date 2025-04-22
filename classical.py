import math
import time
import random
from sympy import primerange, factorint
from itertools import combinations


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
    print("4. Shor's Algorithm")
    print("5. All Algorithms")
    print("6. Exit")
    
    choice = input("Enter your choice (1-6): ")
    while choice not in ['1', '2', '3', '4', '5', '6']:
        print("Invalid choice. Please select a valid option.")
        choice = input("Enter your choice (1-6): ")
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
        return [n] 
    # Recursively factor both sides
    return factor_all(factor) + factor_all(n // factor)


def quadratic_sieve(n, bound=20, max_x_range=100):
    def is_B_smooth(x, base):
        factors = factorint(abs(x))
        return all(p in base for p in factors)

    def get_exponent_vector(x, base):
        factors = factorint(abs(x))
        return [factors.get(p, 0) % 2 for p in base]

    def find_linear_dependency(vectors):
        for r in range(2, len(vectors) + 1):
            for combo in combinations(enumerate(vectors), r):
                indices, rows = zip(*combo)
                summed = [sum(col) % 2 for col in zip(*rows)]
                if all(v == 0 for v in summed):
                    return indices
        return None

    sqrt_n = math.isqrt(n)
    factor_base = list(primerange(2, bound))
    x_vals, qx_vals, vectors = [], [], []

    for x in range(sqrt_n + 1, sqrt_n + max_x_range):
        qx = x * x - n
        if is_B_smooth(qx, factor_base):
            vec = get_exponent_vector(qx, factor_base)
            x_vals.append(x)
            qx_vals.append(qx)
            vectors.append(vec)
        if len(x_vals) >= len(factor_base) + 1:
            break

    deps = find_linear_dependency(vectors)
    if deps is None:
        return "Failure: No dependency found. Try increasing range or bound."

    x_prod = math.prod(x_vals[i] for i in deps) % n
    y_prod = math.prod(abs(qx_vals[i]) for i in deps)
    y_sqrt = math.isqrt(y_prod) % n

    factor = math.gcd(x_prod - y_sqrt, n)
    if 1 < factor < n:
        return (factor, n // factor)
    return "Failure: GCD did not yield nontrivial factor. Try again."





def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_power_of_integer(n):
    for b in range(2, int(math.log2(n)) + 1):
        a = round(n ** (1 / b))
        if a ** b == n:
            return True
    return False

def find_order(a, N):
    r = 1
    while pow(a, r, N) != 1 and r < N:
        r += 1
    return r if pow(a, r, N) == 1 else None

def shor_sim(N):
    if N % 2 == 0:
        return [2, N // 2]

    if is_power_of_integer(N):
        return "Failed: N is a perfect power."

    for _ in range(10):  # try up to 10 random bases
        a = random.randint(2, N - 2)
        g = gcd(a, N)
        if g > 1:
            return [g, N // g]

        r = find_order(a, N)
        if r is None or r % 2 != 0:
            continue

        x = pow(a, r // 2, N)
        if x == N - 1 or x == 1:
            continue

        f1 = gcd(x - 1, N)
        f2 = gcd(x + 1, N)
        if f1 != 1 and f1 != N:
            return [f1, N // f1]
        if f2 != 1 and f2 != N:
            return [f2, N // f2]

    return "Failed to factor — try again."




def flatten_to_primes(factors):
    if isinstance(factors, str):
        return factors  # failure message
    primes = []
    for f in factors:
        if f > 1:
            primes.extend(factorint(f).keys())
    return sorted(set(primes))




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
    print("Using Shor's Algorithm...")
    start_time = time.time()
    raw_factors = shor_sim(number)
    factors = flatten_to_primes(raw_factors)
    end_time = time.time()
    print(f"Factors of {number}: {factors}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")


if choice == '5':
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

    start_time = time.time()
    raw_factors = shor_sim(number)
    factors = flatten_to_primes(raw_factors)
    end_time = time.time()
    print(f"Factors of {number} using Shor's Algorithm: {factors}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")

if choice == '6':
    print("Exiting the program.")
    exit()



