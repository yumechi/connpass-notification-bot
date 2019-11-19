from slacker import Slacker


def slack_post(token: str, channel_name: str, message: str, **kwargs):
    """
    Slackへのポスト処理
    """
    # FIXME: webhookに変更してSlackerをやめる
    slack = Slacker(token)
    slack.chat.post_message(channel_name, message)
    print(f"success: {channel_name}, {message}")
