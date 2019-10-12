import os
from jinja2 import Environment, FileSystemLoader
from bot.firebase import FirebaseDataGetter, content_diff


class MessageTemplate:

    template_file = None

    def get_message(self, **data):
        template_file_path = os.path.join(
            os.path.dirname(__file__), "template"
        )
        env = Environment(
            loader=FileSystemLoader(template_file_path, encoding="utf8")
        )
        template = env.get_template(self.template_file)
        return template.render(data)


class NotificationMessage(MessageTemplate):

    template_file = "notification.j2"

    def create_message(self, result, event_key, event_name):
        event_members = FirebaseDataGetter("event_members").get_data(
            event_key=event_key
        )
        diff = content_diff(
            connpass_data=result,
            firebase_data=event_members,
            diff_key="member",
        )
        return self.get_message(
            **{"event_name": event_name, "my_dict": result, "diff": diff}
        )
