import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    temperature=0.0,  # 창의성 (0.0 ~ 2.0)
    model_name="gpt-4o",  # 모델명
)

template = ( "Provide only the feedback and improved sentence in {language} in the following format, with no extra text or labels: [Your feedback here]--[Improved sentence here, if needed] Sentence: {sentence}"
)
prompt  = PromptTemplate.from_template(template)

chain = prompt | llm

def get_response(sentence, language):
    response = chain.invoke({
        "sentence": sentence,
        "language": language
    })
    return response

print(get_response(sentence='hello world, do you hear me?', language='Korean').content)