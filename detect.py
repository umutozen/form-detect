#Coding By Umut Özen
import requests
from bs4 import BeautifulSoup

def get_form_details(form):
    print("Form:")
    print("Action:", form.get('action'))
    print("Method:", form.get('method'))

    inputs = form.find_all('input')
    for input_element in inputs:
        print("Input:")
        print("Type:", input_element.get('type'))
        print("Name:", input_element.get('name'))
        print("Value:", input_element.get('value'))
        print("------")

def main():
    url = input("Please enter the URL: ") 
   
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')

    for form in forms:
        get_form_details(form)
        print("URL:", url)
        print("===================")

if __name__ == "__main__":
    main()
