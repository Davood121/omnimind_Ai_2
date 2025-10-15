"""Math calculator"""
import re

def calculate(expression):
    """Safely evaluate math expressions"""
    try:
        # Remove any non-math characters
        safe_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
        
        # Evaluate safely
        result = eval(safe_expr, {"__builtins__": {}}, {})
        
        return f"{expression} = {result}"
    except:
        return f"Cannot calculate '{expression}'"
