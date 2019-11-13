import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style


try:
    full_path = os.path.abspath(sys.argv[1])
except IndexError:
    full_path = os.path.join(os.curdir, "tabs")
try:
    os.mkdir(full_path)
except OSError:
    pass
directory = full_path + "/"


def check_url(url):
    url_features = ["http", ".", "//"]
    for feat in url_features:
        if url.count(feat) < 1:
            return -1
    return 1


class WebPage():
    history = {}
    stack = []
    parse_tags = ['p', 'a', 'h1', 'h2', 'h3', 'h3', 'h4', 'h5', 'h6', 'h7', 'ul', 'ol', 'li']

    def __init__(self, url):
        self.sitename = url.split("//")[1].split(".")[-2].lower()
        WebPage.history[self.sitename] = dict(zip(["url", "path"], [url, directory + self.sitename.capitalize()]))
        self.stack.append(self.sitename)
        with open(WebPage.history[self.sitename]["path"], "w") as file:
            file.writelines(self.open(url))

    def go_back(self):
        if len(self.stack) > 1:
            self.reopen(self.stack[-2])
            self.stack.pop(-1)
            self.stack.pop(-1)
        else:
            print("No way back, this is the End of your history!")

    @staticmethod
    def open(url):
        r = requests.get(url)
        text = ""
        last_line = ""
        soup = BeautifulSoup(r.content, 'html.parser')
        output = soup.find_all(WebPage.parse_tags)
        for i in output:
            line = i.string
            if line and line != last_line:
                last_line = line
                if i.name == "a":
                    text += Fore.BLUE + line.strip() + Fore.RESET
                else:
                    text += line.strip()
                text += "\n"
        print(text)
        return text

    @staticmethod
    def reopen(adress):
        with open(WebPage.history[adress]["path"], 'r') as f:
            line = f.read()
            print(line)


url = list()
while 1:
    adress = input().strip()
    if adress == "(exit)":
        break
    if adress == "(back)":
        if url:
            url[-1].go_back()
    elif adress in WebPage.history.keys():
        WebPage.reopen(adress)
    elif check_url(adress) < 0:
        print("Incorrect URL")
    else:
        url.append(WebPage(adress))
