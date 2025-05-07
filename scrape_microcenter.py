# from dotenv import load_dotenv
# load_dotenv()

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

def is_in_stock():
    url = "https://www.microcenter.com/product/689241/intel-arc-b580-limited-edition-dual-fan-12gb-gddr6-pcie-40-graphics-card?storeid=105"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Only search inside divs with class="inventory"
    inventory_div = soup.find("div", class_="inventory")

    # Check for "SOLD OUT" inside that div
    sold_out_element = None
    if inventory_div:
        sold_out_element = inventory_div.find(string=lambda s: s and "sold out" in s.lower())

    return sold_out_element is None  # True if NOT sold out

def send_email():
    msg = MIMEText("The Intel Arc A580 is IN STOCK at MicroCenter!\n\nCheck here:\nhttps://www.microcenter.com/product/689241/intel-arc-b580-limited-edition-dual-fan-12gb-gddr6-pcie-40-graphics-card?storeid=105")
    msg['Subject'] = "Intel Arc A580 AVAILABLE!"
    msg['From'] = os.environ['EMAIL_FROM']
    msg['To'] = os.environ['EMAIL_TO']

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ['EMAIL_FROM'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

if __name__ == "__main__":
    if is_in_stock():
        send_email()

# if True:
#     send_email()

