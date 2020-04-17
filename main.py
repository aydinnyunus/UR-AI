import codecs
import re
from time import sleep
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os


class URAI:
    def __init__(self, phone_number, sender, receiver):
        self.phone_number = phone_number
        self.sender = sender
        self.receiver = receiver

    def element_presence(self, driver, by, xpath, time):
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, time).until(element_present)

    def send_whatsapp_msg(self, chatbot, phone_number):
        driver = webdriver.Chrome(executable_path=os.path.abspath(os.getcwd()) + "chromedriver")
        driver.get("https://web.whatsapp.com/")
        sleep(5)
        driver.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_number))
        sleep(7)
        self.element_presence(driver, By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]', 30)

        # for i in range(29):
        # msg = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div/div[3]/div[{}]/div/div/div/div['
        # '1]/div/span[1]/span'.format(i)).get_attribute("innerHTML").splitlines()
        # print(msg)
        msg = driver.find_element(By.XPATH,
                                  '//*[@id="main"]/div[3]/div/div/div[3]/div[28]/div/div/div/div[1]/div/span[1]').text
        print(msg)
        response = chatbot.get_response(msg)
        print(response)
        response = str(response)
        txt_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        txt_box.send_keys(response)
        txt_box.send_keys("\n")

    def remove_emoji(self, string):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)

        return emoji_pattern.sub(r'', string)

    def modify_text(self):
        with codecs.open('new.txt', 'r', encoding='utf8') as f:
            text = f.readlines()
            for line in text:
                line.replace('"', "'")
                line.replace(',', '')
                line.replace(':', '')

        with codecs.open('wp.txt', 'a', encoding='utf8') as t:
            t.write('{\n')
            t.write('"conversations": [\n[')
            t.close()
        i = 1
        j = 0

        for line in text:

            if self.receiver in line:
                line = '"' + line[len(self.receiver) + 21::] + '"'
                line = line.replace("\n", '')

            elif self.sender in line:
                line = '"' + line[len(self.sender) + 21::] + '"'
                line = line.replace("\n", '')

            with codecs.open('wp.txt', 'a', encoding='utf8') as t:
                t.write(line)
                if i % 2 != 0:
                    t.write(',')

                j += 1

                if j % 2 == 0:
                    t.write('[')

                if i % 2 == 0:
                    t.write("],\n[")

                j += 1

                i += 1
                t.close()

        with codecs.open('wp.txt', 'a', encoding='utf8') as t:
            t.write(']]}')

    def main(self):

        chatbot = ChatBot('Your Chat BOT')

        file_path = os.path.abspath(os.getcwd()) + 'WhatsappMessages.txt'

        # First, lets train our bot with some data
        trainer = ChatterBotCorpusTrainer(chatbot)

        trainer.train(file_path)

        self.modify_text()
        self.remove_emoji(file_path.read())
        self.send_whatsapp_msg(chatbot, self.phone_number)


if __name__ == '__main__':
    phone_number = "PHONE NUMBER WITH COUNTRY CODE"
    sender = "SENDER NAME ON WHATSAPP"
    receiver = "RECEIVER NAME ON WHATSAPP"

    URAI(phone_number=phone_number, sender=sender, receiver=receiver).main()
