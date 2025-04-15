from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver (make sure to have the correct path to your WebDriver)
driver = webdriver.Chrome()

# Open the URL
driver.get('https://www.accuweather.com/en/co/medellin/107060/weather-forecast/107060')

# Wait for the page to load
time.sleep(7)  # Adjust the sleep time as needed

# Find elements and extract data
def get_weather_data() -> dict:
    weather_data = {'hour': [], 'temperature': [], 'precipitation': []}
    while True:
        times = driver.find_elements(By.XPATH, '//div[@class="hourly-list__list-wrapper"]/div[@class="hourly-list__list"]/a[@class="hourly-list__list__item"]')
        for time in times:
            hour = time.find_element(By.XPATH, './/span[@class="hourly-list__list__item-time"]').text
            temperature = time.find_element(By.XPATH, './/span[@class="hourly-list__list__item-temp"]').text
            precipitation = time.find_element(By.XPATH, './/div[@class="hourly-list__list__item-precip"]/span').text
            if hour == '':
                return weather_data
            weather_data['hour'].append(hour)
            weather_data['temperature'].append(temperature)
            weather_data['precipitation'].append(precipitation)
        try:
            driver.find_element(By.CSS_SELECTOR, ".hourly-list__arrow-right").click()
            time.sleep(2)  # Wait for the new data to load
        except:
            break
        print(weather_data)
    return weather_data

# Function to show high precipitation probabilities and clothing advice
def show_precipitation_advice(weather_data):
    hour = weather_data['hour']
    precipitation_data = weather_data['precipitation']
    temperature_data = weather_data['temperature']

    rain = []
    for i in range(len(precipitation_data)):
        precipitation = int(precipitation_data[i].replace('%', ''))
        if precipitation >= 60:
            rain.append((hour[i], precipitation_data[i]))
    print(weather_data)
    if rain:
        print("\n".join([f"{h}:00 con probabilidad de lluvia de {p}%" for h, p in rain]))
    else:
        print("Probablemente no llueva")
    max_precipitation = max(precipitation_data, key=lambda x: int(x.replace('%', '')))
    max_hour = hour[precipitation_data.index(max_precipitation)]
    max_temperature = temperature_data[precipitation_data.index(max_precipitation)]
    print(f"La probabilidad de lluvia más alta es {max_precipitation} en el horario {max_hour}:00 cuya temperatura es {max_temperature}")

# Get all weather data
all_weather_data = get_weather_data()

# Show precipitation advice
show_precipitation_advice(all_weather_data)

driver.quit() 