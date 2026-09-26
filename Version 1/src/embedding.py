from chunker import chunky
from google import genai
from api import api_giver


#intences
chunk = chunky()
ai_client = genai.Client(api_key=api_giver())
print('✅[INFO]: Loaded Intences')


def gemini_embeder(text: str):
    result = ai_client.models.embed_content(
        model= "gemini-embedding-2",
        contents= text,
    )
    return(result.embeddings)

def runner(text: str, chunk_size:int=50, over_lap:int=20):
    try:
        chunked_list = chunk.text_chunking(text=text, chunk_size= chunk_size, over_lap= over_lap)

        #we will save the vectors in another list name embeded vectors:
        all_embedding_vectors = []

        #now we have a list of dictionaries which is like {"Chunk_id": chunk_id, "Text": chunk_text}
        for dict in chunked_list:
            chunk_id = dict["Chunk_id"]
            text_chunk = dict["Text"]

            #now lets give the data to gemini to embed them
            vector = { "Chunk_id":chunk_id, "Text": text_chunk, "Vectors": gemini_embeder(text= text_chunk)}
            print(f'✅[INFO]: Chunk_id {chunk_id}, Vector: {vector}')

            all_embedding_vectors.append(vector)

        return all_embedding_vectors

    except Exception as e:
        print(f'🚨[ERROR]: {e}')