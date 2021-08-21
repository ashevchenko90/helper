import pyttsx3
import datetime
import webbrowser
import requests
from keys import API_KEY_WEATHER, OWM_END

'''
check long and lat of your location at https://www.latlong.net/
'''
CUR_LAT = 45.501690
CUR_LONG = -73.567253

API_KEY = API_KEY_WEATHER
OWM_Endpoint = OWM_END
param = {
    'lat': CUR_LAT,
    'lon': CUR_LONG,
    'units': 'metric',
    'appid': API_KEY,
    'exclude': 'current,minutely,daily',

}

'''Put your name here'''
MASTER = "Boss"

engine = pyttsx3.init('nsss')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[33].id)


'''put your favorite site here'''
my_sites = [
    'https://www.cbc.ca/news/canada/montreal?cmp=DM_SEM_NEWS_MONTREAL_RSA',
    'https://www.tsn.ca/',
    'https://www.youtube.com/'
]


def speak(text):
    engine.say(text)
    engine.runAndWait()
    # time.sleep(0.5)


def greet_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning " + MASTER)
    elif 12 <= hour < 17:
        speak("Good afternoon " + MASTER)
    elif 17 <= hour <= 21:
        speak("Good evening " + MASTER)
    else:
        speak("Good night " + MASTER)


def say_time():
    str_time = datetime.datetime.now().strftime("%H:%M")
    speak(f"Current time is {str_time}")


def open_browser():
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    speak("Opening your favorite sites")
    for link in my_sites:
        webbrowser.get(chrome_path).open(link)
    speak('Your favorite sites are open now.')


def check_weather():
    response = requests.get(OWM_Endpoint, params=param)
    response.raise_for_status()
    weather_data = response.json()
    need_umbrella = False
    for data in weather_data.get('hourly')[0:12]:
        for hourly_weather in data.get('weather'):
            if int(hourly_weather.get('id')) < 700:
                need_umbrella = True
    max_temp = round(max([temp.get('temp') for temp in weather_data.get('hourly')[0:12]]))
    speak(f'Maximum temperature in the next 12 hours is{max_temp} degrees Celsius')
    if need_umbrella:
        speak('It could be rain in the next 12 hours. Bring up an umbrella.')
    else:
        speak("No rain is expected within 12 hours.")


if __name__ == '__main__':
    greet_me()
    say_time()
    check_weather()
    open_browser()
