FROM python:3.9-slim

WORKDIR /app

# Asennetaan järjestelmäriippuvuudet (ChromaDB saattaa vaatia nollasta rakentamista)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit käyttää oletuksena porttia 8501
EXPOSE 8501

# Lisätään Streamlit-konfiguraatiota, jotta se toimii pilvessä ilman varoituksia
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]