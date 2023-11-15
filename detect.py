#Coded By Umut Özen
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

def get_form_details(form):
    print(f"{Fore.BLUE}Form:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Action:{Style.RESET_ALL}", form.get('action'))
    print(f"{Fore.GREEN}Method:{Style.RESET_ALL}", form.get('method'))

    inputs = form.find_all('input')
    for input_element in inputs:
        print(f"{Fore.YELLOW}Input:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Type:{Style.RESET_ALL}", input_element.get('type'))
        print(f"{Fore.CYAN}Name:{Style.RESET_ALL}", input_element.get('name'))
        print(f"{Fore.CYAN}Value:{Style.RESET_ALL}", input_element.get('value'))
        print("------")

def main():
    url = input("Please enter the URL: ")
    
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')

    for form in forms:
        get_form_details(form)
        print(f"{Fore.MAGENTA}URL:{Style.RESET_ALL}", url)
        print("===================")

if __name__ == "__main__":
    main()
