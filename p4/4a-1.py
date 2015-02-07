#-*- coding: utf-8 -*-
from lxml import etree
import re
import urllib
import sys

im = re.compile('image(.?)*')

class ParseRssNews():
	contN = 0
	contI = 0
	if len(sys.argv) > 1:
		encontrado = False
		termino = sys.argv[2]

	def start (self, tag, attrib): # Etiquetas de inicio
		if tag == 'item':
			self.contN += 1

		if tag == 'enclosure':
			for k in attrib:
				if k == 'type' and im.search(attrib[k]) != None:
					self.contI += 1
					name = 'imagen' + str(self.contI) + '.jpg'
					# Descargar las imágenes
					#urllib.urlretrieve(attrib['url'], "img/"+name);

	def data (self, data):
		if len(sys.argv) > 1:
			tr = re.compile('\s'+self.termino+'\s')
			if tr.search(data) != None:
				self.encontrado = True

	def close (self):
		print 'Número de noticias: ' + str(self.contN)
		print 'Número de imágenes: ' + str(self.contI)
		if len(sys.argv) > 1:
			if self.encontrado:
				print 'Existen noticias con el término ' +self.termino
			else:
				print 'No existen noticias con el término ' +self.termino

parser = etree.XMLParser (target=ParseRssNews())
etree.parse (sys.argv[1], parser)
