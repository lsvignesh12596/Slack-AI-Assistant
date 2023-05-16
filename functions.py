import os

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

load_dotenv(find_dotenv())

openai_api_key = os.environ["OPENAI_API_KEY"]

def draft_email(user_input, name = "Vignesh"):

    chat = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=1) #, openai_api_key = openai_api_key) #gpt-3.5-turbo text-davinci-003
    template = """
    You are a helpful assistant that drafts an email reply based on a new mail.
    
    Your goal is to help the user quickly create a perfect email reply by.
    
    Keep your reply short and to the point and mimic the style of the email so you reply in a similar manner to
    match the tone.
    
    Start your reply by saying: "Hi {name}, here's a draft for your reply:". And the proceed with the reply on a new line.
    
    Make sure to sign of with {signature}.
    
    """

    signature = f"Kind regards, \n{name}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "Here's a email to reply to and consider any other comments from the user for reply as well : {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt,human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt = chat_prompt)
    response = chain.run(user_input=user_input, signature=signature,name=name)

    return response

# draft_email("Hi, are you open for projects ?")