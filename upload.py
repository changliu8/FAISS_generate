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
        gcs_path = f"{source_dir}/{filename}"
        blob = bucket.blob(gcs_path)
        blob.upload_from_filename(local_file_path)
        print(f"Uploaded {local_file_path} to gs://{bucket_name}/{gcs_path}")

