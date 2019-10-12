from bot.firebase import FirebaseDataGetter, FirebaseDataSetter, content_diff
from scraping.connpass import scraping_run
from bot.slack.slack_cron import slack_post


class Application:
    @staticmethod
    def run():
        notifications = FirebaseDataGetter("notifications")
        for event_key, post_setting in notifications.get_data().items():
            result = scraping_run(post_setting["event_url"])

            message = Application.create_message(
                result, event_key, post_setting["event_name"]
            )
            # TODO: 更新結果のプログラムを書く
            FirebaseDataSetter("event_members").set_members(event_key, result)
            for setting in post_setting["send_to"]:
                if not bool(setting.get("enable")):
                    continue
                setting["message"] = message
                slack_post(**setting)

    @staticmethod
    def create_message(result, event_key, event_name):
        message_header = f"{event_name}の参加者 "
        message_list = [message_header]

        for key, value in result.items():
            category = key
            member_count = str(value["member_count"]) + "人"
            member = ", ".join(value["member"])
            message = f"{category} [{member_count}]: {member}"
            message_list.append(message)
        event_members = FirebaseDataGetter("event_members").get_data(
            event_key=event_key
        )
        diff = content_diff(
            connpass_data=result,
            firebase_data=event_members,
            diff_key="member",
        )

        diff_message = [""]
        for key, diff in diff.items():
            add_diff, sub_diff = diff["add"], diff["sub"]
            if not add_diff and not sub_diff:
                continue
            single_diff_header = "+++++++++++++++++++++++++++++++++++++++++"
            single_diff_message = [single_diff_header, key]
            if add_diff:
                add_member_content = (
                    f"新しい参加者 😀 {len(add_diff)}人: {'、'.join(add_diff)}"
                )
                single_diff_message.append(add_member_content)
            if sub_diff:
                sub_member_content = (
                    f"新しいキャンセル者 😰{len(sub_diff)}人: {'、'.join(sub_diff)}"
                )
                single_diff_message.append(sub_member_content)
            single_diff_message.append(single_diff_header)
            diff_message.append("\n".join(single_diff_message))
        message_list.append("\n".join(diff_message))
        return "\n".join(message_list)


if __name__ == "__main__":
    Application.run()
