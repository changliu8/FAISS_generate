from google.cloud import storage
import os

# Initialize client
client = storage.Client()

# Reference the bucket
bucket_name = "gcp-rag"
bucket = client.bucket(bucket_name)

# Optional: list all PDFs in the bucket
blobs = bucket.list_blobs(prefix="content/")  # Adjust prefix as needed

for blob in blobs:
    if blob.name.endswith(".pdf"):
        # Set local filename
        local_path = os.path.join("content", os.path.basename(blob.name))
        os.makedirs("content", exist_ok=True)

        # Download the file
        blob.download_to_filename(local_path)
        print(f"Downloaded: {blob.name} to {local_path}")