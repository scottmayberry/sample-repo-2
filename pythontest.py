
import requests


r = requests.get('https://sctmayberry.com')
print(r.status_code)
print(r.ok)
