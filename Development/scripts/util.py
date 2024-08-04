import os
from openai import OpenAI
from config import OPENAI_API_KEY
from config import ORGANIZATION_ID
from config import MOONSHOT_API_KEY


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client_OpenAI = OpenAI(
    organization = ORGANIZATION_ID,
)


client_kimi = OpenAI(
    api_key = MOONSHOT_API_KEY,
    base_url = "https://api.moonshot.cn/v1",
)

def call_openai_completions(messages : str,temperature = 0.0):
        response = client_OpenAI.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=temperature,

                messages=[{"role": "user", "content": messages}],
        )
        completion = response.choices[0].message.content
        return completion

def call_openai_chat_with_history(history):
        response = client_OpenAI.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=history,
        )
        completion = response.choices[0].message.content
        return completion

def call_kimi_completions(messages : str):
 
        response = client_kimi.chat.completions.create(
        model = "moonshot-v1-8k",
        messages=[{"role": "user", "content": messages}],
        temperature = 0.0,
        )
        completion = response.choices[0].message.content
        return completion
def call_openai_completions_with_file(messages,file_path,temperature = 0.0):
        response = client_OpenAI.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=temperature,
                messages=[{"role": "user", "content": messages}],
                files = [file_path],
        )
        completion = response.choices[0].message.content
        return completion