import requests, json, time
import sys
from lxml import html
from lxml import etree as et
from twilio.rest import Client

session_requests = requests.session()

login_url = "https://sso-legacy.sun.ac.za/cas/login?service=https://web-apps.sun.ac.za/AcademicResults/shiro-cas"
result = session_requests.get(login_url)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='lt']/@value")))[0]

username = sys.argv[1]
password = sys.argv[2]

payload = {
		"username": username, 
		"password": password, 
		"lt": authenticity_token,
		"execution": "e1s1",
		"_eventId": 'submit'
}

result = session_requests.post(
	"https://sso-legacy.sun.ac.za/cas/login;jsessionid=7F52F16889C9AF59596895DFC27C8E90?service=https://web-apps.sun.ac.za/AcademicResults/shiro-cas", 
	data = payload, 
	headers = dict(referer=login_url)
)

home_url = "https://web-apps.sun.ac.za/AcademicResults/History.jsp?pLang=1"
result = session_requests.get(
	home_url, 
	headers = dict(referer = home_url)
)
root = et.HTML(result.text)
modules = []
marks = []

table = root[0][0]
marks = []
credits = []
for element in table:
	if(len(element) == 9):
		#Credits
		credit = element[2][0].text
		credit = "".join(credit.split())

		#Marks
		mark = element[7][0].text
		mark = "".join(mark.split())
		if((mark != "*") and (mark != "AM")):
			marks.append(int(mark))
			credits.append(int(credit))

i = 0
creditSum = 0
for mark in marks:
	creditSum += (mark/100)*credits[i]
	i += 1

creditAverage = round(((creditSum/(sum(credits)))*100), 3)
print("***************************************")
print("Student: " + username)
print("Modules: " + str(len(marks)))
print("Credits: " + str(sum(credits)))
print("Credit Weighted Average: " + str(creditAverage) + "%")
print("***************************************")