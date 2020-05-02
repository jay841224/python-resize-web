from cv2 import cv2
import requests, os, cloudstorage
from google.cloud import storage
import numpy as np
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

# Create a Cloud Storage client.
gcs = storage.Client()
# Get the bucket that the file will be uploaded to.
bucket = gcs.get_bucket('my-resize-project')
read = bucket.get_blob('mico.jpg')
a = read.download_as_string()
url = read.public_url
nparr = np.fromstring(a, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
img = cv2.resize(img, (500, 500), cv2.INTER_CUBIC)
cv2.imshow('a', img)
cv2.waitKey(0)
print(a)