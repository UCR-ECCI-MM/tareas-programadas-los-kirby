import ply.lex as lex
from pathlib import Path
import re
# import the yacc module for syntax parsing
import ply.yacc as yacc

# ------------------------------------------------------------------------------
# Analizador_Parser.py
#
# Daniel Gómez Solís
# María Fernanda Herrera Gutiérrez
# Grupo: los kirbys

# Tokenizer for XML medical data
# Syntactical analyzer for XML medical data
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# LEXER CODE

# List of tokens
tokens = (
    'OPEN_HEALTH_TOPICS',               # Open tag <health-topics>
    'TOPICS_TOTAL',                     # Total number of topics
    'DATA_GENERATION',                  # Data of date and time of generation
    'DATE_GENERATED',                   # Date of generation
    'TIME_GENERATED',                   # Time of generation
    'CLOSE_HEALTH_TOPICS',              # Close tag </health-topicS>

    'OPEN_HEALTH_TOPIC',                # Open tag <health-topic>
    'HT_DESCRIPTION',                   # Description of health topic

    'TITLE',                            # Title of health topic
    'URL',                              # URL of health topic
    'ID',                               # ID of health topic
    'LANGUAGE',                         # Language of health topic
    'DATE',                             # Date of health topic
    'CLOSE_HEALTH_TOPIC',               # Close tag </health-topic>

    'OPEN_ALSO_CALLED',                 # Open tag <also-called>
    'CLOSE_ALSO_CALLED',                # Close tag </also-called>

    'OPEN_FULL_SUMMARY',                # Open tag <full-summary>
    'CLOSE_FULL_SUMMARY',               # Close tag </full-summary>

    'OPEN_LANGUAGE_MAPPED_TOPIC',       # Open tag <language-mapped-topic>
    'CLOSE_LANGUAGE_MAPPED_TOPIC',      # Close tag </language-mapped-topic>

    'OPEN_DESCRIPTOR',                  # Open tag <descriptor>
    'CLOSE_DESCRIPTOR',                 # Close tag </descriptor>

    'OPEN_GROUP',                       # Open tag <group>
    'CLOSE_GROUP',                      # Close tag </group>

    'OPEN_OTHER_LANGUAGE',              # Open tag <other-language>
    'VERNACULAR_NAME',                  # Vernacular language name   
    'CLOSE_OTHER_LANGUAGE',             # Close tag </other-language>

    'OPEN_RELATED_TOPIC',               # Open tag <related-topic>
    'CLOSE_RELATED_TOPIC',              # Close tag </related-topic>

    'OPEN_PRIMARY_INSTITUTE',           # Open tag <primary-institute>
    'CLOSE_PRIMARY_INSTITUTE',          # Close tag </primary-institute>

    'OPEN_SEE_REFERENCE',               # Open tag <see-reference>
    'CLOSE_SEE_REFERENCE',              # Close tag </see-reference>

    'OPEN_SITE',                        # Open tag <site>
    'LANGUAGE_SITE_URL',                # Language site URL
    'CLOSE_SITE',                       # Close tag </site>

    'OPEN_INFORMATION_CATEGORY',        # Open tag <information-category>
    'CLOSE_INFORMATION_CATEGORY',       # Close tag </information-category>

    'OPEN_ORGANIZATION',                # Open tag <organization>
    'CLOSE_ORGANIZATION',               # Close tag </organization>

    'OPEN_STANDARD_DESCRIPTION',        # Open tag <standard-description>
    'CLOSE_STANDARD_DESCRIPTION',       # Close tag </standard-description>

    'XML_H',                            # XML heading tags
    'XML_LI',                           # List item tags
    'XML_UL',                           # Unordered list tags
    'XML_P',                            # Paragraph tags
    'XML_A',                            # Anchor tags
    'XML_STRONG',                       # Strong tags
    'XML_TAG',                          # XML tags

    'TEXT'                              # Text content
)

# Regular expression rules for tokens
def t_OPEN_HEALTH_TOPICS(t):
    r'<health-topics'
    return t

def t_TOPICS_TOTAL(t):
    r'total="(\d+)"'
    t.value = int(t.value.split('=')[1].strip('"'))
    return t

def t_DATA_GENERATION(t):
    r'date-generated="'
    return t

def t_DATE_GENERATED(t):
    r'(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/(19|20)\d{2}'
    return t

def t_TIME_GENERATED(t):
    r'\d{2}:\d{2}:\d{2}"'
    # remove quotes
    t.value = t.value.strip('"')
    return t

def t_CLOSE_HEALTH_TOPICS(t):
    r'</health-topics>'
    return t

def t_OPEN_HEALTH_TOPIC(t):
    r'<health-topic'
    return t

def t_HT_DESCRIPTION(t):
    r'meta-desc="[^"]*"'
    t.value = t.value.split('=')[1].strip('"')
    return t

def t_TITLE(t):
    r'title="[^"]*"'
    t.value = t.value.split('=')[1].strip('"')
    return t

def t_URL(t):
    r'url="([a-z]+\:\/\/)?(www\.)?((\w|-)+\.[^ <>]+)"'
    t.value = t.value.split('=')[1].strip('"')
    return t

def t_ID(t):
    r'id="[^"]*"'
    t.value = t.value.split('=')[1].strip('"')
    return t

def t_LANGUAGE(t):
    r'language="[^"]*"'
    t.value = t.value.split('=')[1].strip('"')
    return t

def t_DATE(t):
    r'date-created="(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}"'
    t.value = t.value.split('=')[1].strip('"')
    return t

def t_CLOSE_HEALTH_TOPIC(t):
    r'</health-topic>'
    return t

def t_OPEN_ALSO_CALLED(t):
    r'<also-called>'
    return t

def t_CLOSE_ALSO_CALLED(t):
    r'</also-called>'
    return t

def t_OPEN_FULL_SUMMARY(t):
    r'<full-summary>'
    return t

def t_CLOSE_FULL_SUMMARY(t):
    r'</full-summary>'
    return t

def t_OPEN_LANGUAGE_MAPPED_TOPIC(t):
    r'<language-mapped-topic'
    return t

def t_CLOSE_LANGUAGE_MAPPED_TOPIC(t):
    r'</language-mapped-topic>'
    return t

def t_OPEN_DESCRIPTOR(t):
    r'<descriptor'
    return t

def t_CLOSE_DESCRIPTOR(t):
    r'</descriptor>'
    return t

def t_OPEN_GROUP(t):
    r'<group'
    return t

def t_CLOSE_GROUP(t):
    r'</group>'
    return t

def t_OPEN_OTHER_LANGUAGE(t):
    r'<other-language'
    return t

def t_VERNACULAR_NAME(t):
    r'vernacular-name="[^"]*"'
    t.value = t.value.split('=')[1].strip('"')
    return t

def t_CLOSE_OTHER_LANGUAGE(t):
    r'</other-language>'
    return t

def t_OPEN_RELATED_TOPIC(t):
    r'<related-topic'
    return t

def t_CLOSE_RELATED_TOPIC(t):
    r'</related-topic>'
    return t

def t_OPEN_PRIMARY_INSTITUTE(t):
    r'<primary-institute'
    return t

def t_CLOSE_PRIMARY_INSTITUTE(t):
    r'</primary-institute>'
    return t

def t_OPEN_SEE_REFERENCE(t):
    r'<see-reference>'
    return t

def t_CLOSE_SEE_REFERENCE(t):
    r'</see-reference>'
    return t

def t_OPEN_SITE(t):
    r'<site'
    return t

def t_LANGUAGE_SITE_URL(t):
    r'language-mapped-url="([a-z]+\:\/\/)?(www\.)?((\w|-)+\.[^ <>]+)"'
    t.value = t.value.split('=')[1].strip('"')
    return t

def t_CLOSE_SITE(t):
    r'</site>'
    return t

def t_OPEN_INFORMATION_CATEGORY(t):
    r'<information-category>'
    return t

def t_CLOSE_INFORMATION_CATEGORY(t):
    r'</information-category>'
    return t

def t_OPEN_ORGANIZATION(t):
    r'<organization>'
    return t

def t_CLOSE_ORGANIZATION(t):
    r'</organization>'
    return t

def t_OPEN_STANDARD_DESCRIPTION(t):
    r'<standard-description>'
    return t

def t_CLOSE_STANDARD_DESCRIPTION(t):
    r'</standard-description>'
    return t

def t_XML_H(t):
    r'</?h[2-6]>'
    return t

def t_XML_LI(t):
    r'</?li>'
    return t

def t_XML_UL(t):
    r'</?ul>'
    return t

def t_XML_P(t):
    r'</?p>'
    return t

def t_XML_A(t):
    r'</?a\s+href="[^"]*">'
    return t

def t_XML_STRONG(t):
    r'</?strong>'
    return t

def t_XML_TAG(t):
    r'\<[^>]+\>'
    return t

def t_TEXT(t):
    r'[^\<]+'
    t.value = t.value.replace('\n', ' ').replace('\r', ' ').strip() # remove new lines
    t.value = t.value.replace('>', ' ').replace('\r', ' ').strip() # remove useless '>' characters
    t.value = re.sub(r'\s+', ' ', t.value).strip() # remove extra spaces
    if not t.value: # ignore empty strings
        return None
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}, position {t.lexpos}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# ------------------------------------------------------------------------------
# PARSER CODE

# Parsing rules

# Structures for future use
structure = {} # Not yet needed

# Define different rules for the parser

# Example of a rule
def p_health_topics(p):
    '''health_topics : OPEN_HEALTH_TOPICS TOPICS_TOTAL DATA_GENERATION DATE_GENERATED TIME_GENERATED health_topic_contents CLOSE_HEALTH_TOPICS
        |'''
    # p[0] = p[6]
    if (len(p) > 1):
        health_topics_string = str(p[2])+ " " + p[4] + " " + p[5]
        print(health_topics_string)
        
    print("Health topics parsed")

def p_health_topic_contents(p):
    '''health_topic_contents : OPEN_HEALTH_TOPIC HT_DESCRIPTION TITLE URL ID LANGUAGE DATE elements CLOSE_HEALTH_TOPIC health_topic_contents
        |'''
    if (len(p) > 1):
        health_topic_string =  p[2] + " " + p[3] + " " + str(p[4]) + " " + p[5] + " " + p[6] + " " + p[7]
        print(health_topic_string)
    print ("Health topic contents parsed")

def p_elements(p):
    '''elements : also_called_content full_summary_content group_content language_mapped_topic_content descriptor_content other_language_content primary_institute_content related_topic_content see_reference_content site_content'''
    print("Elements parsed")

def p_also_called_content(p):
    '''also_called_content : OPEN_ALSO_CALLED TEXT CLOSE_ALSO_CALLED also_called_content
        |'''
    if (len(p) > 1):
        print(p[2])
    print("Also called content parsed")

def p_full_summary_content(p):
    '''full_summary_content : OPEN_FULL_SUMMARY TEXT CLOSE_FULL_SUMMARY full_summary_content
        |'''
    if (len(p) > 1):
        print(p[2])
    print("Full summary content parsed")

# Define rule for error handling
def p_error(t):
    print("Syntax error at '%s'" % t.value)

# Build the parser
parser = yacc.yacc()

# Define a rule to read data from file
def read_data():
    file_name = Path(__file__).parent / "test.xml"
    with open(file_name, 'r') as file:
        data = file.read()
    return data

# Read data from file
data = read_data()

# Parse data
parser.parse(data)

# Print parser results

# ------------------------------------------------------------------------------
# Tokenize
# def run_lexer(data):
#     lexer.input(data)
#     path = Path("tokens.txt")
#     with path.open("w") as file:
#         while True:
#             tok = lexer.token()
#             if not tok:
#                 break
#             file.write(f"{tok.type} {tok.value}\n")

# data = read_data()
# run_lexer(data)