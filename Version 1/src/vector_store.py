from embedding import runner
from embedding import gemini_embeder
from vector_math import vector_mathy

math = vector_mathy()

class VectorStore:
    def __init__(self):
        self.db = []

    def add_chunks(self, paragraph, chunk_size:int =30, over_lap:int =15):

        #now here we will call the runner to embed our paragraph
        whole_list_of_dict_vectors = runner(text= paragraph, chunk_size= chunk_size, over_lap= over_lap)

        #now we will save the results on the memory database:
        for dict in whole_list_of_dict_vectors:
            self.db.append(dict)


    def search(self, query_text: str, top_k: int =2):

        #step a: getting our current queary's vectors:
        current_text_vector = gemini_embeder(text= query_text)
        current_vector = current_text_vector[0].values

        #temp dict to save the ranked similarity based chunks:
        top_results = []

        #step b: now from memory database we will extract the vectors and give them scores
        for dict in self.db:
            content_embedding = dict['Vectors']
            chunk_vector = content_embedding[0].values

            chunk_text = dict['Text']

            #now lets calculate the similarity
            similarity = math.cosine_similarity(current_vector, chunk_vector)
            dictionay = {"text": chunk_text, "score": similarity}

            #save the results of similarity
            top_results.append(dictionay)

        # step D: sort the list in descending order based on similarity score:
        key = lambda x: x['score']
        sorted_results = sorted(top_results, key=key, reverse=True)

        return sorted_results[:top_k]


# obj = VectorStore()

# paragraph = "Gardening is the rewarding practice of cultivating and caring for plants, including flowers, vegetables, and aromatic herbs, which connects people directly with nature while significantly lowering daily stress levels. It can be done almost anywhere, ranging from expansive outdoor backyards to small windowsill container pots in city apartments. Space exploration expands human knowledge by sending robotic probes and astronauts to discover the mysteries of the universe, using advanced rovers and powerful telescopes to study distant galaxies, moons, and the surface of Mars. Developing technologies for long-term space travel also helps researchers learn how to sustain life, such as growing fresh food in microgravity. Cooking is the creative art of using heat and precise techniques to transform raw ingredients into delicious meals, allowing anyone to express unique cultural traditions by experimenting with different herbs, spices, and cooking styles. Ultimately, mastering basic culinary skills builds self-reliance and promotes a healthier lifestyle through fresh, home-cooked food."

# obj.add_chunks(paragraph= paragraph)
# a =obj.search(query_text="How do I plant tomatoes?", top_k=2)

# print("💖Results came out man after 12hrs of grinding: \n",a)