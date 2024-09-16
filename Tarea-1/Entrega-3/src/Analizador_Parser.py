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
    'TID',                              # TID of HREF
    'LANGUAGE',                         # Language of health topic
    'DATE',                             # Date of health topic
    'CLOSE_HEALTH_TOPIC',               # Close tag </health-topic>
    'HREF',

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

    'OPEN_QUALIFIER',                   # Open tag <qualifier
    'CLOSE_QUALIFIER',                  # CLose tag </qualifier>

    'XML_H',                            # XML heading tags
    'XML_LI',                           # List item tags
    'XML_UL',                           # Unordered list tags
    'XML_P',                            # Paragraph tags
    'OPEN_XML_A',                       # Anchor tag open
    'CLOSE_XML_A',                      # Anchor tag close
    'XML_STRONG',                       # Strong tags
    'XML_TAG',                          # XML tags
    'TEXT',                              # Text content
)

# Regular expression rules for tokens
def t_OPEN_HEALTH_TOPICS(t):
    r'<health-topics'
    return t

def t_TOPICS_TOTAL(t):
    r'total="(\d+)"'
    t.value = int(t.value.split('=', 1)[1].strip('"'))
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
    t.value = t.value.split('=', 1)[1].strip('"')
    return t

def t_TITLE(t):
    r'title="[^"]*"'
    t.value = t.value.split('=', 1)[1].strip('"')
    return t

def t_URL(t):
    r'url="([a-z]+\:\/\/)?(www\.)?((\w|-)+\.[^ <>]+)(\#[^\<]+)?"'
    t.value = t.value.split('=', 1)[1].strip('"')
    return t

def t_ID(t):
    r'id="[^"]*"'
    t.value = t.value.split('=', 1)[1].strip('"')
    return t

def t_TID(t):
    r'tid="[^"]*"'
    t.value = t.value.split('=', 1)[1].strip('"')
    return t

def t_LANGUAGE(t):
    r'language="[^"]*"'
    t.value = t.value.split('=', 1)[1].strip('"')
    return t

def t_DATE(t):
    r'date-created="(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}"'
    t.value = t.value.split('=', 1)[1].strip('"')
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
    t.value = t.value.split('=', 1)[1].strip('"')
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
    t.value = t.value.split('=', 1)[1].strip('"')
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

def t_OPEN_QUALIFIER(t):
    r'<qualifier'
    return t

def t_CLOSE_QUALIFIER(t):
    r'</qualifier>'
    return t

def t_XML_H(t):
    r'</?h[2-6]>'
    pass

def t_XML_LI(t):
    r'</?li>'
    pass

def t_XML_UL(t):
    r'</?ul>'
    pass

def t_XML_P(t):
    r'</?p>'
    pass

def t_OPEN_XML_A(t):
    r'<a'
    return t

def t_HREF(t):
    r'href="[^"]*"'
    # Divide en '=', toma la parte derecha y elimina comillas
    t.value = t.value.split('=', 1)[1].strip('"')
    return t

def t_CLOSE_XML_A(t):
    r'</a>'
    return t

def t_XML_STRONG(t):
    r'</?strong>'
    pass

def t_XML_TAG(t):
    r'\<[^>]+\>'
    return

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

def p_health_topics(p):
    '''health_topics : OPEN_HEALTH_TOPICS TOPICS_TOTAL DATA_GENERATION DATE_GENERATED TIME_GENERATED health_topic_contents CLOSE_HEALTH_TOPICS
        |'''

        
def p_health_topic_contents(p):
    '''health_topic_contents : OPEN_HEALTH_TOPIC HT_DESCRIPTION TITLE URL ID LANGUAGE DATE elements CLOSE_HEALTH_TOPIC health_topic_contents
        |'''


def p_elements(p):
    '''elements : also_called_content full_summary_content group_content language_mapped_topic_content descriptor_content other_language_content primary_institute_content related_topic_content see_reference_content site_content'''

def p_also_called_content(p):
    '''also_called_content : OPEN_ALSO_CALLED TEXT CLOSE_ALSO_CALLED also_called_content
        |'''
    if (len(p) > 1):
        write_to_file(p[2])

def p_full_summary_content(p):
    '''full_summary_content : OPEN_FULL_SUMMARY tags CLOSE_FULL_SUMMARY full_summary_content
        |'''

def p_tags(p):
    '''tags : XML_H tags XML_H tags
        | XML_LI tags XML_LI tags
        | XML_UL tags XML_UL tags
        | XML_P tags XML_P tags
        | XML_STRONG tags XML_STRONG tags
        | OPEN_XML_A HREF tags CLOSE_XML_A tags
        | OPEN_XML_A HREF TID tags CLOSE_XML_A tags
        | XML_TAG tags XML_TAG tags
        | TEXT tags
        |'''


def p_group_content(p):
    '''group_content : OPEN_GROUP URL ID TEXT CLOSE_GROUP group_content
        |'''


def p_language_mapped_topic_content(p):
    '''language_mapped_topic_content : OPEN_LANGUAGE_MAPPED_TOPIC URL ID LANGUAGE TEXT CLOSE_LANGUAGE_MAPPED_TOPIC language_mapped_topic_content
        |'''


def p_descriptor_content(p):
    '''descriptor_content : OPEN_DESCRIPTOR ID TEXT CLOSE_DESCRIPTOR qualifier_content descriptor_content
        |'''


def p_qualifier_content(p):
    '''qualifier_content : OPEN_QUALIFIER ID TEXT CLOSE_QUALIFIER qualifier_content
                        |'''


def p_other_language_content(p):
    '''other_language_content : OPEN_OTHER_LANGUAGE VERNACULAR_NAME URL TEXT CLOSE_OTHER_LANGUAGE other_language_content
        |'''


def p_primary_institute_content(p):
    '''primary_institute_content : OPEN_PRIMARY_INSTITUTE URL TEXT CLOSE_PRIMARY_INSTITUTE primary_institute_content
        |'''


def p_related_topic_content(p):
    '''related_topic_content : OPEN_RELATED_TOPIC URL ID TEXT CLOSE_RELATED_TOPIC related_topic_content
        |'''


def p_see_reference_content(p):
    '''see_reference_content : OPEN_SEE_REFERENCE TEXT CLOSE_SEE_REFERENCE see_reference_content
        |'''


def p_site_content(p):
    '''site_content : OPEN_SITE TITLE URL LANGUAGE_SITE_URL information_content organization_content standard_content CLOSE_SITE site_content
                    | OPEN_SITE TITLE URL information_content organization_content standard_content CLOSE_SITE site_content
                    |'''


def p_information_content(p):
    '''information_content : OPEN_INFORMATION_CATEGORY TEXT CLOSE_INFORMATION_CATEGORY information_content
                        |'''     

def p_organization_content(p):
    '''organization_content : OPEN_ORGANIZATION TEXT CLOSE_ORGANIZATION organization_content
                        |'''

def p_standard_content(p):
    '''standard_content : OPEN_STANDARD_DESCRIPTION TEXT CLOSE_STANDARD_DESCRIPTION standard_content
                    |'''

# Define rule for error handling
def p_error(t):
    if t:
        write_to_file(f"Syntax error at '{t.value}'")
        parser.errok()  # Borra el estado de error para intentar continuar
    else:
        write_to_file("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Define a rule to read data from file
def read_data():
    file_name = Path(__file__).parent / "medical_data.xml"
    with open(file_name, 'r') as file:
        data = file.read()
    return data

# Function to write results to file
def write_to_file(text):
    with open('parser_output.txt', 'a') as f:
        f.write(text + '\n')

# Read data from file
data = read_data()

# Parse data
parser.parse(data)

print("Parsing completed. Results written to parser_output.txt")