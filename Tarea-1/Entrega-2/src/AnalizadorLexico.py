# ------------------------------------------------------------------------------
# AnalizadorLexico.py
#
# Daniel Gómez Solís
# María Fernanda Herrera Gutiérrez
# Grupo: los kirbys

# Tokenizer for XML medical data
# ------------------------------------------------------------------------------

import ply.lex as lex
from pathlib import Path # to get the path of the file
import re # delete extra spaces

# List of tokens
tokens = (
    'OPEN_HEALTH_TOPIC',                # topic introduction
    'CLOSE_HEALTH_TOPIC',               # <\health-topic>

    'OPEN_HEALTH_TOPICS',               # amount of topics and date
    'CLOSE_HEALTH_TOPICS',              # <\health-topics>

    'OPEN_FULL_SUMMARY',                # summary of topic
    'CLOSE_FULL_SUMMARY',               # <\full-summary>

    'OPEN_PRIMARY_INSTITUTE',           # url of organizations
    'CLOSE_PRIMARY_INSTITUTE',          # <\primary-institute>

    'OPEN_GROUP',                       # related articles for topic
    'CLOSE_GROUP',                      # <\group>

    'OPEN_LANGUAGE_MAPPED_TOPIC',       # shows articles in other languages
    'CLOSE_LANGUAGE_MAPPED_TOPIC',      # <\language-mapped-topic>

    'OPEN_DESCRIPTOR',                  # ID of topic   
    'CLOSE_DESCRIPTOR',                 # <\descriptor>

    'OPEN_OTHER_LANGUAGE',              # ? (we don't understand this tag atm
                                        # , but we think it's useful)
    'CLOSE_OTHER_LANGUAGE',             # <\other-language>

    'OPEN_SEE_REFERENCE',               # ?
    'CLOSE_SEE_REFERENCE',              # <\see-reference>

    'OPEN_SITE',                        # topic article
    'CLOSE_SITE',                       # <\site>

    'OPEN_INFORMATION_CATEGORY',        # ?
    'CLOSE_INFORMATION_CATEGORY',       # <\information-category>

    'OPEN_ORGANIZATION',                # name of organization
    'CLOSE_ORGANIZATION',               # <\organization>

    'OPEN_STANDARD_DESCRIPTION',        # ?
    'CLOSE_STANDARD_DESCRIPTION',       # <\standard-description>

    'OPEN_ALSO_CALLED',                 # other names for topic
    'CLOSE_ALSO_CALLED',                # <\also-called>

    'OPEN_RELATED_TOPIC',               # related topics
    'CLOSE_RELATED_TOPIC',              # <\related-topic>

    'OPEN_HREF',                        # XML tag <a href> url
    'CLOSE_HREF',                       # </a href>

    'TEXT',                             # text inside XML tags 
    'XMLTAG'                            # different XML tags
)

# ------------------------------------------------------------------------------

# Regular expression rules for tokens

def t_OPEN_HEALTH_TOPIC(t):
    r'<health-topic[^>]*>' # regular expression
    # remove newlines and carriage returns
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    # remove extra spaces
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_HEALTH_TOPIC = r'\<\/health-topic\>'

def t_OPEN_HEALTH_TOPICS(t):
    r'\<health-topics total="(\d+)" date-generated="(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})"\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_HEALTH_TOPICS = r'\<\/health-topics\>'

def t_OPEN_FULL_SUMMARY(t):
    r'\<full-summary\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_FULL_SUMMARY = r'\<\/full-summary\>'

def t_OPEN_PRIMARY_INSTITUTE(t):
    r'\<primary-institute url="([^"]+)"\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_PRIMARY_INSTITUTE = r'\<\/primary-institute\>'

def t_OPEN_GROUP(t):
    r'\<group url="([^"]+)" id="(\d+)"\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_GROUP = r'\<\/group\>'

def t_OPEN_LANGUAGE_MAPPED_TOPIC(t):
    r'\<language-mapped-topic url="([^"]+)" id="(\d+)" language="([^"]+)"\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_LANGUAGE_MAPPED_TOPIC = r'\<\/language-mapped-topic\>'

def t_OPEN_DESCRIPTOR(t):
    r'\<descriptor id="(\d+)"\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t
t_CLOSE_DESCRIPTOR = r'\<\/descriptor\>'

def t_OPEN_OTHER_LANGUAGE(t):
    r'\<other-language vernacular-name="([^"]+)" url="([^"]+)"\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t
t_CLOSE_OTHER_LANGUAGE = r'\<\/other-language\>'

def t_OPEN_SEE_REFERENCE(t):
    r'\<see-reference\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_SEE_REFERENCE = r'\<\/see-reference\>'

def t_OPEN_SITE(t):
    r'\<site title="([^"]+)" url="([^"]+)"(?: language-mapped-url="([^"]+)")?\s*/?\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_SITE = r'\<\/site\>'

def t_OPEN_INFORMATION_CATEGORY(t):
    r'\<information-category\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_INFORMATION_CATEGORY = r'\<\/information-category\>'

def t_OPEN_ORGANIZATION(t):
    r'\<organization\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_ORGANIZATION = r'\<\/organization\>'

def t_OPEN_STANDARD_DESCRIPTION(t):
    r'\<standard-description\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_STANDARD_DESCRIPTION = r'\<\/standard-description\>'

def t_OPEN_ALSO_CALLED(t):
    r'\<also-called\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_ALSO_CALLED = r'\<\/also-called\>'

def t_OPEN_RELATED_TOPIC(t):
    r'\<related-topic url="([^"]+)" id="(\d+)"\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_RELATED_TOPIC = r'\<\/related-topic\>'

def t_OPEN_HREF(t):
    r'\<a href="([^"]+)"\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

t_CLOSE_HREF = r'\<\/a\>'

def t_TEXT(t):
    r'[^\<]+'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    if not t.value: # ignore empty strings
        return None
    return t

def t_XMLTAG(t):
    r'\<[^>]+\>'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip()
    t.value = re.sub(r'\s+', ' ', t.value).strip()
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# ------------------------------------------------------------------------------

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}, position {t.lexpos}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Define a rule to read data from file
def read_data():
    file_name = Path(__file__).parent / "medical_data.xml"
    with open(file_name, 'r') as file:
        data = file.read()
    return data

# Read data from file
data = read_data()

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
