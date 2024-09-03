import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    temperature=0.1,  # 창의성 (0.0 ~ 2.0)
    model_name="gpt-4o",  # 모델명
)

template = (
    "Provide feedback in {language}, but do not translate the original sentence. Instead, improve the original sentence in the same language. "
    "Format(without any labels): [Your feedback]--[Improved sentence only if needed]. "
    "Original sentence: {sentence}"
)
prompt  = PromptTemplate.from_template(template)

chain = prompt | llm

def get_ai_response(sentence, language):
    response = chain.invoke({
        "sentence": sentence,
        "language": language
    }).content
    
    return response
