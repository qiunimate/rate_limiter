## Request: 
A rate limiter that should change the rates on demand

## Intro:
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