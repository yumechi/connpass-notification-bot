from scraping.connpass import scraping_run
from bot.slack.slack_cron import post_settings, slack_post

if __name__ == "__main__":
    for url, post_setting in post_settings().items():
        message_header = f"{post_setting['title']}の参加者 "
        result = scraping_run(url)
        message_list = [message_header]
        for key, value in result.items():
            category = key
            member_count = str(value["member_count"]) + "人"
            member = ", ".join(value["member"])
            message = f"{category} [{member_count}]: {member}"
            message_list.append(message)
        for setting in post_setting["send_to"]:
            if not bool(setting.get("enable")):
                continue
            setting["message"] = "\n".join(message_list)
            slack_post(**setting)
