class chunky:
    def text_chunking(self,text,chunk_size: int = 200, over_lap: int = 40):

        sentence_list = text.split('.')

        #now our paragraph became a list where full stops decide a sentences now then
        chunk_size = chunk_size
        over_lap = -over_lap
        current_chunk = ''
        chunk_id = 0
        all_chunks = []

        #now when it have first line we need to push it forward till it get fulled
        for sentences in sentence_list:

            #lets define the total words in a sentence:
            words = len(current_chunk.split())

            #lets take first line from the list and make a simple chunk in if/else:
            if words < chunk_size:
                current_chunk = current_chunk + sentences + "."
                # print('Logger:', current_chunk)
            
            else:
                dist_chunk = {"Chunk_id": chunk_id, "Text": current_chunk}
                chunk_id +=1
                current_chunk = " ".join(current_chunk.split()[over_lap:]) + sentences + "."
                all_chunks.append(dist_chunk)

        #at last when loops all lists end we will add the current_chunk in the dist and pass it to the return list:
        dist_chunk = {"Chunk_id": chunk_id, "Text": current_chunk}
        all_chunks.append(dist_chunk)
        return all_chunks