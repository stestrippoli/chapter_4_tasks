from PyPDF2 import PdfReader
import re


def pdf_to_text(filename):
    reader = PdfReader(filename)
    full_text = ""
    for page in reader.pages:
# extracting text from page
        text = page.extract_text()
        full_text+=(text)
    return full_text
# modulare funzioni

def py_to_text(filename):
    full_text = ""
    with open(filename, "r") as f:
        for line in f:
    # extracting text from page
            if not line.startswith('#'):
             full_text+=(line)
    return full_text
def rs_to_text(filename):
    full_text = ""
    with open(filename, "r") as f:
        for line in f:
    # extracting text from page
            full_text+=(line)
    return full_text

def txt_to_text(filename):
    full_text = ""
    with open(filename, "r") as f:
        for line in f:
    # extracting text from page
             full_text+=(line)
    return full_text


def save(full_text, filename):
    with open(f"{filename}_cleaned.txt", "w") as f:
        f.write(full_text)


def clean_summarization(input_text):
    regex = r".*?(?:[1-7]/7)"

    output_text = re.sub(regex, "", input_text, flags=re.DOTALL)
    output_text = re.sub(".\\\\.", "'", output_text, flags=re.DOTALL)
    output_text = output_text.strip()
    output_text = re.sub(r"\s+", " ", output_text, flags=re.DOTALL)
    output_text = re.sub("km/'h", "km/h", output_text, flags=re.DOTALL)

    return output_text

def clean_qa(input_text):
    regex = "1 Documento reso disponibile da AIFA il 23/07/2022Esula dalla competenza dell�AIFA ogni eventuale disputa concernente i diritti di propriet� industriale e la tutela brevettuale dei dati relativi all�AIC dei medicinali e, pertanto, l�Agenzia non pu� essere ritenuta responsabile in alcun modo di eventuali violazioni da parte del titolare dell'autorizzazione all'immissione in commercio (o titolare AIC)."
    n = len(regex)
    output_text = input_text[:len(input_text) - len(regex)]
    output_text = re.sub("\\n", " ", output_text, flags=re.DOTALL)
    return output_text

