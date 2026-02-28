import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

URL = "https://www.luka-kp.si/wp-admin/admin-ajax.php"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

def format_date(date):
    return date.strftime("%d. %m. %Y")

start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 2, 23)

all_ships = []

current_date = start_date
while current_date <= end_date:

    payload = {
        "action": "PlanPrihodovLadij",
        "pDatumOd": format_date(current_date),
        "pDatumDo": format_date(current_date),
    }

    response = requests.post(URL, headers=headers, data=payload)

    if response.status_code != 200:
        print("Error:", response.status_code)
        current_date += timedelta(days=1)
        continue

    data = response.json()

    html = data["table"]

    soup = BeautifulSoup(html, "html.parser")

    panels = soup.find_all("div", class_="panel panel-accordion")

    print(f"{format_date(current_date)}: found {len(panels)} ships")

    for panel in panels:

        spans = panel.find_all("span")

        if len(spans) < 10:
            continue

        ship = {
            "ticanje": spans[0].text.strip(),
            "ladja": spans[2].text.strip(),
            "datum": spans[3].text.strip(),
            "dolzina": spans[4].text.strip(),
            "ugrez": spans[5].text.strip(),
            "teza_tovora": spans[6].text.strip(),
            "vrsta_tovora": spans[7].text.strip(),
            "bt": spans[8].text.strip(),
            "agent": spans[9].text.strip(),
            "ladjar": spans[10].text.strip() if len(spans) > 10 else ""
        }

        all_ships.append(ship)

    current_date += timedelta(days=1)

print("Total ships:", len(all_ships))

with open("koper_2026_vsi_podatki.csv", "w", newline="", encoding="utf-8") as f:

    fieldnames = [
        "ticanje",
        "ladja",
        "datum",
        "dolzina",
        "ugrez",
        "teza_tovora",
        "vrsta_tovora",
        "bt",
        "agent",
        "ladjar",
    ]

    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()

    writer.writerows(all_ships)

print("Saved to koper_2026_vsi_podatki.csv")