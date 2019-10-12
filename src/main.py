from bot.firebase import FirebaseSettingData
from scraping.connpass import scraping_run
from bot.slack.slack_cron import slack_post

if __name__ == "__main__":
    firebase_data = FirebaseSettingData("notifications")
    for post_setting in firebase_data.get_event().values():
        message_header = f"{post_setting['event_name']}の参加者 "
        result = scraping_run(post_setting["event_url"])
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
