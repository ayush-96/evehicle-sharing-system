import uuid
import random
import string
from datetime import datetime


def generate_uuid():
    return (
        str(uuid.uuid4())[:-5].replace("-", "")
        + str(random.randint(1000, 9999))
        + str(random.choice(string.ascii_lowercase))
    )[:10]


def get_time_difference(time1, time2=datetime.now()):  # Returns total time difference in seconds
    time_diff = abs(time2-datetime.strptime(time1, "%Y-%m-%d %H:%M:%S.%f"))
    return time_diff.total_seconds()
