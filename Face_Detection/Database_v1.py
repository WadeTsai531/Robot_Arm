import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage


# -------- Firebase --------
class My_Firebase:
    def __init__(self):
        cred = credentials.Certificate('robot-arm-55a6f-firebase-adminsdk-uz5oh-635b2f17ad.json')
        firebase_admin.initialize_app(cred)
        self.database = firestore.client()

    def set_data(self, collection, document, data_set):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc_ref.set(data_set)

    def update(self, collection, document,data):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc_ref.update(data)

    def get(self, collection, document,):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc = doc_ref.get()
        doc_id = doc.id
        doc_dict = doc.to_dict()
        return doc_dict

    def delete_data(self, collection, document,):
        user_ref = self.database.collection(collection)
        doc_ref = user_ref.document(document)
        doc_ref.delete()


MF = My_Firebase()

