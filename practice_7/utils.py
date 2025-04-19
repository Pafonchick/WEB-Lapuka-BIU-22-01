import random
from datetime import datetime, timedelta

def generate_chart_data(duration_days=2, interval_minutes=1, base_value=50):
    data = []
    end_time = datetime.now()
    start_time = end_time - timedelta(days=duration_days)
    current_time = start_time

    value = base_value

    while current_time <= end_time:
        step = random.uniform(-1, 1)
        value += step
        value = max(0, min(100, value))

        data.append({
            'timestamp': current_time.isoformat(),
            'value': round(value, 2)
        })
        current_time += timedelta(minutes=interval_minutes)

    return data