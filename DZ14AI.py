# Добавте
# в
# створену
# базу
# даних
# файл
# data/lesson_rag/huge_file.txt про умови користування гуглом
# Оскільки файл надто великий, то його треба добавляти
# частинами. Для цього:
#  прочитайте вміст файлу
#  розділіть його на окремі блоки(між блоками два
# порожніх рядка, дивись файл)
#  отримайте перший рядок кожного блоку – це його
# назва
#  створіть документи для кожного блоку. В метаданих:
# o назва файлу
# o назва блоку
#  створіть ID та добавте все в існуючу базу даних
#  добавте ID у json файл
#  перевірте агента

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore

import os
import dotenv
import json
from uuid import uuid4

dotenv.load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=api_key
)


pc = Pinecone(api_key=pinecone_api_key)
index_name = "dz14"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index,
                                   embedding=embeddings)


def parse_blocks_to_json(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    blocks = content.strip().split('\n\n\n')
    parsed_blocks = []
    documents = []

    for block in blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue

        title = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()

        parsed_blocks.append({
            'title': title,
            'content': body
        })

        doc = Document(
            page_content=body,
            metadata={
                "file_name": os.path.basename(file_path),
                "block_title": title
            }
        )
        documents.append(doc)

    # Зберігаємо json
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(parsed_blocks, file)

    print(f"Збережено у JSON: {output_file}")
    return documents


input_file = 'data/lesson_rag/huge_file.txt'
output_file = 'google_docs.json'

docs = parse_blocks_to_json(input_file, output_file)

ids = [str(uuid4()) for _ in range(len(docs))]


vector_store.add_documents(docs, ids=ids)
print(f" Додано {len(docs)} документів у Pinecone.")

user_text = "Чи можна керувати обдіковим записом дитині 12 років?"

docs = vector_store.similarity_search(
    user_text,   # запит від користувача
    k=3,          # кількість документів
)

for doc in docs:
    print(doc)