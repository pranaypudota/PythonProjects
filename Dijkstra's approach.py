import heapq

def dijkstra_sieve(n):
    """
    Generate primes up to n using a priority queue (Dijkstra's Sieve).
    Returns the list of primes.
    """
    primes_pool = [(4, 2)]  # (next multiple to cross out, prime that generated it)
    heapq.heapify(primes_pool)
    primes = [2]

    for i in range(3, n + 1):
        # Remove all entries whose multiple is less than i
        while primes_pool and primes_pool[0][0] < i:
            multiple, prime = heapq.heappop(primes_pool)
            heapq.heappush(primes_pool, (multiple + prime, prime))

        if primes_pool and primes_pool[0][0] == i:
            # i is composite — update the heap
            multiple, prime = heapq.heappop(primes_pool)
            heapq.heappush(primes_pool, (multiple + prime, prime))
        else:
            # i is prime
            primes.append(i)
            heapq.heappush(primes_pool, (i * i, i))

    return primes

n = 100
primes = dijkstra_sieve(n)
print(f"Number of prime numbers up to {n}: {len(primes)}")
print(f"Prime numbers up to {n}: {primes}")
