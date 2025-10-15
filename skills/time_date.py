"""Time and date utilities"""
from datetime import datetime
import pytz

def get_current_time(timezone="Asia/Kolkata"):
    """Get current time in specified timezone"""
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"Current time: {now.strftime('%I:%M %p, %A, %B %d, %Y')}"
    except:
        now = datetime.now()
        return f"Current time: {now.strftime('%I:%M %p, %A, %B %d, %Y')}"

def get_date():
    """Get current date"""
    now = datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}"
