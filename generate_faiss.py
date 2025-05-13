from langchain_community.document_loaders import PyPDFLoader

# splitting & embedding
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

# vector db
from langchain.vectorstores import FAISS


from google.cloud import storage

import os
import re

# Initialize client
client = storage.Client()

# Reference the bucket
bucket_name = "gcp-rag"
bucket = client.bucket(bucket_name)

# Optional: list all PDFs in the bucket
blobs = bucket.list_blobs(prefix="contents/")  # Adjust prefix as needed

for blob in blobs:
    if blob.name.endswith(".pdf"):
        # Set local filename
        local_path = os.path.join("contents", os.path.basename(blob.name))
        os.makedirs("contents", exist_ok=True)

        # Download the file
        blob.download_to_filename(local_path)
        print(f"Downloaded: {blob.name} to {local_path}")




pdf_folder_path = "content/"

pdf_loaders = []
for file in os.listdir(pdf_folder_path):
    if file.endswith(".pdf"):
        print("Reading file: ", file)
        pdf_loaders.append(PyPDFLoader(os.path.join(pdf_folder_path, file)))
    
#loading all pdf, and convert the context to documents.
def load_pdf(loaders):
    full_documents = []
    for loader in loaders:
        print("Converting file: ", loader.file_path)
        documents = loader.load()
        full_documents.extend(documents)
    return full_documents


#convert the documents to text , i.e. string
def convert_to_text(documents):
    full_text = ""
    for document in documents:
        if len(document.page_content) > 20:
            full_text += document.page_content
    return full_text
    


full_documents = load_pdf(pdf_loaders)
print("The total page of the textbooks are : ", len(full_documents))
full_text = convert_to_text(full_documents)
print("The total number of words are : ", len(full_text))


#remove extra spaces, such that multiple white space.
def remove_extra_spaces(text):
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

#reformat them to sentences.
def clean_text(text):
    cleaned_lines = []
    lines = text.split("\n")
    for line in lines:
        line = remove_extra_spaces(line)
        cleaned_lines.append(line)
    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text

clean_texted_text = clean_text(full_text)
print("The total number of words after cleaning are : ", len(clean_texted_text))


#write out
file_name = "cleaned_text.txt"
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(clean_texted_text)


#save it
with open('cleaned_text.txt', 'r', encoding='utf-8') as f:
    clean_texted_text = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=100
)

chunks = text_splitter.split_text(clean_texted_text)
print("The total number of chunks are : ", len(chunks))

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_db = FAISS.from_texts(
    texts = [chunk for chunk in chunks],
    embedding = embeddings,
)

vector_db.save_local("faiss_index")
print("The vector db is saved in the faiss_index folder")
