# -*- coding: utf-8 -*-

from lxml import etree
from copy import copy
SCHEMA_SPACE = {
	"fgd:"   : "{http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema}",
	"gml:"   : "{http://www.opengis.net/gml/3.2}",
	"xlink:" : "{http://www.w3.org/1999/xlink}",
	"xs:"    : "{http://www.w3.org/2001/XMLSchema}"
}

class schema:
	def __init__(self, schemafile):
		self.root = etree.parse(schemafile)

	def replace_ns(self, path):
		for k, v in SCHEMA_SPACE.iteritems():
			path = path.replace(k, v)
		return path

	def findall(self, path):
		return self.root.findall( self.replace_ns(path) )

	def find(self, path):
		return self.root.find( self.replace_ns(path) )

	def names_of(self, nodes):
		return [node.get("name") for node in nodes]

	def get_Types(self, t_name):
		return self.names_of( self.findall(t_name) ) 

	def get_simpleTypes(self):
		return self.get_Types("xs:simpleType")

	def get_complexTypes(self):
		return self.get_Types("xs:complexType")

	def get_elements_of_attribute(self, attribute):
		return self.names_of(self.findall(".//xs:element/xs:complexType/xs:" + attribute + "/../.."))

	def get_element_attributes(self, name): 
		node = self.find(".//xs:element[@name='" + name + "']")
		if node is None:
			node = self.find(".//xs:complexType[@name='" + name + "']")

		if node is None:
			return None
		else:
			return node.attrib
