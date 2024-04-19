import gradio as gr
import pandas as pd

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

base_url = "http://saiga.vkcloud.eazify.net:8000/v1"
base_url = "http://hackllm.vkcloud.eazify.net:8000/v1"
base_url = "http://shwars.vkcloud.eazify.net:8000/v1"

chat = ChatOpenAI(api_key="<key>",
                model = "tgi",
                openai_api_base = base_url,
                temperature=0.2)

instruct = """
Прочитай приведённый ниже в тройных обратных кавычках отзыв и кратко верни все положительные и 
отрицательные моменты в формате JSON следующего вида:
{{
  "positive" : [<список хороших моментов>],
  "negative" : [<список плохих моментов>],
}}
Отзыв: ```{review}```"
"""

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Ты редактор сайта отзывов, и твоя задача извлекать из отзывов положительные и отрицательные моменты."),
        ("human", instruct),
    ]
)

parser = JsonOutputParser()

def process(text):
    res = chat.invoke(chat_template.format_messages(review=text))
    try:
        js = parser.invoke(res)
    except:
        js = { "positive" : [] , "negative" : [] }

    mx = max(len(js['positive']),len(js['negative']))
    while len(js['positive'])<mx:
        js['positive'].append('')
    while len(js['negative'])<mx:
        js['negative'].append('')

    return pd.DataFrame(js)

demo = gr.Interface(
    fn=process,
    inputs=["text"],
    outputs=["dataframe"],
)

demo.launch(server_name="0.0.0.0",server_port=8000)
