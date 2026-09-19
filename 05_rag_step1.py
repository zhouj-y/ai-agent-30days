from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#加载文档
loader = TextLoader("product_manual.txt", encoding="utf-8")
documents = loader.load()

print("===原始文档数量===")
