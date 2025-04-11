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
def get_weather_data():
    weather_data = []
    while True:
        times = driver.find_elements(By.XPATH, '//div[@class="hourly-list__list-wrapper"]/div[@class="hourly-list__list"]/a[@class="hourly-list__list__item"]')
        for time in times:
            hour = time.find_element(By.XPATH, './/span[@class="hourly-list__list__item-time"]').text
            temperature = time.find_element(By.XPATH, './/span[@class="hourly-list__list__item-temp"]').text
            precipitation = time.find_element(By.XPATH, './/div[@class="hourly-list__list__item-precip"]/span').text
            if hour == '':
                return weather_data
            weather_data.append({'hour': hour, 'temperature': temperature, 'precipitation': precipitation})
        try:
            driver.find_element(By.CSS_SELECTOR, ".hourly-list__arrow-right").click()
            time.sleep(2)  # Wait for the new data to load
        except:
            break
    return weather_data

# Function to show high precipitation probabilities and clothing advice
def show_precipitation_advice(weather_data):
    for data in weather_data:
        hour = data['hour']
        precipitation = int(data['precipitation'].replace('%', ''))
        if precipitation > 75:
            advice = "Lleva abrigo"
        elif precipitation < 35:
            advice = "No lleves abrigo"
        else:
            advice = "Considera llevar abrigo"
        print(f'Hour: {hour}, Precipitation: {precipitation}%, Advice: {advice}')

# Get all weather data
all_weather_data = get_weather_data()

# Print all data
for data in all_weather_data:
    print(f'Hour: {data["hour"]}, Temperature: {data["temperature"]}, Precipitation: {data["precipitation"]}')

# Show precipitation advice
show_precipitation_advice(all_weather_data)

driver.quit() 