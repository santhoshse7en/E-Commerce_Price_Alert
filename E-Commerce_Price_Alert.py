import requests
from bs4 import BeautifulSoup
import smtplib

# product url
URL = "https://www.amazon.com/Acer-Predator-i7-9750H-Keyboard-PH315-52-78VL/dp/B07QXLFLXT/ref=sr_1_3?keywords=helios+300&qid=1577004447&sr=8-3"

sender_email_address = "SENDER_MAIL_ADDRESS"
sender_email_password = "SENDER_MAIL_PASSWORD"

receiver_mail_address = "RECIEVER_MAIL_ADDRESSES" # list

previous_price = "PREVIOUS_PRICE"


def amazon_us_price_alert(URL):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "lxml")

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:9].replace(",", ''))

    if(converted_price == previous_price):
        change_percent = ((float(converted_price)-previous_price)/previous_price)*100
        send_mail(title, price, change_percent)


def send_mail(title, price, change_percent):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender_email_address, sender_email_password)

    subject = "Price dropped " + str(change_percent) + " since added"
    body = "Product: " + \
        str(title) + "\n\n" + "Price: " + str(price) + \
        "\n\n" + 'Check the link ' + URL

    msg = f"Subject: {subject}\n\n{body}"

    if len(receiver_mail_address) == 1:
        server.sendmail(
            sender_email_address,
            receiver_mail_address[0],
            msg
        )

        print('Mail sent successfully')

        server.quit()
    else:
        for i in range(len(receiver_mail_address)):
            server.sendmail(
                sender_email_address,
                receiver_mail_address[i],
                msg
            )

            print('Mail sent successfully')

            server.quit()

amazon_us_price_alert(URL)
