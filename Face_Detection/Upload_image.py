import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import time
import os

cred = credentials.Certificate('robot-arm-55a6f-firebase-adminsdk-uz5oh-635b2f17ad.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'robot-arm-55a6f.appspot.com'
})

bucket = storage.bucket()

# output = blob.download_to_filename('Wd_2.jpg')
# print(output)

blob = bucket.blob('Wade.jpg')
with open('pic/test_3/Wade.jpg', 'rb') as my_file:
    blob.upload_from_file(my_file)
print('OK')

