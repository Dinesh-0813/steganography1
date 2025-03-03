from functools import wraps
from flask import request, abort
import time
from collections import defaultdict

class RateLimit:
    def __init__(self, calls=15, period=900):
        self.calls = calls
        self.period = period
        self.records = defaultdict(list)

    def __call__(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            current = time.time()
            ip = request.remote_addr

            self.records[ip] = [t for t in self.records[ip] if current - t < self.period]
            if len(self.records[ip]) >= self.calls:
                abort(429)  # Too Many Requests

            self.records[ip].append(current)
            return f(*args, **kwargs)
        return decorated

rate_limit = RateLimit()