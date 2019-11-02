import pandas as pd
import random
import numpy as np
from py2neo import Graph, Node, Relationship
import os

df = pd.read_csv("static/orders.csv")
df2 = pd.read_csv('static/participants.csv')
print(df2.head())

# gets max group size
df_agg = df[['client', 'people']]
df_agg = df_agg.groupby('client').max().reset_index()

# gets members per group
list2=[]
for i in range(len(df_agg)):
    num = df_agg['people'][i]
    for k in range(num): 
        list1 = list(df_agg.iloc[i])
        list1.append(random.randrange(120)+1)
        list2.append(list1)
df3 = pd.DataFrame(list2, columns=['client', 'people', 'id'])
df3.to_csv("static/membership.csv", index=False)

# gets random members per group participating in orders each day
list4 = []
for i in range(len(df)):
    num = df['people'][i]
    list1 = list(df3.loc[df3['client']==df['client'][i]]['id'])
    list2 = random.sample(list1, (num-1))
    for item in list2:
        list3 = list(df.iloc[i])
        list3.append(item)
        list4.append(list3)
df4 = pd.DataFrame(list4, columns=['date', 'time', 'people', 'catering', 'client', 'id'])

df_final = pd.merge(df4, df2, on='id', how='left')
df_final.to_csv("static/final_dataset.csv", index=False)


graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)


query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/participants.csv" AS row
		CREATE (n:Participant {id: row.id, first_name: row.first_name, last_name: row.last_name, email: row.email,
		gender: toInteger(row.gender), weight: toInteger(row.weight), healthy_feeling: toInteger(row.healthy_feeling), 
		ethnic_food: toInteger(row.ethnic_food), diet_restrictions: row.diet_restrictions})'''
graph.run(query)


query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/participants.csv" AS row
		MERGE (n:Cuisine {name: row.fav_cuisine})'''
graph.run(query)

query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/diet.csv" AS row
		MERGE (n:Diet {name: row.diet_restrictions})'''
graph.run(query)

query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/diet.csv" AS row
		MATCH (n:Participant {id: row.id}), (c:Diet {name: row.diet_restrictions})
		MERGE (n)-[rel:REQUIRES]->(c)'''
graph.run(query)

query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/participants.csv" AS row
		MATCH (n:Participant {id: row.id}), (c:Cuisine {name: row.fav_cuisine})
		MERGE (n)-[rel:LIKES]->(c)
		set rel.value = 5'''
graph.run(query)


query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/participants.csv" AS row
		MATCH (n:Participant {id: row.id}), (c:Cuisine {name: "Greek"})
		WITH n, c, toInteger(row.greek_food) as val
		WHERE val > 2 
	 	MERGE (n)-[rel:LIKES]->(c)
		set rel.value = val
		'''
graph.run(query)

query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/participants.csv" AS row
		MATCH (n:Participant {id: row.id}), (c:Cuisine {name: "Indian"})
		WITH n, c, toInteger(row.indian_food) as val
		WHERE val > 2 
	 	MERGE (n)-[rel:LIKES]->(c)
		set rel.value = val'''
graph.run(query)

query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/participants.csv" AS row
		MATCH (n:Participant {id: row.id}), (c:Cuisine {name: "Italian"})
		WITH n, c, toInteger(row.italian_food) as val
		WHERE val > 2 
	 	MERGE (n)-[rel:LIKES]->(c)
		set rel.value = val'''
graph.run(query)

query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/participants.csv" AS row
		MATCH (n:Participant {id: row.id}), (c:Cuisine {name: "Arabic"})
		WITH n, c, toInteger(row.arabic_food) as val
		WHERE val > 2 
	 	MERGE (n)-[rel:LIKES]->(c)
		set rel.value = val'''
graph.run(query)

query = '''LOAD CSV WITH HEADERS FROM "https://need2feed-ai.herokuapp.com/static/participants.csv" AS row
		MATCH (n:Participant {id: row.id}), (c:Cuisine {name: "Asian"})
		WITH n, c, toInteger(row.asian_food) as val
		WHERE val > 2 
	 	MERGE (n)-[rel:LIKES]->(c)
		set rel.value = val'''
graph.run(query)



# df = pd.DataFrame(graph.run(query))
# df.columns=['id', 'gender']
# print(df.head())