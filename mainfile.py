#Welcome to The Advance Ai created by codingsheep17@gmail.com (SYED HASEEB SHAH)
#importing module
from dotenv import load_dotenv
from db import get_connection
#creating class and working on it
class SheepAi:

    def run(self):
        load_dotenv()
        self.initialize_imp_objects()
        self.user_login()

    def initialize_imp_objects(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()

    def get_connection(self):
        if not self.connection.is_connected():
            self.connection = get_connection()
            self.cursor = self.connection.cursor()

    def user_login(self):
        self.user_name = str(input("Enter Your Name --> ")).lower()
        self.user_gmail = str(input("Enter Your Gmail --> ")).lower()
        self.checking_user_existence()

    def checking_user_existence(self):
        try:      
            self.get_connection()
            self.cursor.execute("SELECT * FROM users;")
            self.users_data_fetch = self.cursor.fetchall()
            found = False
            for i in self.users_data_fetch:
                if self.user_name.strip() == i[1].strip() and self.user_gmail.strip() == i[2].strip():
                    self.user_id = i[0]
                    print(self.user_id)
                    found = True
                    break
            if found:
                print("User Logged in Successfully, Moving to Menu...")
                self.main_menu()
            else:
                print("User not found")
                self.user_account_creation_permission = str(input("Do You Want To Create a new account (y\\n)? --> ")).lower()
                if self.user_account_creation_permission == "y":
                    self.register_new_user()
                elif self.user_account_creation_permission == "n":
                    print(f"Sorry, You've to Create an Account Before Using SheepAi")
                else:
                    print("KindlY Enter Only Two Options (y\\n)")
            self.connection.commit()
        except Exception as u:
            print(f"Error Detected in checking_user_existence {u}")
                
    def register_new_user(self):
        try:
            self.get_connection()
            self.cursor.execute("""SELECT * FROM users""")
            self.fresh_fetched_data = self.cursor.fetchall()
            self.register_new_name = str(input("Enter Name You Want To Register --> ")).lower()
            self.register_new_gmail = str(input("Enter Your email --> ")).lower()
            if any(self.register_new_gmail == j[2] for j in self.fresh_fetched_data):
                print(f"Email {self.register_new_gmail} already registered")
            else:
                self.get_connection()
                self.cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s)",
                    (self.register_new_name, self.register_new_gmail)
                )
            self.connection.commit()
            self.user_id = self.cursor.lastrowid
        except Exception as r:
            print(f"Error Detected in register_new_user {r}")

    def main_menu(self):
        import cryptoapp
        import newsappspeechrecognition
        import weatherapp
        while True:
            print("""
1: Weather
2: Crypto
3: News
4: View Databases
5: Exit""")
            choice = int(input("Select: "))
            if choice == 1:
                weather_app = weatherapp.WeatherApp()
                weather_app.main(self.user_id)       
            elif choice == 2:
                cryptoapp.CryptoApp().main(self.user_id)
            elif choice == 3:
                newsappspeechrecognition.NewsApp().main(self.user_id)
            elif choice == 4:
                self.view_past_db()
            elif choice == 5:
                print("Exiting...")
                self.close_connection()
                break
            else:
                print("Invalid choice")

    def db_weather(self):
        try:
            self.get_connection()
            self.cursor.execute("""
                SELECT * FROM weather_logs
            WHERE user_id=%s
            ORDER BY query_time DESC
            LIMIT 5;""",(self.user_id,)
    )
            self.weather_recent_data = self.cursor.fetchall()
            for i in self.weather_recent_data:
                self.weather_id = i[0]
                self.user_w_table_id = i[1]
                self.user_city = i[2]
                self.temperature = i[3]
                self.weather_cond = i[4]
                self.time = i[5]
                print(self.weather_id, self.user_w_table_id, self.user_city, self.temperature, self.weather_cond,
                    self.weather_cond, self.time)
            self.close_connection()
        except Exception as view_db_weather_error:
            print(f"Error occured in history of weather {view_db_weather_error}")
    def db_crypto(self):
        try:
            self.get_connection()
            self.cursor.execute("""
                SELECT * FROM crypto_logs
            WHERE user_id=%s
            ORDER BY query_time DESC
            LIMIT 5;""",(self.user_id,)
    )
            self.cyrpto_recent_data = self.cursor.fetchall()
            for i in self.cyrpto_recent_data:
                self.crypto_id = i[0]
                self.user_c_table_id = i[1]
                self.coin_name = i[2]
                self.price_usd = i[3]
                self.crypto_time = i[4]
                print(self.crypto_id, self.user_c_table_id, self.coin_name, 
                    self.price_usd, self.crypto_time)
            self.close_connection()
        except Exception as view_crypto_db_error:
            print(f"Error occured in history of crypto {view_crypto_db_error}")

    def db_news(self):
        try:
            self.get_connection()
            self.cursor.execute("""
            SELECT * FROM news_logs
            WHERE user_id=%s
            ORDER BY query_time DESC
            LIMIT 5;""",(self.user_id,)
    )
            self.news_recent_data = self.cursor.fetchall()
            for i in self.news_recent_data:
                self.news_id = i[0]
                self.user_n_table_id = i[1]
                self.headline = i[2]
                self.source= i[3]
                self.time = i[4]
                print(f"{self.news_id}|{self.user_n_table_id}|{self.headline}|{self.source}|{self.time}")
            self.close_connection()
        except Exception as view_db_news_error:
            print(f"Error occured in history of news {view_db_news_error}")
    def view_past_db(self):
        try:
            running = True
            while running:
                print("""SELECT YOUR CHOICE (1-4)
1: Weather History
2: Crypto History
3: News History
4: Exit to menu""")
                self.user_db_choice = int(input("Enter Your choice --> "))
                if self.user_db_choice == 1:
                    self.db_weather()
                elif self.user_db_choice == 2:
                    self.db_crypto()
                elif self.user_db_choice == 3:
                    self.db_news()
                elif self.user_db_choice == 4:
                    print("Returning to main menu..")
                else:
                    print("Kindly Enter The Above Option")
        except Exception as view_db_menu:
            print(f"Error Occured {view_db_menu}")

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":    
    sheep_ai = SheepAi()
    sheep_ai.run()