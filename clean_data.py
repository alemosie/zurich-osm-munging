# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from pprint import pprint as pp
import re
import json
import pdb
import random
# for unicode
import codecs

# Per http://wiki.openstreetmap.org/wiki/OSM_XML#Contents, only three types of root tags: node, way, relation
"""
Challenges:

    - What to do with refs
    http://wiki.openstreetmap.org/wiki/Key:ref


Analyses:
    - How many elements changed per changeset

"""

FULL_PATH = "zurich_switzerland.osm"
EXTRACT_PATH = "zurich_osm_extract.osm"

class ProcessParentTag():

    def __init__(self, element):
        self.created_keys = ["version", "changeset", "timestamp", "user", "uid"]
        self.element = element
        self.attribs = element.attrib
        self.document = self.create_document()

    def create_document(self):
        document = {}
        document["id"] = self.attribs["id"]
        document["type"] = self.element.tag
        document["created"] = {key: self.attribs[key] for key in self.created_keys}
        return document


class ProcessChildren():
    # does not assume that the element has children before processing
    def __init__(self, element):
        self.children = element.getchildren()
        self.document = self.create_full_document()

    def create_full_document(self):
        # process tag children
        tags = [element for element in self.children if element.tag == "tag"]
        tag_document = self.create_tag_document(tags)

        # process member children
        members = [element for element in self.children if element.tag == "member"]
        member_document = self.create_member_document(members)

        # process nd children
        nds = [element for element in self.children if element.tag == "nd"]
        nd_document = self.create_nd_document(nds)

        return dict(tag_document.items() + member_document.items() + nd_document.items())

    def process_nested_key(self, attrs, key):
        split = key.split(":") if ":" in key else key.split(".")

        # decision: only account for two layers of specificity in keys
        if len(split) == 2:
            if split[0] in attrs:
                attrs[split[0]][split[1]] = attrs[key]["base_value"]
            else:
                if split[0] == "source" and split[1] in attrs:
                    attrs[split[1]][split[0]] = attrs[key]["base_value"]
                else:
                    attrs[split[0]] = {}

        # delete old key with colon
        attrs.pop(key, None)
        return attrs

    def sanitize_base_values(self, attrs):
        for attr in attrs:
            if attrs[attr].keys() == ["base_value"]:
                attrs[attr] = attrs[attr]["base_value"]
        return attrs

    def sanitize_list_values(self, value):
        if ";" in value or "|" in value:
            return re.split(";|\|", value)
        else:
            return value

    def create_tag_document(self, tags):
        if len(tags) > 0:
            # to account for things like "wheelchair" and "wheelchair: description"
            children_attributes = {c.attrib["k"]:
                                  {"base_value":self.sanitize_list_values(c.attrib["v"])}
                                  for c in tags}
            for key in children_attributes.keys():
                if ":" in key or "." in key:
                    self.process_nested_key(children_attributes, key)
            # returns all element's children that are tag types
            return self.sanitize_base_values(children_attributes)
        else:
            return {}

    def create_member_document(self, members):
        if len(members) > 0:
            processed_members = []
            for child in members:
                # doing it this way to preserve order of relations
                child = child.attrib
                if child["role"] == "stop":
                    processed_members.append({"stop": child["ref"]})
                else:
                    processed_members.append({child["type"]: child["ref"]})
            return {"relations": processed_members}
        else:
            return {}

    def create_nd_document(self, nds):
        if len(nds) > 0:
            return {"refs": [child.attrib["ref"] for child in nds]}
        else:
            return {}


class ParseOSM(object):

    def __init__(self, osm_file):
        self.file = osm_file
        self.parse_tag_types()
        self.documents = []
        self.run_parser()


    def parse_tag_types(self):
        with codecs.open(self.file, "r") as raw_osm:
            tree = ET.parse(raw_osm)
            root = tree.getroot()
            self.nodes = root.findall("node")
            self.ways = root.findall("way")
            self.relations = root.findall("relation")

    def process_nodes(self):
        for node in self.nodes:
            base_document = ProcessParentTag(node).document
            base_document["position"] = [float(node.attrib["lat"]), float(node.attrib["lon"])]
            children = ProcessChildren(node).document # process child tags, if they exist

            full_document = dict(base_document.items() + children.items())
            self.documents.append(full_document)

    def process_relations(self):
        for relation in self.relations:
            base_document = ProcessParentTag(relation).document
            children = ProcessChildren(relation).document

            full_document = dict(base_document.items() + children.items())
            self.documents.append(full_document)

    def process_ways(self):
        for way in self.ways:
            base_document = ProcessParentTag(way).document
            children = ProcessChildren(way).document

            full_document = dict(base_document.items() + children.items())
            self.documents.append(full_document)

    def run_parser(self):
        self.process_nodes()
        self.process_relations()
        self.process_ways()

    def write_to_file(self, filename="", print_extract=0):
        with open(filename, "w") as json_file:
            json_file.write(json.dumps(self.documents))
        if print_extract > 0:
            pp(random.sample(self.documents, print_extract))

if __name__ == "__main__":
    osm = ParseOSM(FULL_PATH)
    osm.write_to_file(filename="data/zurich.json", print_extract=10)
