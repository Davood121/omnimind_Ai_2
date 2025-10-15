"""Weather information using free API"""
import requests

def get_weather(city="Delhi"):
    """Get current weather for a city"""
    try:
        # Using wttr.in - free, no API key needed
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            temp = current['temp_C']
            feels = current['FeelsLikeC']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            
            return f"Weather in {city}: {desc}, {temp}°C (feels like {feels}°C), Humidity: {humidity}%"
        
        return f"Unable to fetch weather for {city}"
    except:
        return "Weather service unavailable"
