import random
import string
import time


def generate_id(prefix: str = "w", length: int = 16) -> str:
    """
    Generate a unique ID with a prefix and random characters.
    Similar to the format used in the Insightful API.
    """
    chars = string.ascii_lowercase + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(length - len(prefix)))
    return f"{prefix}{random_part}"