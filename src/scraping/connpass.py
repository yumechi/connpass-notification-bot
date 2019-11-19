import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re

admin_member_count_pattern = re.compile(r"(\D+)(\d+)人$")


def scraping_run(event_url) -> dict:
    res = requests.get(event_url)
    soup = BeautifulSoup(res.text, "html.parser")
    result = get_participants_data(soup.find_all(class_="participants_table"))
    return result


def get_participants_data(parsed_data) -> OrderedDict:
    ret_data = OrderedDict()
    for table in parsed_data:
        one_table = get_table_data(table)
        ret_data.update(one_table)
    return ret_data


def get_table_data(table) -> dict:
    table_data = {}
    rows = table.findAll("tr")
    is_first_line = True
    category_name, member_count = None, None
    for row in rows:
        cells = row.findAll(["td", "th"])
        if is_first_line:
            category_name, member_count = get_first_line_info(cells)
            if not category_name:
                return table_data
            table_data[category_name] = {}
            table_data[category_name]["member_count"] = member_count
            table_data[category_name]["member"] = []
        else:
            user_name = cells[0].find(class_="display_name").get_text().strip()
            table_data[category_name]["member"].append(user_name)
        is_first_line = False
    return table_data


def get_first_line_info(cells) -> (str, int):
    category_name = cells[0].get_text().strip()

    def __default_action(x) -> (str, int):
        return "", 0

    func = __default_action

    # パターンに引っかからないものはパスする
    # 具体的には管理者とキャンセルをパスする
    # FIXME: 抽選中メンバーをどうするか
    for pattern in ("参加者",):
        if pattern in category_name:
            func = get_normal_member_data
            break
    return func(category_name)


def get_admin_member_data(category_name: str) -> (str, int):
    """
    管理者のメンバー情報を取得する。原則利用しない。
    example: category_name='管理者4人'
    """
    member_match = admin_member_count_pattern.search(category_name)
    member_count = 0
    if member_match:
        category_name = member_match.group(1)
        member_count = int(member_match.group(2))
    return category_name, member_count


def get_normal_member_data(category_name: str) -> (str, int):
    """
    通常参加者のメンバー情報を取得する。キャンセルは原則使用しない。
    example: category_name='もくもくしたい人\n              参加者\n              6人'
    example: category_name='もくもくしたい人\n              キャンセル\n              6人'
    """
    category_data = [s.strip() for s in category_name.split("\n")]
    member_count = 0
    if len(category_data) == 3:
        if "キャンセル" in category_data[1]:
            category_data[0] += "(キャンセル)"
        category_name = category_data[0]
        member_count = int(category_data[2][:-1])
    return category_name, member_count


if __name__ == "__main__":
    _res = scraping_run(
        "https://teckup-tokyo.connpass.com/event/149255/participation"
    )
    print(_res)
