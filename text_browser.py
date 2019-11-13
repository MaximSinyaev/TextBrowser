#!/usr/bin/python3
import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style


# Defining system messages and string const
greetings = """Welcome to text-browser, hope you are here only because of interest!
For help type {color}(help){reset} or {color}help{reset}""".format(color=Fore.GREEN, reset=Fore.RESET)
help_msg = """Type url that you want to visit using full address (i.e. https://pypi.org) to display all static\
readable information from web-site.

Allowed commands:
     url   - display parsed web-page from the URL if possible
    (back) - display previous web-page
    (exit) - exits from browser
    (help) - shows this message
"""
usage = """Usage:   {} [OPTION] [PATH]
Shows parced web-pages

With no PATH uses default path for history ("./tabs"), other arguments will be ignored

    -h, --help  shows help-message
"""
bye_msg = "Goodbye"
email = "bemaxradio@gmail.com"


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
    def reopen(address):
        with open(WebPage.history[address]["path"], 'r') as f:
            line = f.read()
            print(line)

    @staticmethod
    def del_tabs():
        for tab in WebPage.history.values():
            os.remove(tab["path"])
        try:
            os.rmdir(full_path)
        except OSError:
            print("Can not delete directory {}".format(full_path))


# Reading path for directory and trying to create it
try:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(usage)
        exit(0)
except IndexError:
    pass
try:
    if sys.argv[1] == "":
        raise IndexError
    full_path = os.path.abspath(sys.argv[1])
except IndexError:
    full_path = os.path.join(os.curdir, "tabs")
except:
    print("Oops, error acquired! You can send this '{}' to {email}".format(sys.argv[1], email=email))
    exit(1)
finally:
    try:
        os.mkdir(full_path)
    except OSError:
        print("Can not access directory, please choose another one")
        exit(1)
# finally:
    directory = full_path + "/"
    print("Directory for tabs: {color}{}{reset} (default: \"./tabs\")".format(full_path, color=Fore.GREEN,
                                                                              reset=Fore.RESET))

# Starting infinite loop with user-input
url = list()
print(greetings)
while 1:
    address = input(Fore.MAGENTA + "> " + Fore.RESET).strip()
    if address == "(exit)" or address == "exit":
        break
    if address == "(back)":
        if url:
            url[-1].go_back()
            url.pop(-1)
    elif address == "(help)" or address == "help":
        print(help_msg)
    elif address in WebPage.history.keys():
        WebPage.reopen(address)
    elif check_url(address) < 0:
        print("Incorrect URL")
    else:
        url.append(WebPage(address))
WebPage.del_tabs()
print(bye_msg)
