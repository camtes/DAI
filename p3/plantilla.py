## -*- coding: utf-8 -*-
##
## Autor: Carlos Campos Fuentes
## 		  http://ccamposfuentes.es
import web
import anydbm
from web import form
from web.contrib.template import render_mako

web.config.debug = False

urls = ('/', 'index',
		'/logout', 'logout',
		'/datos', 'datos',
		'/pagina2', 'pagina2',
		'/pagina3', 'pagina3',
		'/pagina4', 'pagina4'
		)

app = web.application(urls, locals())

formLogin = form.Form(
	form.Textbox('username', form.notnull, maxlenght="30", description="Usuario "),
	form.Password('passwd', maxlenght="15", description="Contraseña "),
	form.Button("Login")
	)

session = web.session.Session(app, web.session.DiskStore('sessions'))

templates = render_mako(
    directories=['templates'],
    input_encoding='utf-8',
    output_encoding='utf-8',
    )

# Variables y funciones
def insert_message(user):
	return str("Bienvenido " + str(user) + " (<a href='/logout'>Logout</a>)")

def insert_last():
	return str("\
			<ol>\
				<li> "+ str(session.primera) + "</li>\
				<li> "+ str(session.segunda) + "</li>\
				<li> "+ str(session.tercera) + "</li>\
			</ol> \
		")

def insert_data():
	data = {}
	db = anydbm.open('db', 'c')
	# Recuperamos los datos de nuestra base de datos
	for k, v in db.iteritems():
		data[k] = v
	db.close()

	# Creamos cadena de texto
	return str("\
				<ul>\
					<li> Nombre: "+ str(data["nombre"]) +"</li>\
					<li> Apellidos: "+ str(data["apellidos"]) +"</li>\
					<li> DNI: "+ str(data["dni"]) +"</li>\
	"#				<li> Correo: "+str(data["correo"]) +"</li>\
	"				<li> VISA: "+ str(data["visa"]) +"</li>\
	"#				<li> Día: "+ str(data["dia"]) +"</li>\
	#				<li> Mes: "+ str(data["mes"]) +"</li>\
	#				<li> Año: "+ str(data["ano"]) +"</li>\
	#				<li> Descripción: "+ str(data["descripcion"]) +"</li>\
	#				<li> Contraseña: "+ str(data["contrasena"]) +"</li>\
	#				<li> Contraseña2: "+ str(data["contrasena2"]) +"</li>\
	"			</ul> \
				")



class index:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Inicio", form = form)
		else:
			return templates.template(titulo = "Inicio", message = insert_message(session.user), ultimas = insert_last())

	def POST(self):
		form = formLogin()

		if not form.validates():
			return templates.template(form = form)
		else:
			aux = web.input()
			user = aux.username
			session.user = user
			session.primera = "null"
			session.segunda = "null"
			session.tercera = "null"
			return templates.template(titulo = "Inicio", 
				message = insert_message(session.user), ultimas = insert_last())

class datos:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Datos", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='datos'>Datos</a>"
			return templates.template(titulo = "Datos", 
				message = insert_message(session.user), content = insert_data(), ultimas = insert_last())


class pagina2:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Pagina 2", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='pagina2'>Pagina 2</a>"
			return templates.template(titulo = "Pagina 2", 
				message = insert_message(session.user), ultimas = insert_last())

class pagina3:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Pagina 3", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='pagina3'>Pagina 3</a>"
			return templates.template(titulo = "Pagina 3", 
				message = insert_message(session.user), ultimas = insert_last())
		
class pagina4:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Pagina 4", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='pagina4'>Pagina 4</a>"
			return templates.template(titulo = "Pagina 4", 
				message = insert_message(session.user), ultimas = insert_last())

class logout:
	def GET(self):
		session.kill()
		raise web.seeother('/')

if __name__ == "__main__":
	app.run()