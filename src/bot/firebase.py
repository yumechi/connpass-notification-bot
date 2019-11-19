import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

dot_env_file = ".env"
firebase_cred = None


def init_firebase():
    # 1度しかInitしてはいけないため
    global firebase_cred
    if firebase_cred:
        return
    load_dotenv(dot_env_file)

    credentials_file_name = os.environ.get("FIREBASE_FILENAME")
    firebase_cred = credentials.Certificate(credentials_file_name)
    firebase_admin.initialize_app(firebase_cred)


def content_diff(
    connpass_data: dict, firebase_data: dict, diff_key: str
) -> dict:
    diff = {}
    if not firebase_data:
        firebase_data = {}
    for kind_key, kind_info in connpass_data.items():
        kind_diff = {"add": [], "sub": []}
        latest_data = kind_info.get(diff_key, [])
        if kind_key not in firebase_data:
            kind_diff["add"] = latest_data
        else:
            old_data = firebase_data[kind_key].get(diff_key, [])
            kind_diff["add"] = list(set(latest_data) - set(old_data))
            kind_diff["sub"] = list(set(old_data) - set(latest_data))
        diff[kind_key] = kind_diff
    return diff


class FirebaseConnector:
    def __init__(self, content_name):
        self.content_name = content_name
        init_firebase()
        try:
            db = firestore.client()
            self.connection = db.collection(content_name)
        except Exception as e:
            print("firebase connection error: %s" % e)
            raise e


class FirebaseDataGetter(FirebaseConnector):
    def get_data(self, **kwargs):
        if hasattr(self, "content_name"):
            return getattr(self, "get_" + self.content_name, self.get_none)(
                **kwargs
            )
        return {}

    def get_none(self):
        return {}

    def get_notifications(self):
        # generatorなので
        try:
            ref = self.connection.stream()
            return [data for data in ref][0].to_dict()
        except Exception as e:
            print("get event error: %s" % e)
            raise e

    def get_event_members(self, event_key):
        # generatorなので
        try:
            ref = self.connection.stream()
            for doc in ref:
                if doc.id == event_key:
                    return doc.to_dict()
        except Exception as e:
            print("get members error: %s" % e)
            return {}


class FirebaseDataSetter(FirebaseConnector):
    def set_members(self, key, data):
        try:
            doc_ref = self.connection.document(key)
            doc_ref.set(data)
        except Exception as e:
            print("set event error: %s" % e)
            raise e


if __name__ == "__main__":
    entity = FirebaseDataGetter("notifications")
    print(entity.get_data())
