import threading
import time
import statistics
import math

class TokenBucketRateLimiter:
    """
    A Token Bucket rate limiter.
    """

    REFILL_PERIOD = 1 # refill tokens every 1 second
    MAX_REFILL_TOKENS = 10 # Maximum refill 10 tokens every second
    MAX_TOKENS = 20 # Maximum of 20 simultaneous tokens

    def __init__(self):
        # initiate status: 10 total tokens and refill 5 every second
        self.num_tokens = 10
        self.refill_number = 5
        self.token_bucket = threading.Semaphore(self.num_tokens) # token pool
        self.lock = threading.Lock() # mutex to ensure only one thread run through given code
        self.request_count = 0 # Number of requires during the last period

        # background thread to refill tokens
        self.refill_thread = threading.Thread(target=self._refill_daemon, daemon=True)
        self.refill_thread.start()

    def _refill_daemon(self):
        while True:
            time.sleep(self.REFILL_PERIOD)
            with self.lock:
                print(f"requests during last {self.REFILL_PERIOD} second: {self.request_count})")
                # Adjust refilling number to mean of request_count and current refilling number
                new_fill_num = min(self.MAX_REFILL_TOKENS, math.ceil(statistics.mean([self.request_count, self.refill_number])))
                new_max = min(self.MAX_TOKENS, new_fill_num * 2)
                if new_max != self.num_tokens or new_fill_num != self.refill_number:
                    self.refill_number = new_fill_num
                    self.num_tokens = new_max
                    # Reset the token bucket with the new max value
                    self.token_bucket = threading.Semaphore(self.num_tokens)
                    print(f"Adjusted max_tokens to {self.num_tokens}, refill_number to {self.refill_number}")

                # Refill up to the new max
                for _ in range(self.MAX_REFILL_TOKENS):
                    if self.token_bucket._value < self.num_tokens:
                        self.token_bucket.release()

                self.request_count = 0  # reset request count

    def acquire(self, blocking=False, timeout=None):
        with self.lock:
            self.request_count += 1
        return self.token_bucket.acquire(blocking, timeout)

def test_acquire(limiter, iter, sleep_time):
    for i in range(iter):
        allowed = limiter.acquire()
        print(f"Request {i+1}: {'Allowed' if allowed else 'Rejected'}")
        time.sleep(sleep_time)

if __name__ == "__main__":
    limiter = TokenBucketRateLimiter()
    test_acquire(limiter, 10, 0.2)
    test_acquire(limiter, 10, 0.4)
    test_acquire(limiter, 10, 0.1)
    test_acquire(limiter, 10, 0.3)