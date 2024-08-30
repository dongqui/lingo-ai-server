import os
from langchain import OpenAI, LLMChain, PromptTemplate
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

llm = OpenAI(api_key=api_key, temperature=0.7)

template = "You are a helpful assistant. Answer the following question: {question}"
prompt = PromptTemplate(template=template, input_variables=["question"])

chain = LLMChain(llm=llm, prompt=prompt)

def get_response(question):
    response = chain.run(question=question)
    return response