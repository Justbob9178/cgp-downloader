import requests, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import download


load_dotenv()
username = os.getenv("username")
password = os.getenv("password")



def doDownload(choice):
    for i in ["CloudFront-Key-Pair-Id", "CloudFront-Policy", "CloudFront-Signature"]:
        if i in session.cookies.keys():
            session.cookies.pop(i)
            print(f"removed cookie {i}")
    current = books[choice-1].find(attrs={"title": True})
    id = current["title"].split(" - ")[0]
    if id == "SAHR46" or id == "MXFR47": # these are the sample/ demo books and use the url format "https://library.cgpbooks.co.uk/democontent/{id}/assets/(workspace.js/pager.js)"
        return
    dataNeeded["EVENTTARGET"] = books[choice-1].find_all("a")[0].get("id").replace("_", "$")
    dataNeeded["DigitalLicenceId"] = books[choice-1].find_all("input")[0].get("value").replace("_", "$")
    dataNeeded["DigitalLicenceNum"] = books[choice-1].find_all("input")[0].get("id")
    requestHeader = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    requestData = {
        "__CMSCsrfToken": dataNeeded["CMSCsrfToken"],
        "__EVENTTARGET": dataNeeded["EVENTTARGET"],
        "__VIEWSTATEGENERATOR": dataNeeded["VIEWSTATEGENERATOR"],
        "p$lt$ctl00$UnifiedHeader$navSearch$ctl01$txtSearch": "",
        "p$lt$ctl00$UnifiedHeader$navSearch$ctl01$currentDocHf": "130",
        "p$lt$ctl00$UnifiedHeader$navSearch$ctl03$txtSearch": "",
        "p$lt$ctl00$UnifiedHeader$navSearch$ctl03$currentDocHf": "130",
        "p$lt$Body$lt$ctl00$MyProductList$txtSearch": "",
        dataNeeded["DigitalLicenceNum"]: dataNeeded["DigitalLicenceId"],
        "__VIEWSTATE": dataNeeded["VIEWSTATE"]
    }
    for i in books[choice-1].find_all("input"): 
        if i.get("id").endswith("ctl01_btnProductLink"): # for the books with online extras
            requestData[i.get("id").replace("_", "$")] = "Book"
            requestData["__EVENTTARGET"] = ""
    response = session.post("https://www.cgpbooks.co.uk/bookspacedemo?aliaspath=%2fYour-Online-Editions", headers=requestHeader, data=requestData)
    soup = BeautifulSoup(response.text, 'html.parser')
    requestData = {
        "UserGuid": soup.find_all(attrs={"name": "UserGuid"})[0].get("value"),
        "Signature": soup.find_all(attrs={"name": "Signature"})[0].get("value"),
        "DasContentUrl": soup.find_all(attrs={"name": "DasContentUrl"})[0].get("value"),
        "DisplayTitle": soup.find_all(attrs={"name": "DisplayTitle"})[0].get("value")
    }
    response = session.post(soup.find_all(attrs={"name": "form"})[0].get("action"), data=requestData)
    download.down(id, session)

if username and password:
    print("Using preset username and password")
else:
    username = input("input username - ")
    password = input("input password - ")

session = requests.Session()

session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0",})

response = session.get("https://www.cgpbooks.co.uk/sign-in?returnurl=/your-account&aliaspath=/sign-in")

dataNeeded = {}
for i in response.text.split('>'):
    if "id=\"__CMSCsrfToken\"" in i:
        dataNeeded["CMSCsrfToken"] = i.split("\"")[7]
    elif "id=\"__VIEWSTATEGENERATOR\"" in i:
        dataNeeded["VIEWSTATEGENERATOR"] = i.split("\"")[7]
    elif "id=\"__VIEWSTATE\"" in i:
        dataNeeded["VIEWSTATE"] = i.split("\"")[7]

loginData = {
    "__CMSCsrfToken": dataNeeded["CMSCsrfToken"],
    "__VIEWSTATEGENERATOR": dataNeeded["VIEWSTATEGENERATOR"],
    "p$lt$Body$lt$ctl01$Login$Login1$UserName": username,
    "p$lt$Body$lt$ctl01$Login$Login1$Password": password,
    "p$lt$Body$lt$ctl01$Login$Login1$LoginButton": "",
    "__VIEWSTATE": dataNeeded["VIEWSTATE"],
}

response = session.post("https://www.cgpbooks.co.uk/sign-in?returnurl=/your-account&aliaspath=/sign-in", data=loginData)

response = session.get("https://www.cgpbooks.co.uk/bookspacedemo")

for i in response.text.split('>'):
    if "id=\"__CMSCsrfToken\"" in i:
        dataNeeded["CMSCsrfToken"] = i.split("\"")[7]
    elif "id=\"__VIEWSTATEGENERATOR\"" in i:
        dataNeeded["VIEWSTATEGENERATOR"] = i.split("\"")[7]
    elif "id=\"__VIEWSTATE\"" in i:
        dataNeeded["VIEWSTATE"] = i.split("\"")[7]

soup = BeautifulSoup(response.text, 'html.parser')
books = soup.find_all(attrs={"class": "digi-prod"})
print(f'Select book(s) to download -\n[0] - Download all books')
for i in range(len(books)):
    current = books[i].find(attrs={"title": True})
    print(f'[{i + 1}] - {current["title"]}')
print(f"Or input numbers seperated by commas to download multiple books. E.g '1, 3, 4, 5'")

choice = input("What books would you like to download?")

response = session.post("https://www.cgpbooks.co.uk/your-account", data=loginData)

if "," in choice:
    choices = choice.split(', ')
    for i in choices:
        doDownload(int(i))

else:

    if choice != "0":
        doDownload(int(choice))

    else:
        for i in range(len(books)):
            doDownload(int(i))