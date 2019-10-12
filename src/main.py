from bot.firebase import FirebaseDataGetter, FirebaseDataSetter
from message.MessageTemplate import NotificationMessage
from scraping.connpass import scraping_run
from bot.slack.slack_cron import slack_post


class Application:
    @staticmethod
    def run():
        notifications = FirebaseDataGetter("notifications")
        for event_key, post_setting in notifications.get_data().items():
            result = scraping_run(post_setting["event_url"])

            message = NotificationMessage().create_message(
                result, event_key, post_setting["event_name"]
            )

            FirebaseDataSetter("event_members").set_members(event_key, result)
            for setting in post_setting["send_to"]:
                if not bool(setting.get("enable")):
                    continue
                setting["message"] = message
                slack_post(**setting)


if __name__ == "__main__":
    Application.run()
