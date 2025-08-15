#news app using Gnews Api
#creating class
import requests
import pyttsx3
import os
from dotenv import load_dotenv
from db import get_connection

class NewsApp:
    def main(self, user_id):
        load_dotenv()
        self.user_news_db_id = user_id
        self.engine_init = pyttsx3.init()
        self.engine = self.engine_init
        self.engine.setProperty("rate", 135)
        try:
          self.connection = get_connection()
          self.cursor = self.connection.cursor()
        except Exception as db_err:
          print(f"Database error: {db_err}")
        self.ip_api()
    
    def speech_engine(self, text : str):
        try:
            self.text = text
            print(self.text)
            self.engine.say(self.text)
            self.engine.runAndWait()
        except Exception as error:
            print(f"Error While Speech Recognition")

    def ip_api(self):
        self.ip_api_url = "http://ip-api.com/json/"
        self.response = requests.get(self.ip_api_url).json()
        self.country_code = self.response["countryCode"].lower()  # e.g. 'pk'
        self.country_name = self.response["country"]
        self.api_working()
        
    def api_working(self):
        try:
            self.api_key = os.getenv("NEWS_API_KEY")
            self.api_url = f"https://gnews.io/api/v4/top-headlines?country={self.country_code}&apikey={self.api_key}"
            self.data_fetch = requests.get(self.api_url)
            self.data = self.data_fetch.json()
            self.user_menu()
        except Exception:
            self.speech_engine("""An Error Occured While Fetching Data
1: Try Again, Check Your Internet Connection
2: Try Again By Restarting the App
3: Check If the Server is Down or Crashed.""")
            
    def changed_country_api_working(self):
        try:
            self.api_key = os.getenv("NEWS_API_KEY")
            self.api_url = f"https://gnews.io/api/v4/top-headlines?country={self.country_code}&apikey={self.api_key}"
            self.data_fetch = requests.get(self.api_url)
            self.data = self.data_fetch.json()
            self.top_headlines()
        except Exception:
            self.speech_engine("""An Error Occured While Fetching Data
1: Try Again, Check Your Internet Connection
2: Try Again By Restarting the App
3: Check If the Server is Down or Crashed.""")
    
    def top_headlines(self):
        self.index_no = 0
        for i in range(1,5):
            self.title = self.data["articles"][self.index_no]["title"]
            self.source = self.data["articles"][self.index_no]["source"]["name"]
            self.url = self.data["articles"][self.index_no]["url"]
            print("******")
            self.cursor.execute(
                "INSERT INTO news_logs (user_id, headline, source) VALUES (%s,%s,%s)",
                (self.user_news_db_id, self.title, self.source)
            )
            self.connection.commit()
            self.speech_engine(f"Title is {self.title}")
            self.speech_engine(f"Source is {self.source}")
            print(f"Url --> {self.url}")
            print("******")
            self.index_no += 1
        

    def news_categories(self):
        try:    
            self.speech_engine(f"""--- Choose a News Category ---
1. Technology
2. Business
3. Sports
4. Entertainment
5. Politics
6. World""")
            self.news_category = int(input("Enter (1-6) --> "))
            self.cateogries = {
                1: "technology",
                2: "business",
                3: "sports",
                4: "entertainment",
                5: "politics", 
                6: "world"
            }

            if self.news_category in self.cateogries:
                self.cateogry = self.cateogries[self.news_category]
                self.api_url = f"https://gnews.io/api/v4/top-headlines?category={self.cateogry}&country={self.country_code}&apikey={self.api_key}"
                self.data_fetch = requests.get(self.api_url)
                self.data = self.data_fetch.json()
                self.top_headlines()
            else:
                self.speech_engine("Invalid input. Choose a number between 1 and 6.")
        except ValueError:
            self.speech_engine("Please enter a number only (1-6).")

        
    def change_country(self):
        try:
            country_code_input = input("--- Enter the Country Code (e.g. us, gb, pk) --> ").lower()
            if len(country_code_input) == 2:
                self.country_code = country_code_input
                self.speech_engine(f"Country changed to {self.country_code.upper()}.")
                self.api_working()  # <-- fetch new data right away
            else:
                self.speech_engine("Please enter a valid 2-letter country code.")
        except Exception as e:
            self.speech_engine(f"Error while changing country: {e}")

    def user_menu(self):
        running = True
        while running:
            self.user_menu_input = 0
            try:
                print(f"""Tell Your Choice
1: Top Headlines
2: News Categories
3: Filter by Country
4: Exit""")
                self.user_menu_input = int(input("Enter Your Choice --> "))
                if self.user_menu_input == 1:
                    self.top_headlines()
                elif self.user_menu_input == 2:
                    self.news_categories()
                elif self.user_menu_input == 3:
                    self.change_country()
                elif self.user_menu_input == 4:
                    self.speech_engine("Thanks for using NewsApp")
                    self.cursor.close()
                    self.connection.close()
                    running = False
            except ValueError:
                self.speech_engine("Kindly Enter Only Option Ranging From (1-4)")

if __name__ == "__main__":
    NewsApp().main()