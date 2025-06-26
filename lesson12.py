# Завдання 1
# Створіть векторну базу даних, де кожен документ – це
# вміст файлу з папки data/lesson_rag/files
#  добавте в метадані шлях до файлу
#  створіть для кожного документу ID
#  збережіть створені ID та назви відповідних файлів в
# окремий json файл
# Перевірте чи працює правильно пошук

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
import json
import dotenv
import os
from uuid import uuid4

from sqlalchemy.testing.suite.test_reflection import metadata

# завантажити api ключі з папки .env
dotenv.load_dotenv()

# отримати сам ключ
api_key = os.getenv('GEMINI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')

# створення моделі для кодування текстів
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",  # назва моделі
    google_api_key=api_key
)



# створення векторної бази даних
pc = Pinecone(api_key=pinecone_api_key)

# назва таблиці з документами
index_name = "task1"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,   # назва таблиці
        dimension=768,     # кількість чисел у векторі
        metric="cosine",   # формула для обрахунку схожості
        spec=ServerlessSpec(
            cloud="aws",         # хмарна платформа(Амазон)
            region="us-east-1"   # регіон де знаходиться сервер(впливає на оплату)
        )
    )

index = pc.Index(index_name)

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

file_names = os.listdir("data/lesson_rag/files")
print(file_names)
user_docs = []
for file_name in file_names:
    file_name = f"data/lesson_rag/files/{file_name}"
    with open(file_name, "r", encoding="UTF-8") as file:
        data = file.read()
        doc = Document(
            page_content=data,
            metadata= {"file_path": file_name}
                    )
        user_docs.append(doc)

#print(user_docs)
ids = [str(uuid4()) for _ in range(len(file_names))]
id_data = {}
for i in range(len(ids)):
    id = ids[i]
    name_file = file_names[i]
    id_data[name_file] = id

# print(id_data)
with open('data_ai.json', 'w' ) as file:
    json.dump(id_data, file)

vector_store.add_documents(user_docs, ids=ids)







# Завдання 2
# На основі створеної бази даних створіть агента та
# реалізуйте його у вигляді чат бота
# Завдання 3
# Внесіть зміни в декілька файлів. Змініть базу даних для
# цього:
#  визначте назви файлів які були змінені(вручну
# вказати списком в коді)
#  отримайте їхні ID
#  видаліть їх з бази даних
#  створіть нові документи та добавте в базу даних