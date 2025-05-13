from google.cloud import storage
import os


# Initialize client
client = storage.Client()

# Reference the bucket
bucket_name = "gcp-rag"
bucket = client.bucket(bucket_name)

source_dir = "faiss_index"

for filename in os.listdir(source_dir):
    local_file_path = os.path.join(source_dir,filename)

    
    if os.path.isfile(local_file_path):
        # Create a blob (object) in the bucket with the same name as the local file
        blob = bucket.blob(filename)

        # Upload the file to Google Cloud Storage
        blob.upload_from_filename(local_file_path)

        print(f"File {filename} uploaded to gs://{bucket_name}/{filename}")

