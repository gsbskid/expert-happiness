import streamlit as st

from langchain_cohere import ChatCohere
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage
from langchain_community.vectorstores import FAISS

options = st.sidebar.selectbox(
    'Type of Document Formatting' , 
    options = [
        'Unstructured' , 
        'Full Text'
    ]
)


def format_docs(docs):
    '''
    Function to format the documents

    Args :
        1) docs : list : list of documents

    Returns :
        1) str : formatted documents
    '''
    return "\n\n".join(doc.page_content for doc in docs)


def get_answer(question) :
    '''
    Function to get the answer

    Args :
        1) question : str : question to ask

    Returns :
        1) str : answer
    '''

    cohere_api_key = 'FELFXgLGfcqsy4eh4Q75dXNT7VyIQjKZmhkiIug3'

    with st.spinner('Understanding the docs... This can take a while if loading for the first time') :

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        if options == 'Unstructured' : vectorstore = FAISS.load_local(
            'unstructured_vc' , 
            embeddings = embeddings , 
            allow_dangerous_deserialization = True 
        )


        elif options == 'Full Text' : vectorstore = FAISS.load_local(
            'normal_vc' , 
            embeddings = embeddings , 
            allow_dangerous_deserialization = True 
        )

    with st.spinner('Getting Relevant Text...') : similar_docs = vectorstore.similarity_search(question , fetch_k = 20)
    with st.spinner('Running LLM...') : 


        context = ''
        for doc in similar_docs : context += doc.page_content
        if len(context.split()) > 4000 : st.write(f'The provided query has huge context of {len(context.split())} Tokens exceeding the 4801 Token Limit of the model, trucnating the context')
        context = ' '.join(context.split()[:4000])

        prompt = open('Prompt.txt').read().format(context , question)

        llm = ChatCohere(cohere_api_key=cohere_api_key)
        message = [HumanMessage(content=prompt)]

        # except : return 'Could not send the query, please check your context length and the api key'

    return llm.invoke(message).content

def check_prompt(prompt) : 
    '''
    Function to check the prompt

    Args :
        1) prompt : str : prompt to check

    Returns :
        1) bool : True if prompt is valid else False
    '''

    try : 
        prompt.replace('' , '')
        return True 
    except : return False


def check_mesaage() : 
    '''
    Function to check the messages
    '''

    if 'messages' not in st.session_state : st.session_state.messages = []

check_mesaage()

for message in st.session_state.messages : 

    with st.chat_message(message['role']) : st.markdown(message['content'])

prompt = st.chat_input('Ask me anything')

if check_prompt(prompt) :

    with st.chat_message('user') : st.markdown(prompt)

    st.session_state.messages.append({
        'role' : 'user' , 
        'content' : prompt
    })

    if prompt != None or prompt != '' : 

        response = get_answer(prompt)

        with st.chat_message('assistant') : st.markdown(response)


        st.session_state.messages.append({
            'role' : 'assistant' , 
            'content' : response
        })
