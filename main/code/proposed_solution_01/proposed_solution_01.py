import requests
from bs4 import BeautifulSoup
import PyPDF2
import spacy
import re  # Expressões regulares

# --- 1. Coleta de Dados (exemplo simplificado) ---
def baixar_dou(data):  # Ex: data = "2024-03-15"
    url = f"https://www.in.gov.br/leiturajornal?data={data}&secao=do1"  # Ajustar para outras seções
    response = requests.get(url)
    response.raise_for_status()  # Verifica se houve erro na requisição

    soup = BeautifulSoup(response.text, 'html.parser')
    # Encontrar o link para o PDF (o layout do site pode mudar!)
    pdf_link = soup.find('a', {'href': re.compile(r'\.pdf$')})['href']

    pdf_response = requests.get(pdf_link)
    pdf_response.raise_for_status()

    with open(f"dou_{data}.pdf", "wb") as f:
        f.write(pdf_response.content)
    print(f"DOU {data} baixado.")

# --- 2. Conversão de PDF para Texto ---
def pdf_para_texto(pdf_path):
    texto = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            texto += page.extract_text()
    return texto

# --- 3. Pré-processamento (exemplo básico) ---
def pre_processar(texto):
    texto = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôûÂÊÎÔÛãõÃÕçÇ ]', '', texto)  # Remove caracteres especiais
    texto = texto.lower()
    texto = re.sub(r'\s+', ' ', texto).strip() # Normaliza espaços
    return texto

# --- 4. PLN (spaCy - Exemplo de NER) ---
def extrair_entidades(texto):
    nlp = spacy.load("pt_core_news_sm") # Carrega o modelo em português
    doc = nlp(texto)
    entidades = []
    for ent in doc.ents:
        entidades.append((ent.text, ent.label_))
    return entidades

# --- Exemplo de uso ---
data_dou = "2024-03-15"  # Exemplo de data
baixar_dou(data_dou)
texto_dou = pdf_para_texto(f"dou_{data_dou}.pdf")
texto_limpo = pre_processar(texto_dou)

# Exemplo simples para encontrar trechos que *parecem* ser editais:
for trecho in texto_limpo.split("."):  # Divisão *muito* simplificada!
  if "edital" in trecho or "licitacao" in trecho or "concorrencia" in trecho:
      print("Possível trecho relevante:")
      print(trecho)
      entidades = extrair_entidades(trecho) # Extrai entidades do trecho
      print("Entidades:", entidades)
      print("-" * 20)

# Para classificação e modelos mais avançados, você precisaria
# treinar seus próprios modelos ou usar modelos pré-treinados maiores.