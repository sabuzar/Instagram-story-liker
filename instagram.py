from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import re

class InstagramBot:
    def __init__(self, username, password, user_profile, number_follower=0):
        self.username = username
        self.password = password
        self.user1_profile = f"https://www.instagram.com/{user_profile}/"
        self.user_followers = f"https://www.instagram.com/{user_profile}/followers/"
        self.base_url = 'https://www.instagram.com'
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome()  # Update with your ChromeDriver path
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[text()='Optionele cookies afwijzen'] | //*[text()='Allow all cookies']")))
            self.driver.find_element(By.XPATH, f"//*[text()='Optionele cookies afwijzen'] | //*[text()='Allow all cookies']").click()  
            # self.driver.find_element(By.XPATH, f"//*[text()='Allow all cookies']").click()  
            time.sleep(10)
        except:
            pass
    def login(self):
        
        # self.driver.get(self.base_url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        

        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)

        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # time.sleep(4)  # Let the page load
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_ac8f']//div")))
        self.driver.find_element(By.XPATH, "//div[@class='_ac8f']//div").click()
        
    
    def story_like(self):
        try:
            self.driver.find_element(By.XPATH, f"//*[text()='Not Now']").click()  
        except:  
            pass
        self.driver.get(self.user1_profile)
        
        # get number of followers
        WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/" +user_profile+ "/followers/']//span[@class='_ac2a']")))
        span_element = self.driver.find_element(By.XPATH, "//a[@href='/" +user_profile+ "/followers/']//span[@class='_ac2a']")
        number_followers = span_element.get_attribute("title").replace(",", "")
        # if number_follower>
        print(number_followers)
        self.driver.get(self.user_followers)
        
        # get all followers
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']")))    
        all_followers = self.driver.find_elements(By.XPATH, "//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']")
        counter = 0  # Initialize a counter
        prev_length = 0

        while len(all_followers)<=int(number_followers)-1:
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR,"div[class='_aano']")
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            print(len(all_followers))
            print(counter)
            time.sleep(3)
            all_followers = self.driver.find_elements(By.XPATH, "//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']")
            if len(all_followers) == prev_length:
                counter += 1
              
            else:
                counter = 0
            if counter >= 5:  # If the length remains the same for 5 consecutive iterations
                
                break
            else:
          # Reset the counter if the length changes
                prev_length = len(all_followers)  # Update the previous length
            
        data_list = []
        all_followers = self.driver.find_elements(By.XPATH, "//div[@class='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3']")
        scrollable_div = self.driver.find_element(By.CSS_SELECTOR,"div[class='_aano']")
        self.driver.execute_script("arguments[0].scrollTop = 0;", scrollable_div)
        for i in range(len(all_followers)):
            follower = all_followers[i]
            follower1 = follower.find_element(By.XPATH, ".//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade']").text
            data = {}
            data['follower_name'] = follower1 # Replace with appropriate attribute
            
            data_list.append(data)

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data_list)
        # df
        index1=2
        index = 0
        while index < len(df):
            index1+=1
            try:
                name = df.iloc[index]['follower_name']
                try:
                   
                    try:
                        self.driver.get("https://www.instagram.com/"+name+"/")
                        xpath_expression = f"//img[@alt=\"{name}'s profile picture\"]"
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_expression)))
        
                        self.driver.find_element(By.XPATH, xpath_expression).click()
                        time.sleep(4)
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Unlike']")
                            self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Close']").click()
                            
                        except:
                            while True:
                                try:
                                    self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Next']")
                                    self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Like']").click()
                                    self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Like']").click()
                                    self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Next']").click()
                                    
                                    
                                except:
                                    self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Like']").click()
                                    self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Like']").click()
                                    break
                                time.sleep(1)
                            self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Close']").click()

                    except:
                        pass
                
                except:
                    pass
                index += 1
            except:
                pass
     
    def close_browser(self):
        self.driver.quit()
if __name__ == "__main__":
    # Replace 'your_username' and 'your_password' with your Instagram credentials
    username = 'UserName'
    password = 'PSWD'
    user_profile = 'Target Profile'
    number_followers = 0
    bot = InstagramBot(username, password, user_profile, number_followers)
    bot.login()
    bot.story_like()
    # bot.close_browser()