import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import tempfile

load_dotenv()
# Tämä tulostaa terminaaliin avaimen 5 ensimmäistä merkkiä varmistukseksi
print(f"DEBUG: Avain alkaa: {os.getenv('OPENAI_API_KEY')[:10]}...")

# 1. Alustus
#load_dotenv()

st.set_page_config(page_title="AI Document Advisor", page_icon="")
st.title("AI Document Advisor")
st.markdown("Lataa PDF-tiedosto ja kysy siltä mitä vain.")

# Alustetaan chatti-historia Streamlitin muistiin (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Sivupalkki tiedoston latausta varten
with st.sidebar:
    st.header("Lataus")
    uploaded_file = st.file_uploader("Valitse PDF-tiedosto", type="pdf")

# 3. RAG-logiikka: Prosessoidaan tiedosto kun se ladataan
@st.cache_resource # Cache estää tiedoston uudelleenlatauksen jokaisella klikkauksella
def setup_rag(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Moderni "Chain" (LCEL)
    template = """Vastaa kysymykseen vain annetun kontekstin perusteella:
    {context}
    
    Kysymys: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    # Tämä on "moottori", joka hakee tiedon ja generoi vastauksen
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

# 4. Chattikäyttöliittymä
if uploaded_file:
    with st.spinner("Analysoidaan dokumenttia..."):
        qa_chain = setup_rag(uploaded_file)
    st.success("Dokumentti valmis! Voit nyt esittää kysymyksiä.")

    # Näytetään aiemmat viestit
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Käyttäjän uusi kysymys
    if prompt := st.chat_input("Mitä haluat tietää dokumentista?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        #with st.chat_message("assistant"):
            # TÄSSÄ TAPAHTUU RAG:
            # 1. Kysymys lähetetään ketjulle
            # 2. Chroma etsii osuvat tekstipalat
            # 3. GPT vastaa palojen perusteella
        with st.chat_message("assistant"):
            # Uusi tapa palauttaa vastaus suoraan merkkijonona
            full_response = qa_chain.invoke(prompt)
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.info("Lataa PDF-tiedosto sivupalkista aloittaaksesi.")