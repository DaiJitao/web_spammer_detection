import requests


user_info = {'name': 'letian', 'password': '123', "班级":"二年级"}

r = requests.post("http://127.0.0.1:5660/register", data=user_info)
print(r.text)