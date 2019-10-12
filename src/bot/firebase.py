import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

dot_env_file = ".env"


class FirebaseSettingData:
    def __init__(self, content_name):
        load_dotenv(dot_env_file)

        credentials_file_name = os.environ.get("FIREBASE_FILENAME")
        cred = credentials.Certificate(credentials_file_name)
        firebase_admin.initialize_app(cred)

        try:
            db = firestore.client()
            self.db_ref = db.collection(content_name).stream()
        except Exception as e:
            print("firebase connection error: %s" % e)
            raise e

    def get_event(self):
        # generatorなので
        try:
            return [data for data in self.db_ref][0].to_dict()
        except Exception as e:
            print("get event error: %s" % e)
            raise e


if __name__ == "__main__":
    entity = FirebaseSettingData("notifications")
    print(entity.get_event())
