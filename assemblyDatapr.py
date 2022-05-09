import json
import requests




def makeDatapr():
    url = "https://pr.zk.court.gov.ua/new.php"

    payload = "q_court_id=0708"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://pr.zk.court.gov.ua/sud0708/gromadyanam/csz/",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    with open("data/data_pr.json", "w", encoding="utf-8") as file_json:
        json.dump(response.json(), file_json, ensure_ascii=False, indent=8)


def makeDatazka():
    url = "https://zka.court.gov.ua/new.php"

    payload = "q_court_id=4806"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://zka.court.gov.ua/sud4806/gromadyanam/csz/",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    with open("data/data_zka.json", "w", encoding="utf-8") as file_json:
        json.dump(response.json(), file_json, ensure_ascii=False, indent=8)


def makeDataug():
    url = "https://ug.zk.court.gov.ua/new.php"

    payload = "q_court_id=0712"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://ug.zk.court.gov.ua/sud0712/gromadyanam/csz/",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    with open("data/data_ug.json", "w", encoding="utf-8") as file_json:
        json.dump(response.json(), file_json, ensure_ascii=False, indent=8)


def main():
        makeDatapr()
        makeDataug()
        makeDatazka()


main()





if __name__ == "__main__":
    main()
