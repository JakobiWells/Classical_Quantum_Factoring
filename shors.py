import random
import math

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

# ✅ Example:
if __name__ == "__main__":
    N = 120 # Try also 21, 35, etc.
    print(f"Factoring {N} using simulated Shor's algorithm:")
    print(shor_sim(N))