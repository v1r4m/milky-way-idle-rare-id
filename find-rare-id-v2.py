import urllib.request
import urllib.error
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.milkywayidle.com/v1/characters/create"
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://www.milkywayidle.com/",
    "Origin": "https://www.milkywayidle.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Cookie": f"accessToken={ACCESS_TOKEN}",
}

import string

candidates = [f"{c}{d}" for c in string.ascii_lowercase for d in string.digits]

for name in candidates:
    payload = json.dumps({"gameModeHrid": "ironcow", "name": name}).encode()
    req = urllib.request.Request(URL, data=payload, headers=HEADERS, method="POST")

    try:
        resp = urllib.request.urlopen(req)
        # 200이면 캐릭터가 생성된 거니까 즉시 알림
        body = resp.read().decode()
        print(f"[!!] {name} -> {resp.status} (created!) {body}")
        break
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if e.code == 400 and "not available" in body:
            print(f"[x] {name} -> taken")
        else:
            print(f"[?] {name} -> {e.code} {body}")
            if e.code == 429:
                print("    rate limited, waiting 5s...")
                time.sleep(5)
                continue

    time.sleep(0.3)