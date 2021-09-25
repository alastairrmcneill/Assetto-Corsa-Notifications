import requests
import time
import credentials


LOGIN_URL = 'http://149.7.16.11:8840/login'
TIMINGS_URL = 'http://149.7.16.11:8840/live-timing'


payload = {
    'Username': credentials.username,
    'Password': credentials.password
}

with requests.session() as s:
    s.post(LOGIN_URL, data = payload)
    r = s.get(TIMINGS_URL)

    print(r.text)



