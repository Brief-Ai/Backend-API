from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
import os
from langchain.prompts import PromptTemplate


os.environ['OPENAI_API_KEY'] = "OPEANAI API KEY"

from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
llm = OpenAI(temperature=0, verbose=True)

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

template = """
Extract the user's interesting topics based on the following search history:
EXAMPLES:
search history: China, United States, Russia
interesting topics: Frances, Country, Geography, international relations
================================================================
search history: {history}
interesting topics:
"""
prompt_template = PromptTemplate(
    input_variables=['history'],
    template=template
)
model = OpenAI(temperature=0, model_name="gpt-3.5-turbo")
in_text = prompt_template.format(history="basketball, baseball, NBA")

interests = model(in_text)

result = db_chain.run(f"Give ids for records whose description is about {interests} in the news_article table")
# print(type(result))

# print("--------------------------------")

print(result)
