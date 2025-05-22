## Request
A rate limiter that should change the rates on demand

## Intro
I’m not super familiar with rate limiters, so I looked into it a bit. In short:

    A rate limiter helps prevent system overload by controlling how many operations can happen per unit of time.

And there are different styles, e.g.,

- Token Bucket
- Leaky bucket
- Sliding Window
- etc.

For this, I’ll go with **Token Bucket** since it's one of the more common and straightforward ones.

## Programming language
Even though Go is probably better for concurrency, I’m picking Python here. Most AI engineers use **Python** day to day anyway, and I’ll just ignore the GIL issue for now.

## Token Bucket
The Token Bucket algorithm is a common way to implement rate limiting.
It works like this: there’s a “bucket” that gets filled with tokens at a fixed rate. Every time a request comes in, it needs to grab a token from the bucket. If there are enough tokens, the request is allowed. If not, it gets blocked or rejected.

## Strategy
My rate limiter has 3 parameters:

- REFILL_PERIOD: fixed at **1 second**
- refill_number: starts at 5, then updates to the average of the last period’s request count and the current value, capped at **10**
- num_tokens: starts at 10, and is always 2 * refill_number, capped at **20**

The idea is to let it adjust to current demand smoothly, so that it’s responsive but doesn’t spike or swing too much.