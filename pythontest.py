

import math
import os
import sys

import requests


print(sys.version)
print(sys.executable)

r = requests.get('https://sctmayberry.com')
print(r.status_code)
