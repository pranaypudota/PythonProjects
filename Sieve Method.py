def sieve_of_eratos(n):
    primes = []
    sieve = [True] * (n + 1)
    for x in range(2, int(n**0.5) + 1):
        if sieve[x]:
            for y in range(x*x, n + 1, x):
                sieve[y] = False
    for x in range(2, n + 1):
        if sieve[x]:
            primes.append(x)
    return primes
# Example usage
n = 30
primes = sieve_of_eratos(n)
print(f"Number of prime numbers up to {n}: {len(primes)}")
print(f"Prime numbers up to {n}: {primes}")
