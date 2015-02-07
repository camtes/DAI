from lxml import etree
import sys

tree = etree.parse(sys.argv[1])

rss = tree.getroot()
channel = rss[0]

num_noticias = 0

palabra_busca = sys.argv[2]

num_imagenes = 0

print ""


for e in channel:
	if (e.tag == 'item'):
		for ed in e:
			if(ed.tag == 'title' and palabra_busca in ed.text):
				num_noticias += 1
				print "Noticia ", num_noticias, "Titulo: ", ed.text
				print ""

			if(ed.tag == 'enclosure'):
				num_imagenes += 1


print "Total noticias ", num_noticias
print "Total imagenes ", num_imagenes
