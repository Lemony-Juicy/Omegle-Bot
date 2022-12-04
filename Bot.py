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

# RECAPTCHA = ["id", "recaptcha-anchor-label"]


def get_random_fact():
    response = loads(requests.get("https://uselessfacts.jsph.pl/random.json?language=en").text)['text']
    return response


class OmegleBot(object):
    def __init__(self, responses: list, iterations: int):
        self.responses = responses
        self.iterations = iterations
        self.br = webdriver.Chrome()
        self.setup()

    def setup(self):
        self.br.get("https://www.omegle.com/")
        self.br.find_element(*CHAT_BY_TEXT_BUTTON).click()
        self.br.find_element(*TOS_CHECKBOX1).click()
        self.br.find_element(*TOS_CHECKBOX2).click()
        self.br.find_element(*CONFIRM_BUTTON).click()

    def click_new_chat(self):
        nc = []
        while not nc:
            nc = list(filter(lambda x: x.get_attribute("alt") == "New chat", self.br.find_elements("tag name", "img")))
            sleep(3)
        if nc:
            nc[0].click()


    def start_new(self):
        self.br.find_element(*DISCONNECT_BUTTON).click()
        self.br.find_element(*DISCONNECT_BUTTON).click()
        self.click_new_chat()

    def send(self):
        inp = self.br.find_element(*CHAT_MSG_INTERACTABLE)
        inp.send_keys(f"{get_random_fact() if self.responses == [] else random.choice(self.responses)}\n")

    def begin_sending(self):
        delay = random.randint(2, 5) if self.iterations != 1 else 1
        sleep(delay)
        for _ in range(self.iterations):
            input_wrapper = self.br.find_element(*CHAT_MSG_WRAPPER)
            if input_wrapper.find_element(*TEXT_AREA).get_attribute("class") != "chatmsg disabled":
                self.send()
            else:
                self.click_new_chat()
            sleep(delay)

        self.start_new()
        self.begin_sending()


def get_iterations(prompt: str) -> int:
    user_input = input(prompt)
    if user_input.isdigit():
        return int(user_input)
    return get_iterations("Input provided is not a number, please try again\n=> ")


def main():
    responses: list[str] = input(
        "\nEnter a responses to be sent (or press enter without any text to send random facts). "
        "Each response has to be separated with the vertical column character: '|'\n"
        "=> ").split('|')
    iterations: int = get_iterations(
        "Enter the number of times (iterations) you want the bot to send the response before moving to "
        "another chat.\n=> ")

    bot = OmegleBot(responses=responses, iterations=iterations)
    bot.begin_sending()


if __name__ == '__main__':
    main()
