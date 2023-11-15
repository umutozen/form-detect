#Coding by Umut Özen
import requests
from bs4 import BeautifulSoup

url = "https://www.cnn.com"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    forms = soup.find_all('form')
 
    for form in forms:
        print(form)
else:
    print("Error. HTTP Kodu:", response.status_code)
