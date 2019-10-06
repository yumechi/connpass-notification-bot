from slacker import Slacker
import json5


def slack_post(token: str, channel_name: str, message: str, **kwargs):
    slack = Slacker(token)
    slack.chat.post_message(channel_name, message)
    print(f"success: {channel_name}, {message}")


def post_settings() -> dict:
    """
     :return:
    """
    try:
        with open(".env.json5", "r") as config_file:
            return json5.load(config_file)
    except Exception as e:
        print(f"config file load error: {e}")
        raise e
