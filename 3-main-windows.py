#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate

print("Testing lazy pagination (showing first 7 users):")
print("=" * 50)

user_count = 0
try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)
            user_count += 1
            if user_count >= 7:
                raise StopIteration

except (BrokenPipeError, StopIteration):
    sys.stderr.close()
    
print(f"\nShowing first {user_count} users only")