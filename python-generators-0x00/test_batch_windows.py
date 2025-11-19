#!/usr/bin/python3
import sys
from itertools import islice

processing = __import__('1-batch_processing')

# Test with batch size 50 and show only first 10 users
print("First 10 users over age 25 (batch size 50):")
print("=" * 50)

# We need to capture the output since batch_processing prints directly
# Let's modify our approach for testing

# Alternative: Test the stream_users_in_batches directly
print("\nTesting stream_users_in_batches with batch_size=5:")
batch_gen = processing.stream_users_in_batches(5)

batch_count = 0
user_count = 0

for batch in batch_gen:
    batch_count += 1
    print(f"\nBatch {batch_count}:")
    
    for user in batch:
        if user['age'] > 25:
            user_count += 1
            print(f"  {user}")
            
            # Stop after 10 users
            if user_count >= 10:
                break
    if user_count >= 10:
        break

print(f"\nProcessed {batch_count} batches")
print(f"Found {user_count} users over age 25")