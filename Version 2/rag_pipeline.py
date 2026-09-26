from databases import Vector_Storage
import chromadb
from google import genai
import os
from dotenv import load_dotenv

#google ai client:
load_dotenv()
ai_client = genai.Client(api_key= os.getenv('GEMINI_KEY'))

#making a client:
chroma_client = chromadb.PersistentClient(path="./my_vector_database")

#create or fetch a collection (similar to a table in sql):
collection = chroma_client.get_or_create_collection(name='vector_storage')

#intence
vec_store = Vector_Storage()


#here is our document text which we will store for 1 time only:
para = "Gardening is a wonderful hobby.It brings people closer to nature.It is the act of growing plants.You can grow flowers or vegetables.You can also care for trees.Many people use their backyard.Others use a small balcony.Some use a sunny windowsill.Space size does not matter.Working with plants brings peace.It adds joy to daily life.It allows you to slow down.You can breathe fresh air.You can enjoy natural beauty.Starting is very simple.You only need basic things.You need good soil.You need high-quality seeds.You need clean water.You need warm sunlight.First, prepare the dirt.Dig the dirt up well.Make the soil very soft.Healthy soil provides food.It helps plants grow strong.Next, plant your seeds.You can use baby plants too.Place them gently in the ground.Regular care is important.Plants need water to drink.Do not give too much water.Excess water rots the roots.They also need sunshine.Sunshine helps them make food.It makes their leaves green.Watch the daily changes.At first, you see bare dirt.Then, you water the soil.A tiny green shoot appears.It pushes through the ground.The shoot grows taller.It develops strong leaves.Beautiful flowers start to bloom.Delicious food begins to grow.A tiny seed changes completely.It becomes a tomato plant.Or it becomes a sunflower.This gives a sense of success.Gardening teaches us patience.Plants take time to grow.Growth cannot be rushed.Gardening helps your body.It helps your mind too.It is a gentle exercise.It keeps your body moving.Digging keeps you active.Planting strengthens your muscles.Weeding keeps you moving.Spend time under the sun.Sunlight gives you vitamin D.Vitamin D strengthens bones.Gardening relieves daily stress.Birds make quiet sounds.The earth smells fresh.Flowers show bright colours.These things calm the mind.Your worries disappear.You focus on the plants.Gardening helps our planet.It helps your household too.Colorful flowers attract insects.Bees visit the garden.Butterflies fly around.Insects help the environment.You can grow fresh herbs.You can grow crisp lettuce.You can grow sweet strawberries.Harvest food from your yard.Homemade food tastes better.Store food cannot compare.Homegrown food is healthier.Eating it is very satisfying.Gardening is a beautiful cycle.You give love to earth.You receive life and beauty.You get fresh food in return.It is a simple habit.It makes the world greener.It makes people happier.Nature rewards your effort.Every seed holds potential.Green spaces bring comfort.Plants respond to care.Leaves reach for the sky.Roots anchor in darkness.Rain showers bring life.Morning dew drops glisten.Seasons change the view.Spring brings new life.Summer brings full blooms.Autumn brings rich harvests.Winter brings quiet rest.Gardening connects us all.It is a timeless art.Children love to dig.Adults find quiet peace.Seniors stay very active.Every garden tells a story.Little sprouts show hope.Green leaves give oxygen.Shade trees cool the air.Soil life stays busy.Worms break down organic matter.Ladybirds eat harmful pests.Nature works in harmony.Patience brings great rewards.A green thumb develops.Learning happens every day.Mistakes help you learn.Some seeds do not grow.You try again next time.Resilience is built here.Life finds a way.Small pots hold big dreams.Urban spaces become green.Rooftops turn into farms.Community gardens bring friends.Sharing seeds is joyful.Trading advice builds bonds.Food tastes sweeter together.Flowers brighten up rooms.A simple vase holds joy.Colors lift your mood.Scents fill the evening air.Jasmine smells so sweet.Mint refreshes your senses.Rosemary boosts your focus.Nature heals our souls.Take a deep breath.Feel the soft soil.Listen to rustling leaves.Watch a caterpillar crawl.See a bee collect pollen.The world slows down.Technology fades away.Screens are forgotten.Real connection is made.Touch the living earth.Understand the food source.Respect the farming process.Value every single drop.Conserve water for plants.Use compost for nutrients.Recycle kitchen waste.Feed the soil naturally.Chemicals are not needed.Organic ways are best.Protect the local wildlife.Birds find safe shelter.Frogs catch pesky bugs.Ecosystems find perfect balance.Your yard becomes alive.Morning walks get better.Evening watering is relaxing.Sunset highlights the green.Night brings cool rest.Plants sleep at night.Morning wakes them up.The cycle never stops.Life keeps moving forward.Keep planting more seeds.Keep tending your patch.Enjoy the simple progress.Celebrate the first flower.Taste the first berry.Share your extra harvest.Keep the earth healthy.Pass down the knowledge.Teach the next generation.Love the natural world.Gardening stays with you.It is a lifelong friend.A true peaceful escape.Your own green sanctuary.Make the world happier."

#lets store the para inside the database:
# Check if collection is empty before running the store method
if collection.count() == 0:
    print("Database empty. Embedding and storing chunks...")
    vec_store.store(paragraph=para, chunk_size=20, over_lap=10)
else:
    print(f"Database loaded with {collection.count()} chunks. Skipping embedding!")


#now lets ask a query:
input = "what to grow in garden?"

#lets make it a vector too:
input_vector = vec_store.gemini_encodding(text= input)

#now we have the vector so lets see the results:
results_context = vec_store.result(query_vector= input_vector)

#now lets give the contexts to the gemini ai
interaction = ai_client.interactions.create(
    input= f"""
You are a helpful ai. You have a extra rag system installed so you can see context of similar things. Current User input {input},
User's Context: {results_context}, If you get the context then please reply with that you found the context.
""",
    model= 'gemini-3.1-flash-lite'
)

print(interaction.output_text)