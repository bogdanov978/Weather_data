# encoding: UTF-8
import requests
import datetime


class Day:
    def __init__(self, unix_dt, sunrise, sunset, temp_night, feels_night):
        self.date = datetime.date.fromtimestamp(unix_dt).strftime('%d-%m-%Y')
        self.day_length = sunset - sunrise  # продолжительность дня в секундах
        self.temp_night = temp_night
        self.feels_night = feels_night
        self.night_diff = feels_night - temp_night
        # вычисление продолжительности светового дня
        self.day_length_seconds = self.day_length
        self.day_length_hours = self.day_length_seconds // 3600
        self.day_length_seconds %= 3600
        self.day_length_minutes = self.day_length_seconds // 60
        self.day_length_seconds %= 60

    def __str__(self):
        return str(self.date) + '\n' + self.get_day_len_time() + '\n' + str(self.temp_night) + '\n' + str(self.feels_night) + '\n' + str(self.night_diff) + '\n'

    def get_day_len_time(self):
        return "{h}:{m}:{s}".format(
            h=self.day_length_hours,
            m=self.day_length_minutes,
            s=self.day_length_seconds
        )


if __name__ == "__main__":
    API_key = input("Please, enter your API key for https://openweathermap.org/:\n")
    lon = 30.264168  # координаты Санкт-Петербурга
    lat = 59.894444
    excluded = "current,minutely,hourly,alerts"  # будут получены только дневные прогнозы

    req = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={excluded}&appid={API_key}&units=metric".format(
        lat=lat,
        lon=lon,
        excluded=excluded,
        API_key=API_key
    )
    response = requests.get(req)
    # print(response.status_code)

    days = []
    for day in response.json()["daily"]:  # получение прогнозов на ближайшие 7 дней
        days.append(
            Day(unix_dt=day["dt"],
                sunrise=day["sunrise"],
                sunset=day["sunset"],
                temp_night=day["temp"]['night'],
                feels_night=day["feels_like"]['night']
                )
        )

    day_min_night_diff = min(days, key=lambda x: abs(x.night_diff))  # abs для корректной обработки отрицательных значений
    output1_str = "{date}\nfeels like (night): {feels_like}C, fact night temperature: {temp}C, diff: {df}C\n".format(
        date=day_min_night_diff.date,
        feels_like=day_min_night_diff.feels_night,
        temp=day_min_night_diff.temp_night,
        df=day_min_night_diff.night_diff
    )
    print(output1_str)

    day_max_length = max(days[:5], key=lambda x: x.day_length)  # поиск максимума на ближайшие 5 дней
    output2_str = "max day length for [{first}, {last}] is {time} ({date})\n".format(
        first=days[0].date,
        last=days[4].date,
        time=day_max_length.get_day_len_time(),
        date=day_max_length.date
    )
    print(output2_str)
