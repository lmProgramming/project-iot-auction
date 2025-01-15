import time
from functools import wraps


def debounce(debounce_delay=1):
    def decorator(func):
        # This will store the last processed time for each card_id, unique to each decorated function
        last_processed_time = {}

        @wraps(func)
        def wrapper(card_uuid, *args, **kwargs):
            # Get the current time
            current_time = time.time()

            # Check if the card has been processed recently (within debounce_delay)
            if (
                card_uuid not in last_processed_time
                or (current_time - last_processed_time[card_uuid]) >= debounce_delay
            ):
                # Call the original function if debouncing is not active
                result = func(card_uuid, *args, **kwargs)

                # Update the last processed time for this card_id
                last_processed_time[card_uuid] = current_time

                return result
            else:
                # Optionally, you can return None or some indicator that the card was ignored
                last_processed_time[card_uuid] = current_time
                print(f"Debounced: {card_uuid} ignored")
                return (None, None)

        return wrapper

    return decorator
