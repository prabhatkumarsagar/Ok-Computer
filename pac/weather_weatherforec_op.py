import requests
from pyowm.owm import OWM 
from pyowm.utils import timestamps
import geocoder

try:
    from pac import voice_io

except ModuleNotFoundError:
    import voice_io
    

g = geocoder.ip('me')
ct=(g.city)


#weather
def weather_curr():      
    api_key = "cd140d1c1404cba5de2dabf6bcd00f52" 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = base_url + "&q=" + ct + "&appid=" + api_key
    response = requests.get(url)  
    x = response.json()  
    if x["cod"] == "404":  
        voice_io.show("Oops! it looks like i ran into a problem fetching your request, maybe try again later?")
    else:
        y = x["main"]  
        curr_temperature = y["temp"]  
        curr_pressure = y["pressure"]  
        curr_humidity = y["humidity"]  
        z = x["weather"]  
        weather_desc = z[0]["description"]  
        voice_io.show(f"The current temperatre in {ct} is {str(round(curr_temperature-273))}°C" + ". It's a " +str(weather_desc))  

#weather forecaster
def weather_forec():
    voice_io.show("Sorry i am currently restricted to show weather forecast for tomorrow only. \nLook out for future updates and see if my handcuffs are set free. Here's tomorrow's weather forecast anyway.")
    owm = OWM('cd140d1c1404cba5de2dabf6bcd00f52')
    mgr=owm.weather_manager()
    loc = mgr.weather_at_place(ct)
    weather = loc.weather
    temp = weather.temperature(unit='celsius')
    for key,val in temp.items():
        if key=="temp":
            voice_io.show(f'\nThe temperature tommorow will be around {val}°C.')
        else:
            continue
    loa = mgr.forecast_at_place(ct,'3h')
    tomorrow=timestamps.tomorrow()
    forecasttt=loa.get_weather_at(tomorrow)
    status=(forecasttt.status)
    voice_io.show(f'And the sky would remain {status}')
