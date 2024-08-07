
import os

from  llama_index.core import SimpleDirectoryReader,VectorStoreIndex
from llama_index.core import StorageContext


from flask import Flask,  request


openai_api_key=os.environ['OPENAI_API_KEY']

# env_vectordb_create= os.environ["VECTORDB_CREATE"]  # False



# #Persist
# # initialize client, setting path to save data
# db = chromadb.PersistentClient(path="./chroma_db")
# # create collection
# chroma_collection = db.get_or_create_collection("knowledge")
# # assign chroma as the vector_store to the context
# vector_store=ChromaVectorStore(chroma_collection=chroma_collection)
# storage_context=StorageContext.from_defaults(vector_store=vector_store)


# print(f"Args , {env_vectordb_create}!")
# if (env_vectordb_create == "True"):
#     ##Setup
#     print(f"First time , {env_vectordb_create}!")
#     docs=SimpleDirectoryReader("pdfdir").load_data()
#     #Create index and use the storage context above to change default vector store
#     index=VectorStoreIndex.from_documents(docs,storage_context=storage_context,show_progress=True)
 
# else:
#     print("Not first time", {env_vectordb_create})
#     # load your index from stored vectors
#     index = VectorStoreIndex.from_vector_store( vector_store, storage_context=storage_context)


docs=SimpleDirectoryReader("pdfdir").load_data()
index=VectorStoreIndex.from_documents(docs)
#Function to query
def query_kb(index_i,query_str):
    """Search Knowledge Base or KB"""

    query_engine=index_i.as_query_engine()
    
    response= query_engine.query(query_str)
    responseAsText = str(response).strip()
    
    return responseAsText








app = Flask(__name__)
app.static_folder = 'static'
@app.route("/")
def home():
    return "KB Seatch API "
@app.route("/kb")
def get_bot_response():
  
    user_prompt = request.args.get('prompt')
    user_query = f'Get the resolution for the Issue or Problem: {user_prompt} and then Compose the response in two parts Issue:   Resolution: ' 
    result = query_kb(index,user_query)
    return result

@app.route("/otp")
def validate_otp():
  
    user_otp_str = request.args.get('otp')
    user_query = f'OTP received : {user_otp_str}  ' 
    print(f"OTP :::::::::::: {user_query}")
    print(f'datatype of otp = {type(user_otp_str)}')
    user_otp = int(user_otp_str)
    if (user_otp==10001):
        result = "Valid"
    else:
        result="Invalid"
    return result


if __name__ == "__main__":
    app.run()