# Imports
from bs4 import BeautifulSoup
from urllib.parse import unquote
import math
import os

# Classes

class Guide:
    def __init__(self, guide_name, file_content, stig_rule_dict):
        self.guide_name = guide_name
        self.file_content = file_content
        self.stig_rule_dict = stig_rule_dict

    def __str__(self) -> str:
        return f"{str(self.guide_name)} - {str(self.file_content)} - {str(self.stig_rule_dict)}"

class StigRule:
    def __init__(self, rule_name, rule_title, vuln_id, rule_id, rule_weight, rule_severity, stig_id, rule_fix_text, rule_description, check_content):
        self.rule_name = rule_name
        self.rule_title = rule_title
        self.vuln_id = vuln_id
        self.rule_id = rule_id
        self.rule_weight = rule_weight
        self.rule_severity = rule_severity
        self.stig_id = stig_id
        self.rule_fix_text = rule_fix_text
        self.rule_description = rule_description
        self.check_content = check_content
        self.category_score = self._calculateScore()
        # self.check_commands = self._getRequiredFields(self.check_content)
        # self.fix_commands = self._getRequiredFields(self.rule_fix_text)

    def _getRequiredFields(self, field):
        command_list = []
        
        field_split = field.split("\n")
        for field_line in field_split:
            field_text_to_fill = []
    
            if not field_line.startswith('Open "'):
                pass

            if not field_line.startswith('Enter "'):
                pass

            if not field_line.startswith('Enter "'):
                pass

            field_command = field_line.replace("$ ", "").strip()

            

            new_command = Command(field_command, field_text_to_fill)
            command_list.append(new_command)

        return command_list
  

    def _calculateScore(self):
        severity_Dictionary = {
            "critical": 5,
            "high": 4,
            "medium": 3,
            "low": 2,
            "no": 1,
        }

        severity_categories_dictionary = {
            "undefined": -1,
            "Very Low": 3,
            "Low": 5,
            "Medium": 10,
            "High": 13,
            "Very High": 17,
            "Extreme": float("inf"),
        }

        try:
            category_score = float(math.ceil(float(severity_Dictionary[self.rule_severity]) * (float(self.rule_weight)/2)))

            for category_name, category_score_limit in severity_categories_dictionary.items():
                if category_score <= category_score_limit:
                    severity_category = category_name
                    break
            self.category_score = severity_category
        except:
            self.category_score = "undefined"
    
        return self.category_score

    def __str__(self) -> str:
        return f"{str(self.rule_name)} - {str(self.rule_title)} - {str(self.vuln_id)} - {str(self.rule_id)} - {str(self.rule_weight)} - {str(self.rule_severity)} - {str(self.stig_id)} - {str(self.rule_fix_text)} - {str(self.rule_description)} - {str(self.check_content)} - {str(self.category_score)}"


def parseGuide(filename):
    # Defining Variables
    rule_dictionary = {}

    # Open XML File
    with open(filename, 'r', encoding='utf-8') as xml_file:
        xml_data = xml_file.read()
        content = BeautifulSoup(xml_data, 'xml')

    # Find all Group tags with the id attribute
    group_id_tags = content.find_all('Group', id=True)

    # Populate StigRule Object
    for group_id_tag in group_id_tags:

        # Extract Group ID
        group_id = group_id_tag['id']

        # Extract Group Information
        group_info = content.find('Group', id=group_id)
        
        # Extract Information under the parent Group tag
        rule_name = group_info.find('title').text
        vuln_id = group_id

        # Extract Rule Information
        group_rule_info = group_info.find('Rule')
        rule_id = group_rule_info['id']
        rule_weight = group_rule_info['weight']
        rule_severity = group_rule_info['severity']
        rule_title = group_rule_info.find('title').text
        stig_id = group_rule_info.find('version').text
        rule_fix_text = group_rule_info.find('fixtext').text
        # Extract Rule Description
        group_description_info = group_rule_info.find('description').text
        # URL Decode Rule Description
        group_description_info_decoded = unquote(group_description_info)
        # Transform back into XML
        group_description_info_xml = BeautifulSoup(group_description_info_decoded, 'xml')
        rule_description = group_description_info_xml.find('VulnDiscussion').text

        # Extract Check Information from Rule Information
        check_rule_info = group_rule_info.find('check')
        check_content = check_rule_info.find('check-content').text

        # Create Object
        rule = StigRule(rule_name, rule_title, vuln_id, rule_id, rule_weight, rule_severity, stig_id, rule_fix_text, rule_description, check_content)
        rule_dictionary[vuln_id] = rule
    
    # Create Guide Object
    guide = Guide(filename, group_id_tags, rule_dictionary)

    return guide


# Test replacement of commands from user input



# Test with no user input


guide = parseGuide("./script/testXmlFiles/U_MS_Windows_Server_2022_STIG_V1R3_Manual-xccdf.xml")

for rule in guide.stig_rule_dict:
    print(guide.stig_rule_dict[rule])
