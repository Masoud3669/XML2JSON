# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:59:45 2023

@author: Masoud
"""
from lxml import etree
import json
import xml.etree.ElementTree as ET

# Validate the XML document against the XSD schema
def validate_xml(xml_data, xsd_schema):
    
        xml_doc = etree.fromstring(xml_data)
        xsd_doc = etree.fromstring(xsd_schema) 
        xsd = etree.XMLSchema(xsd_doc)
    
        is_valid = xsd.validate(xml_doc)

        if is_valid:
            print("XML is valid according to XSD.")
        else:
            print("XML is NOT valid according to XSD.")
            print(xsd.error_log)
    


class XMLToJsonConverter:
    def __init__(self, xml_structure):
        self.xml_structure = xml_structure

    def convert_to_json(self):
        return json.dumps(self._convert_to_json_recursive(self.xml_structure), indent=3)

    def _convert_to_json_recursive(self, element):
        result = {}

        if 'tag' in element:
            result[element['tag']] = {}

            if 'attributes' in element:
                result[element['tag']]['attributes'] = element['attributes']

            if 'text' in element and element['text'] is not None:
                result[element['tag']]['text'] = element['text']

            if 'children' in element and element['children']:
                for child in element['children']:
                    result[element['tag']].update(self._convert_to_json_recursive(child))
            else:
                if 'text' in element and element['text'] is not None:
                    result[element['tag']] = element['text']
                else:
                    result[element['tag']] = None

        return result
#  Returns the XML structure 
def get_xml_structure(xml_string):
    root = ET.fromstring(xml_string)

    root_element = {
        'tag': root.tag,
        'attributes': root.attrib,
        'text': root.text,
        'children': []
    }

    for child in root:
        child_element = {
            'tag': child.tag,
            'attributes': child.attrib,
            'text': child.text,
            'children': []
        }
        for sub_child in child:
            sub_child_element = {
                'tag': sub_child.tag,
                'attributes': sub_child.attrib,
                'text': sub_child.text
            }
            child_element['children'].append(sub_child_element)

        root_element['children'].append(child_element)

    return root_element

      


# Example XML data
xml_data = """
<room xmlns="http://www.example.com/onem2m">
    <temperature>23.5</temperature>
    <light>on</light>
</room>
"""

# Example XSD schema as a string
xsd_schema = """
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://www.example.com/onem2m"
           xmlns="http://www.example.com/onem2m"
           elementFormDefault="qualified">

  <!-- Define the room element -->
  <xs:element name="room">
    <xs:complexType>
      <xs:sequence>
        <!-- Define the temperature element -->
        <xs:element name="temperature" type="xs:decimal"/>

        <!-- Define the light element -->
        <xs:element name="light" type="xs:string"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""

# Call the validation function
validate_xml(xml_data, xsd_schema)

# Get XML structure
result_structure = get_xml_structure(xml_data)

# Create an instance of XMLToJsonConverter
converter = XMLToJsonConverter(result_structure)

# Convert to JSON
json_data = converter.convert_to_json()

# Display the result
print(json_data)










