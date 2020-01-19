from bs4 import BeautifulSoup
import requests


def get_weather_data(zip_code=73104):
    try:
        results = requests.get('https://weather.com/weather/today/l/' + str(zip_code) + ':4:US')
        soup = BeautifulSoup(results.content, 'html.parser')

        location = soup.find("h1", {"class": "today_nowcard-location"}).text
        temp = soup.find("div", {"class": "today_nowcard-temp"}).text
        condition = soup.find("div", {"class": "today_nowcard-phrase"}).text
        feels_like = soup.find("div", {"class": "today_nowcard-feels"}).text
        timestamp = soup.find("p", {"class": "today_nowcard-timestamp"}).text
    except Exception as e:
        return {'status': 404, 'message': str(e)}

    return {'location': location, 'temperature': temp,
            'condition': condition, 'feelsLike': feels_like,
            'timestamp': timestamp, 'status': 200}
