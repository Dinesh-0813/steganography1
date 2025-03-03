from google.cloud import storage
import os
from datetime import datetime

class CloudStorage:
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = "your-bucket-name"  # Replace with your bucket name
        self.bucket = self.client.bucket(self.bucket_name)

    def upload_file(self, file_path, user_id):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination_blob_name = f"user_{user_id}/{timestamp}_{os.path.basename(file_path)}"
        blob = self.bucket.blob(destination_blob_name)
        
        blob.upload_from_filename(file_path)
        return blob.public_url

    def download_file(self, blob_name, destination_file_name):
        blob = self.bucket.blob(blob_name)
        blob.download_to_filename(destination_file_name)