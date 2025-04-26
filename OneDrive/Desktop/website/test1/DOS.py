import requests
import threading

url = "httpspio://127.0.0.1:5000/"

def flood():
    while True:
        try:
            requests.get(url)
        except:
            pass

# Launch 50 threads
for _ in range(50):
    t = threading.Thread(target=flood)
    t.start()