#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

# print processed users in a batch of 50, but limit output
print("Users over age 25 (showing first 10 only):")
print("=" * 50)

# We'll use a counter to limit output
user_count = [0]  # Use list to make it mutable in nested functions

def limited_print(user):
    if user_count[0] < 10:
        print(user)
        user_count[0] += 1
    else:
        raise StopIteration

# Modify batch_processing temporarily for testing
original_batch_processing = processing.batch_processing

def limited_batch_processing(batch_size):
    import sys
    
    batch_stream = processing.stream_users_in_batches(batch_size)
    
    try:
        for batch in batch_stream:
            filtered_users = [user for user in batch if user['age'] > 25]
            
            for user in filtered_users:
                limited_print(user)
                if user_count[0] >= 10:
                    return
    except StopIteration:
        return

# Run the limited version
limited_batch_processing(50)
print(f"\nShowing first {user_count[0]} users only")