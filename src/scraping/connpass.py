import requests
from bs4 import BeautifulSoup


def run() -> None:
    res = requests.get(
        "https://teckup-tokyo.connpass.com/event/149255/participation"
    )
    soup = BeautifulSoup(res.text, "html.parser")
    print(soup.find_all(class_="participants_table"))


if __name__ == "__main__":
    run()
