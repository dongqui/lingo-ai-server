import os
from langchain import OpenAI, LLMChain, PromptTemplate
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

llm = OpenAI(api_key=api_key, temperature=0.7)

template = ( "Provide only the feedback and improved sentence in {language} in the following format, with no extra text or labels: [Your feedback here]-[Improved sentence here, if needed] Sentence: {sentence}"
)
prompt = PromptTemplate(template=template, input_variables=["feedback_language", "sentence"])

chain = LLMChain(llm=llm, prompt=prompt)

def get_response(sentence, feedback_language):
    response = chain.run(sentence=sentence, feedback_language=feedback_language)
    return response

print(get_response('hello world, do you hear me?', 'Korean'))