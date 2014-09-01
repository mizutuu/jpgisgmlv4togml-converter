# -*- coding: utf-8 -*-
# based on a script from http://wiki.openstreetmap.org/wiki/Converting_OSM_to_GML
# modified to work with JPGIS(GML) V4.0 XSD by yoshida
import os, sys, re, xml.sax
from xml.sax.handler import ContentHandler
from xml.etree.cElementTree import Element, SubElement, ElementTree
from fgdschema import fgdschema
from itertools import islice
from collections import deque

class fgd2gml (ContentHandler):
	def __init__ (self, fh, xsdfile):
		ContentHandler.__init__(self)
		self.fh = fh
		self.xsdfile = xsdfile

	def getFGDTags (self):
		with open(self.xsdfile) as f:
			schema = fgdschema(f)
			return schema.get_fgd_element_names()

	def getFGDNodeElements (self, name):
		with open(self.xsdfile) as f:
			schema = fgdschema(f)
			self.nodeelements = schema.get_fgd_elements(name)

	def getFGDNodeElement (self, name):
		for element in self.nodeelements:
			if element['name'] == name:
				return element
		return None

	def getFGDNodeElementType (self, name):
		element = self.getFGDNodeElement(name)
		if element is None:
			return None
		return element['type']

	def isFGDTag (self, name):
		# matched FGD element name. ('WStrL', 'Cstline', etc...)
		if name in self.tags:
			return True
		return False

	def isFGDNodeName (self, name):
		if self.featuretag is None:
			return False
		if self.nodeelements is None:
			self.getFGDNodeElements(self.featuretag)

		# matched FGD node member name. (case of WStrL element, 'loc', 'type', 'name', etc...)
		node = self.getFGDNodeElement(name)
		if node is None:
			return False

		return True

	def startDocument (self):
		self.tags = self.getFGDTags()
		self.nodeelements = None
		self.featuretag = None	# ex) 'WStrL', 'Cstline', etc...
		self.featureid = None

		self.currentstack = []
		self.current = None

		self.nodes = []

	def characters(self, data):
		if self.current is not None:
			self.currentstack[-1]['text'] += data

	def startElement (self, name, attr):
		if self.isFGDTag(name):
			# find new FGD tag.
			self.featuretag = name
			self.featureid = attr["gml:id"]
		elif self.isFGDNodeName(name):
			# find new FGD node tag.
			type = self.getFGDNodeElementType(name)
			self.current = {
				'name': name, # ex) 'fid', 'lfSpanFr', ...
				'type': type, # ex) 'xs:string', 'gml:TimeInstantType', ...
				'isgml': type[0:4] == 'gml:',
				'text': "",
				'node': []
			}
			self.currentstack.append( self.current )
			#print "S:", name, self.getFGDNodeElement(name)["type"]

		elif self.current is not None and self.current['isgml']:
			# find new tag, in FGD node.
			newNode = {
				'name': name,
				'text': "",
				'node': []
			}
			self.currentstack[-1]['node'].append( newNode )
			self.currentstack.append( newNode )

	def endElement (self, name):
		if self.current is not None and self.current['name'] == name:
			# find end FGD node tag.
			self.nodes.append(self.current)
			self.currentstack = []
			self.current = None
			#print "E:", name

		elif self.current is not None and self.current['isgml']:
			# find end tag, in FGD node.
			self.currentstack.pop()

		if name in self.tags and self.featuretag == name:
			# find end FGD tag.
			self.generateFeature()

			self.featureid = None
			self.currentstack = []
			self.current = None
			self.nodes = []

	def rebuildElement (self, parentElement, node):
		newElement = SubElement(parentElement, node['name'])
		newElement.text = node['text'].strip()

		if node['name'] in {'gml:pos', 'gml:posList'}:
			# convert the lat/lon -> lon/lat.
			contentlist = newElement.text.split("\n")
			newElement.text = ' '.join( [ x[1] + "," + x[0] for x in [x.split() for x in contentlist if x != ""]] )

		for n in node['node']:
			self.rebuildElement(newElement, n)

	def generateFeature (self):
		featureMember = Element('gml:featureMember')
		feature = SubElement(featureMember, 'ogr:' + self.featuretag)
		# set the fid.
		for node in self.nodes:
			if node['name'] == 'fid':
				feature.attrib['fid'] = node['text'].strip()

		# generate the id node.
		SubElement(feature, "ogr:id").text = self.featureid

		# generate the child nodes.
		for node in self.nodes:
			newElement = SubElement(feature, 'ogr:' + node['name'])
			newElement.text = node['text'].strip()

			if node['type'] in {'gml:CurvePropertyType', 'gml:DiscreteCoverageType',
                                            'gml:PointPropertyType', 'gml:SurfacePropertyType'}:
				geomElement = SubElement(newElement, 'ogr:geometryProperty')
				geomElement.text = node['text'].strip()
				for n in node['node']:
					self.rebuildElement(geomElement, n)

				# set the 'srsName' in child node.
				iter = geomElement.iter("*")
				gmlElement = next(islice(iter, 1, None), None)
				gmlElement.attrib['srsName'] = 'EPSG:4612'

			elif node['type'] == 'gml:TimeInstantType':
				lastElement = deque(node['node'], maxlen=1).pop()
				newElement.text = lastElement['text'].strip()

		ElementTree(featureMember).write(self.fh, 'utf-8')
		self.fh.write("\n")


if __name__ == "__main__":
	xsdfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'FGD_GMLSchema.xsd')
	fgdParser = fgd2gml(sys.stdout, xsdfile)
	print '<?xml version="1.0" encoding="utf-8" ?>'
	print '<ogr:FeatureCollection'
	print '     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
	print '     xsi:schemaLocation=""'
	print '     xmlns:ogr="http://ogr.maptools.org/"'
	print '     xmlns:gml="http://www.opengis.net/gml">'

	xml.sax.parse( sys.stdin, fgdParser )

	print '</ogr:FeatureCollection>'
