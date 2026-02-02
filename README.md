https://doc-advisor-jans.azurewebsites.net/

# AI Document Advisor

Python-pohjainen RAG-sovellus (Retrieval-Augmented Generation), joka mahdollistaa keskustelun käyttäjän omien PDF-dokumenttien kanssa.

##  Kuvaus
Sovellus tarjoaa Streamlit-käyttöliittymän, johon käyttäjä voi ladata paikallisen `.pdf`-tiedoston ja keskustella sen sisällöstä tekoälyn avulla.  
Käyttäjää ei autentikoida, eikä dataa tai sessioita tallenneta sovelluksen sulkemisen jälkeen.

## Teknologiat
- Python  
- Streamlit (UI)
- LangChain (RAG-pipeline)
- OpenAI (GPT-4o-mini)
- ChromaDB (vektoritietokanta)
- Docker
- Azure (ACR & Web App)

##  Arkkitehtuuri
- PDF → tekstin paloitus → vektorointi
- Semanttinen haku (RAG)
- LLM-vastaukset dokumentin kontekstissa

##  Julkaisu
Sovellus on kontitettu Dockerilla ja julkaistu Azure-pilviympäristöön.  
Ympäristömuuttujat ja API-avaimet hallitaan turvallisesti.

##  Tietoturva
- Ei käyttäjätilejä
- Ei pysyvää tallennusta
- Sessio poistuu sovelluksen sulkeutuessa

# AI Document Advisor – RAG Application

Production-ready AI application for conversational document analysis.

##  Project Overview
AI Document Advisor is a Python-based Retrieval-Augmented Generation (RAG) application that enables users to chat with their own PDF documents via a web interface. The application is deployed live in Azure and designed with privacy-first principles.

##  Key Features
- Upload and analyze local PDF files
- Context-aware AI chat using document content
- No authentication, no persistent storage
- Session data is discarded on application close

##  Tech Stack
- **Backend:** Python, LangChain (LCEL)
- **LLM:** OpenAI GPT-4o-mini
- **Vector Store:** ChromaDB
- **Frontend:** Streamlit
- **Containerization:** Docker
- **Cloud:** Azure (Container Registry & Web Apps)

##  Architecture Highlights
- Document ingestion → text splitting → vector embedding
- Semantic search with Retrieval-Augmented Generation
- Modular, maintainable pipeline design

##  DevOps & Deployment
- Fully containerized with Docker
- CI-ready design with secure environment variable handling
- Deployed to Azure using ACR and Web Apps

##  Security & Privacy
- No user accounts or authentication
- No document or chat persistence
- API keys managed via environment variables

