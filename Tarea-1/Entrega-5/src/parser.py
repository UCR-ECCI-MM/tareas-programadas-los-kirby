# ------------------------------------------------------------------------------
# parser.py
#
# Daniel Gómez Solís
# María Fernanda Herrera Gutiérrez
# Grupo: los kirbys

# Syntactical analyzer for XML medical data
# ------------------------------------------------------------------------------

import ply.yacc as yacc
from lexer import tokens, build_lexer

# ------------------------------------------------------------------------------
# Data structures

# List to store total topics, date and time of generation of XML
health_TOPICS_DATA_GENERATION_XLL = []       

# Dictionary to store description, title, url, id, language and date of a health topic
# It stores all the elements of a health topic (also_called, full_summary, group, language_mapped_topic
# , descriptor, other_language, primary_institute, related_topic, see_reference, site)
diccionary_health_content = {}

# ------------------------------------------------------------------------------
# Parsing rules

# Define different rules for the parser
def p_health_topics(p):
    '''health_topics : OPEN_HEALTH_TOPICS TOPICS_TOTAL DATA_GENERATION DATE_GENERATED TIME_GENERATED health_topic_contents CLOSE_HEALTH_TOPICS
                     |'''
    if (len(p) > 1):
        total_topics = str(p[2])
        date = str(p[4])
        time = str(p[5])
        # Add to list
        global health_TOPICS_DATA_GENERATION_XLL
        health_TOPICS_DATA_GENERATION_XLL = [total_topics, date, time]
        # Save data set info to file
        save_data_set_info(health_TOPICS_DATA_GENERATION_XLL)
        
def p_health_topic_contents(p):
    '''health_topic_contents : OPEN_HEALTH_TOPIC HT_DESCRIPTION TITLE URL ID LANGUAGE DATE elements CLOSE_HEALTH_TOPIC health_topic_contents
                             |'''
    if (len(p) > 1):
        description = p[2]
        title = p[3]
        url = p[4]
        id = p[5]
        language = p[6]
        date = p[7]
        elements = p[8]
        # If the id is already in the dictionary, append the new content
        if id in diccionary_health_content:
            diccionary_health_content[id].append((description, title, url, id, language, date, elements))
        # If the id is not in the dictionary, create a new entry
        else:
            diccionary_health_content[id] = [(description, title, url, id, language, date, elements)]
        save_to_txt(diccionary_health_content)

def p_elements(p):
    '''elements : also_called_content full_summary_content group_content language_mapped_topic_content descriptor_content other_language_content primary_institute_content related_topic_content see_reference_content site_content'''
    if len(p) > 1:
        p[0] = {}  # Dictionary to store elements of a health topic
        
        # Add also_called content if it exists
        if p[1]:
            p[0]['also_called'] = p[1]
        
        # Add full_summary content if it exists
        if p[2]:
            p[0]['full_summary'] = p[2]

        # Add group content if it exists
        if p[3]:
            p[0]['group'] = p[3]

        # Add language_mapped_topic content if it exists
        if p[4]:
            p[0]['language_mapped_topic'] = p[4]

        # Add descriptor content if it exists
        if p[5]:
            p[0]['descriptor'] = p[5]

        # Add other_language content if it exists
        if p[6]:
            p[0]['other_language'] = p[6]

        # Add primary_institute content if it exists
        if p[7]:
            p[0]['primary_institute'] = p[7]    

        # Add related_topic content if it exists
        if p[8]:
            p[0]['related_topic'] = p[8]

        # Add see_reference content if it exists
        if p[9]:
            p[0]['see_reference'] = p[9]

        # Add site content if it exists
        if p[10]:
            p[0]['site'] = p[10]

def p_also_called_content(p):
    '''also_called_content : OPEN_ALSO_CALLED TEXT CLOSE_ALSO_CALLED also_called_content
                           |'''
    if len(p) > 1:
        if p[4] is not None:
            p[0] = [p[2]] + p[4]  # Add current content to the list
        else:
            p[0] = [p[2]]  # Create a new list with the current content
    else:
        p[0] = []  # List to store also_called content
    
def p_full_summary_content(p):
    '''full_summary_content : OPEN_FULL_SUMMARY tags CLOSE_FULL_SUMMARY full_summary_content
                            |'''
    if len(p) > 1:
        if p[4] is not None and p[2] is not None:
            p[0] = [p[2]] + [" "] + p[4]  # Save current content and add to the list
        elif p[2] is not None:
            p[0] = [p[2]]  # Save current content
    else:
        p[0] = []  # Empty list to store full_summary content

def p_tags(p):
    '''tags : XML_H tags
            | XML_LI tags
            | XML_UL tags
            | XML_P tags
            | XML_STRONG tags
            | OPEN_XML_A HREF tags CLOSE_XML_A tags
            | OPEN_XML_A HREF TID tags CLOSE_XML_A tags 
            | XML_TAG tags
            | TEXT tags
            |'''
    
    length = len(p)

    if length == 3:
        if p[2] != None:
            p[0] = " " + p[1] + p[2]
    elif length == 6:
        p[0] = p[2]
        if p[5] != None:
            p[0] = " " + p[2] + " " + p[3] + p[5]
        else:
            p[0] = " " + p[2] + " " + p[3]
    elif length == 7:
        if p[6] != None:
            p[0] = " " + p[2] + " " + p[4]  + p[6]
        else:
            p[0] = " " + p[2] + p[4]
    else:
        p[0] = " "

def p_group_content(p):
    '''group_content : OPEN_GROUP URL ID TEXT CLOSE_GROUP group_content
                     |'''
    length = len(p)

    if length == 1:
        p[0] = []
    else:
        group_data = {'url': p[2], 'id': p[3], 'text': p[4]}
        p[6].append(group_data)
        p[0] = p[6]

def p_language_mapped_topic_content(p):
    '''language_mapped_topic_content : OPEN_LANGUAGE_MAPPED_TOPIC URL ID LANGUAGE TEXT CLOSE_LANGUAGE_MAPPED_TOPIC language_mapped_topic_content
                                     |'''
    length = len(p)

    if length == 1:
        p[0] = []
    else:
        language_mapped_data = {'url': p[2], 'id': p[3], 'language': p[4], 'text': p[5]}
        p[7].append(language_mapped_data)
        p[0] = p[7]
    
def p_descriptor_content(p):
    '''descriptor_content : OPEN_DESCRIPTOR ID TEXT CLOSE_DESCRIPTOR qualifier_content descriptor_content
                          |'''
    length = len(p)

    if length == 1:
        p[0] = []
    else:
        descriptor_data = {'id': p[2], 'text': p[3]}
        p[6].append(descriptor_data)
        p[0] = p[6]

def p_qualifier_content(p):
    '''qualifier_content : OPEN_QUALIFIER ID TEXT CLOSE_QUALIFIER qualifier_content
                         |'''
    # No vamos a utilizarlo, entonces no hace falta.
    # if len(p) > 1:
    #     p[0] = {'id': p[2], 'text': p[3]}  # Store in dictionary

def p_other_language_content(p):
    '''other_language_content : OPEN_OTHER_LANGUAGE VERNACULAR_NAME URL TEXT CLOSE_OTHER_LANGUAGE other_language_content
                              |'''
    length = len(p)

    if length == 1:
        p[0] = []
    else:
        other_language_data = {'vernacular_name': p[2], 'url': p[3], 'text': p[4]}
        p[6].append(other_language_data)
        p[0] = p[6]

def p_primary_institute_content(p):
    '''primary_institute_content : OPEN_PRIMARY_INSTITUTE URL TEXT CLOSE_PRIMARY_INSTITUTE primary_institute_content
                                 |'''
    length = len(p)

    if length == 1:
        p[0] = []
    else:
        other_language_data = {'url': p[2], 'text': p[3]}
        p[5].append(other_language_data)
        p[0] = p[5]

def p_related_topic_content(p):
    '''related_topic_content : OPEN_RELATED_TOPIC URL ID TEXT CLOSE_RELATED_TOPIC related_topic_content
                             |'''
    if len(p) > 1:
        # If there is previous content, append the current content
        if p[6] is not None:
            # If there is previous content, append the current content
            p[0] = p[6]
            p[0].append({'url': p[2], 'id': p[3], 'text': p[4]})
        else:
            # If there is no previous content, start with the current content
            p[0] = [{'url': p[2], 'id': p[3], 'text': p[4]}]
    else:
        p[0] = []  # Aux list to store related_topic content

def p_see_reference_content(p):
    '''see_reference_content : OPEN_SEE_REFERENCE TEXT CLOSE_SEE_REFERENCE see_reference_content
                             |'''
    if len(p) > 1:
        if p[4] is not None:
            p[0] = [p[2]] + p[4]  # Add current content to the list
        else:
            p[0] = [p[2]]  # Create a new list with the current content
    else:
        p[0] = []  # List to store see_reference content

def p_site_content(p):
    '''site_content : OPEN_SITE TITLE URL LANGUAGE_SITE_URL information_content organization_content standard_content CLOSE_SITE site_content
                    | OPEN_SITE TITLE URL information_content organization_content standard_content CLOSE_SITE site_content
                    |'''
    length = len(p)
    if length == 1:
        p[0] = []
    else:
        site_data = {}
        if length == 10:
            site_data = {
                'title': p[2],
                'url': p[3],
                'language_site_url': p[4] if p[4] is not None else None,
                'information_content': p[5] if p[5] is not None else None,
                'organization_content': p[6] if p[6] is not None else None,
                'standard_content': p[7] if p[7] is not None else None
            }
            p[9].append(site_data)
            p[0] = p[9]
        elif length == 9:
            site_data = {
                'title': p[2],
                'url': p[3],
                'information_content': p[4] if p[4] is not None else None,
                'organization_content': p[5] if p[5] is not None else None,
                'standard_content': p[6] if p[6] is not None else None
            }
            p[8].append(site_data)
            p[0] = p[8]

def p_information_content(p):
    '''information_content : OPEN_INFORMATION_CATEGORY TEXT CLOSE_INFORMATION_CATEGORY information_content
                           |'''
    if len(p) > 1:
        if p[4] is not None:
            p[0] = [p[2]] + p[4]  # Add current content to the list
        else:
            p[0] = [p[2]]  # Create a new list with the current content
    else:
        p[0] = []  # List to store information_category content
    
def p_organization_content(p):
    '''organization_content : OPEN_ORGANIZATION TEXT CLOSE_ORGANIZATION organization_content
                            |'''
    if len(p) > 1:
        if p[4] is not None:
            p[0] = [p[2]] + p[4]  # Add current content to the list
        else:
            p[0] = [p[2]]  # Create a new list with the current content
    else:
        p[0] = []  # List to store organization content
    
def p_standard_content(p):
    '''standard_content : OPEN_STANDARD_DESCRIPTION TEXT CLOSE_STANDARD_DESCRIPTION standard_content
                        |'''
    if len(p) > 1:
        if p[4] is not None:
            p[0] = [p[2]] + p[4]  # Add current content to the list
        else:
            p[0] = [p[2]]  # Create a new list with the current content
    else:
        p[0] = []  # List to store standard_description content
    
# Define rule for error handling
def p_error(t):
    if t:
        print(f"Syntax error at '{t.value}'")
        parser.errok()  # Continue parsing
    else:
        print("Syntax error at EOF")

# Build parser
def build_parser():
    return yacc.yacc()

# ------------------------------------------------------------------------------
# Auxiliar functions

# Save data set info to file
def save_data_set_info(health_TOPICS_DATA_GENERATION_XLL):
    with open("health_topics.txt", "a") as file:
        total_topics, date, time = health_TOPICS_DATA_GENERATION_XLL
        file.write(f"Total Topics: {total_topics}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Time: {time}\n")
        file.write("\n")

# Store parsed data to a file
def save_to_txt(dic):
    with open("health_topics.txt", "w") as file:
        for id, entries in dic.items():
            file.write(f"Topic ID: {id}\n")
            for entry in entries:
                title, description, url, id, language, date, elements = entry
                file.write(f"Title: {title}\n")
                file.write(f"Description: {description}\n")
                file.write(f"URL: {url}\n")
                file.write(f"Language: {language}\n")
                file.write(f"Date: {date}\n")

                # Write the elements in a readable format
                file.write("Elements:\n")
                for key, value in elements.items():
                    if isinstance(value, list):
                        # Convert all items to strings before joining
                        value_str = [str(v) for v in value]  # Convert each item to str
                        file.write(f"  {key.capitalize()}: {', '.join(value_str)}\n")
                    else:
                        file.write(f"  {key.capitalize()}: {value}\n")
                file.write("\n")  # Add a new line to separate entries
