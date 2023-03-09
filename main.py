import tkinter as tk
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd


class DromParser:
    def __init__(self, n_pages):
        self.n_pages = n_pages
        self.data = []
        self.header = ["name_car", "price", "year", "engine", "power", "type_engine", "type_transmition", "type_of_drive", "mileage"]

    def parse_page(self, page):
        url = f"https://vladivostok.drom.ru/auto/used/all/page{page}/?multiselect[]=2_0_0_0&multiselect[]=31_0_0_0&multiselect[]=33_0_0_0&multiselect[]=20_0_0_0&multiselect[]=62_0_0_0&multiselect[]=57_0_0_0&multiselect[]=4_0_0_0&multiselect[]=67_0_0_0&multiselect[]=6_0_0_0"
        response = requests.get(url)
        sleep(1)
        soup = BeautifulSoup(response.text, "lxml")
        cars_div = soup.find("div", class_="css-1nvf6xk eqhdpot0")
        if cars_div:
            cars = cars_div.findAll("a", class_="css-xb5nz8 e1huvdhj1")
            for car in cars:
                name_car = car.find("div", class_="css-17lk78h e3f4v4l2")
                if name_car:
                    name_car = name_car.find("span", {"data-ftid": "bull_title"}).text.replace(",", "")
                    year = name_car.split()[-1]
                    name_car = " ".join(name_car.split()[:-1])
                else:
                    name_car = "Unknown"
                    year = "Unknown"
                price = car.find("div", class_ = "css-1dv8s3l eyvqki91").find("span", {"data-ftid":"bull_price"}).text
                price = price.replace('\xa0', '').strip().replace(" ", "")
                engine_and_power = car.findAll("span", class_="css-1l9tp44 e162wx9x0")[0].text
                if "(" in engine_and_power:
                    engine, power = engine_and_power.split(" (")
                    engine = engine.replace("л", "").strip()
                    power = power.replace("л.с.),", "").strip()
                else:
                    engine = engine_and_power.replace("л", "").strip()
                    power = "Unknown"
                type_engine = car.findAll("span", class_="css-1l9tp44 e162wx9x0")[1].text.rstrip(",") if len(car.findAll("span", class_="css-1l9tp44 e162wx9x0")) > 1 else "Unknown"
                type_transmition = car.findAll("span", class_="css-1l9tp44 e162wx9x0")[2].text.rstrip(",") if len(car.findAll("span", class_="css-1l9tp44 e162wx9x0")) > 2 else "Unknown"
                type_of_drive = car.findAll("span", class_="css-1l9tp44 e162wx9x0")[3].text.rstrip(",") if len(car.findAll("span", class_="css-1l9tp44 e162wx9x0")) > 3 else "Unknown"
                mileage = car.findAll("span", class_="css-1l9tp44 e162wx9x0")[4].text.rstrip(",") if len(car.findAll("span", class_="css-1l9tp44 e162wx9x0")) > 4 else "Unknown"
                car_data = [name_car, price, year, engine, power, type_engine, type_transmition, type_of_drive, mileage]
                self.data.append(car_data)

    def parse_all_pages(self):
        for page in range(1, self.n_pages + 1):
            self.parse_page(page)

    def save_to_csv(self, filename):
        df = pd.DataFrame(self.data, columns=self.header)
        df.to_csv(filename, index=False)
