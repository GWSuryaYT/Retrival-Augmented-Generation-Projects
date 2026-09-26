import chromadb
from google import genai
from chunker import Chunky
from dotenv import load_dotenv
import os

load_dotenv()

#making intence:
chunk = Chunky()

#making a client:
chroma_client = chromadb.PersistentClient(path="./my_vector_database")

#create or fetch a collection (similar to a table in sql):
collection = chroma_client.get_or_create_collection(name='vector_storage')

#create a client for gemini:
ai_client = genai.Client(api_key= os.getenv('GEMINI_KEY'))


class Vector_Storage:

    def __init__(self):

        print('[✅]Success: Loaded Vector_Storage')

    def gemini_encodding(self, text:str):

        encoddings = ai_client.models.embed_content(
            model="gemini-embedding-2",
            contents= text,
        )
        results_in_structured_form = encoddings.embeddings
        vector = results_in_structured_form[0].values
        return vector

    def store(self,paragraph:str, chunk_size:int, over_lap:int):
        #get the chunks=
        all_chunked_texts = chunk.chunk_maker(paragraph= paragraph, overlap= over_lap, chunk_size= chunk_size)

        #now we will get a list of chunked texts from the paragraph now lets get their vectors:
        id_chunk = 1
        for chunks_of_Texts in all_chunked_texts:

            #saving the texts + their vectors:
            collection.add(
                ids = str(id_chunk),
               documents = chunks_of_Texts,
               embeddings= self.gemini_encodding(chunks_of_Texts) 
            )
            id_chunk += 1

        print('💖Successfully stored it in the database. Thank You.')

    def result(self, query_vector, top_k:int=2):

        query_results = collection.query(
            query_embeddings= [query_vector],
            n_results= top_k
        )
        return query_results