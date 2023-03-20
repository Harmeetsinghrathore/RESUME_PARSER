import os, re
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
import pdfplumber
from nltk.corpus import stopwords

from . import constants as cs



# ____________EXTRACT TEXT FROM THE PDF FILE ________


def extract_text_from_pdf(file):
    # pdf_reader = PyPDF2.PdfReader(file)
    # file_text = pdf_reader.pages[0].extract_text()

    text = '' 
    with pdfplumber.open(file) as file:
        for page in file.pages:
            text += page.extract_text()

    return text

# _____________________ NAME __________________________

def extract_name(file_text):

    matcher = Matcher(nlp.vocab, validate=True)
    nlp_text = nlp(file_text)

    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern], on_match = None)

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text




# _____________________ PHONE NUMBER __________________


def extract_phone_number(file_text):

    number = ''
    PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
    phone = re.findall(PHONE_REG, file_text)
    if phone:
        number = ''.join(phone[0])
        if file_text.find(number) >= 0 and len(number) < 16:
            pass
        else:
            print('Error : Line 42 phone number')

    if number:
        return number
    else:
        return 'Null'


# _____________________ EMAIL __________________________


def extract_email(file_text):

    EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')

    email = re.findall(EMAIL_REG, file_text)

    if email:
        return email[0]
    else:
        return 'Null'



# _____________________ SKILLS __________________________

def extract_skills(pdf_path):

    doc = nlp(pdf_path)

    # Extract tokens and noun chunks
    tokens = [token.text for token in doc if not token.is_stop]
    noun_chunks = [chunk for chunk in doc.noun_chunks]

   
    data = pd.read_csv('apps/ResumeBuilder/db/skills.csv')
    skills = list(data.columns.values)
    skillset = []
    # Check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    # Check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    # Return a list of unique skills
    return [i.capitalize() for i in set([i.lower() for i in skillset])]





# _____________________ ENTITIES __________________________

def extract_entities(text):
    text_split = [i.strip() for i in text.split('\n')]
    entities = {}
    key = False
    p_key = ''
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            if phrase.lower().strip() in cs.RESUME_SECTIONS_GRAD:
                p_key = phrase.lower().strip()
        
        if p_key in cs.RESUME_SECTIONS_GRAD:
            entities[p_key.upper()] = []
            key = p_key
            p_key = ""
        elif key and phrase.strip():
            entities[key.upper()].append(phrase)
    return split_into_objects(entities)



def split_into_objects(entities):
    parameters = {}
    for key in list(entities.keys()):
        parameters[key] = []
        for phrase in entities[key]:
            if not set(phrase.lower().split()) & set(cs.INTERNSHIP_SECTIONS_GRAD) and len(parameters[key]) > 0:
                parameters[key][-1].append(phrase) 
            else:
                parameters[key].append([phrase])
    return parameters