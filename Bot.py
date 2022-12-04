from selenium import webdriver
import random
import requests
from json import loads
from time import sleep

NEWCHAT_BUTTON = ["xpath", "/html/body/div[5]/div/div/div[1]/div[1]/div/div[11]/div/div/img"]
TOS_CHECKBOX1 = ["xpath", "/html/body/div[7]/div/p[1]/label/input"]
TOS_CHECKBOX2 = ["xpath", "/html/body/div[7]/div/p[2]/label/input"]
CONFIRM_BUTTON = ["xpath", "/html/body/div[7]/div/p[3]/input"]
CHAT_BY_TEXT_BUTTON = ["id", "chattypetextcell"]
CHAT_MSG_WRAPPER = ["class name", "chatmsgwrapper"]
CHAT_MSG_INTERACTABLE = ["class name", "chatmsg"]
TEXT_AREA = ["tag name", "textarea"]

DISCONNECT_BUTTON = ["class name", "disconnectbtn"]
DISABLED_TEXT_INPUT = ["class name", "chatmsg disabled"]


def get_random_fact():
    response = loads(requests.get("https://uselessfacts.jsph.pl/random.json?language=en").text)['text']
    return response


class OmegleBot(object):
    def __init__(self):
        self.responses = input("\nEnter a responses to be sent (or press enter without any text to send random facts). "
                               "Each response has to be separated with the vertical column character: '|'\n"
                               "=> ").split('|')

        self.br = webdriver.Chrome()
        self.br.get("https://www.omegle.com/")
        self.br.find_element(*CHAT_BY_TEXT_BUTTON).click()

        self.br.find_element(*TOS_CHECKBOX1).click()
        self.br.find_element(*TOS_CHECKBOX2).click()

        self.br.find_element(*CONFIRM_BUTTON).click()

    def click_new_chat(self):
        list(filter(lambda x: x.get_attribute("alt") == "New chat", self.br.find_elements("tag name", "img")))[0].click()

    def start_new(self):
        self.br.find_element(*DISCONNECT_BUTTON).click()
        self.br.find_element(*DISCONNECT_BUTTON).click()
        self.click_new_chat()

    def begin_sending(self):
        for _ in range(random.randint(1, 3)):
            try:
                sleep(random.randint(2, 5))
                input_wrapper = self.br.find_element(*CHAT_MSG_WRAPPER)
                if input_wrapper.find_element(*TEXT_AREA).get_attribute("class") != "chatmsg disabled":
                    input_interactable = self.br.find_element(*CHAT_MSG_INTERACTABLE)
                    input_interactable.send_keys(f"{get_random_fact() if self.responses == [] else random.choice(self.responses)}\n")
                else:
                    self.click_new_chat()
            except KeyboardInterrupt:
                break
        self.start_new()
        self.begin_sending()


def main():
    bot = OmegleBot()
    bot.begin_sending()
    input()


if __name__ == '__main__':
    main()
