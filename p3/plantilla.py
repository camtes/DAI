## -*- coding: utf-8 -*-
##
## Autor: Carlos Campos Fuentes
## 		  http://ccamposfuentes.es
import web
from web import form
from web.contrib.template import render_mako

web.config.debug = False

urls = ('/', 'index',
		'/logout', 'logout',
		'/pagina1', 'pagina1',
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

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla accumsan sit amet felis at mattis. \
	Sed nec congue dolor, ut efficitur leo. Nam quis ante at augue venenatis vestibulum. Integer sodales iaculis nunc a dapibus. \
	Sed facilisis mattis nunc eu viverra. Nullam venenatis cursus arcu eu pretium. Nam lobortis neque mi, porttitor placerat massa tempus id. \
	Maecenas quis tincidunt nunc. Nulla fermentum massa quis aliquam viverra. In tincidunt pharetra hendrerit. Curabitur non tincidunt metus. \
	Nunc sodales arcu dui, at elementum dolor sollicitudin eu. Donec id congue velit. Aenean placerat leo ac est sagittis finibus. \
	Sed malesuada sodales nibh sit amet convallis. Curabitur ultrices pulvinar enim eget convallis. Praesent ultricies pretium dui, \
	at tincidunt justo tristique molestie. Donec ornare, enim vel ullamcorper sodales, justo metus dictum metus, \
	vel sagittis nibh tortor vel leo. Maecenas id nisl et metus volutpat elementum. Cras dignissim erat non ex ultrices imperdiet. \
	Aliquam pharetra condimentum ligula at molestie. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. \
	Curabitur non libero vitae dolor vestibulum maximus. Vestibulum egestas nibh urna, vitae vehicula lectus consectetur id. Sed et elit eros. \
	Quisque sodales venenatis arcu condimentum consequat. Sed leo quam, maximus eu metus vulputate, posuere varius risus. \
	Praesent ac facilisis leo. Nam non lacus enim. Aliquam nisi enim, maximus in risus eget, porta egestas neque. \
	Pellentesque fermentum sit amet lacus quis cursus. In volutpat sodales ipsum, eget dictum erat tincidunt quis. \
	Nunc malesuada odio sapien, et dapibus tellus imperdiet sit amet. Duis interdum efficitur orci, non rutrum augue ornare at. \
	Fusce suscipit turpis eget turpis auctor, ac fermentum risus euismod."

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
			return templates.template(titulo = "Inicio", message = insert_message(session.user), ultimas = insert_last())

class pagina1:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Pagina 1", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='pagina1'>Pagina 1</a>"
			return templates.template(titulo = "Pagina 1", message = insert_message(session.user), content = str(lorem), ultimas = insert_last())

class pagina2:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Pagina 2", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='pagina2'>Pagina 2</a>"
			return templates.template(titulo = "Pagina 2", message = insert_message(session.user), content = str(lorem), ultimas = insert_last())

class pagina3:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Pagina 3", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='pagina3'>Pagina 3</a>"
			return templates.template(titulo = "Pagina 3", message = insert_message(session.user), content = str(lorem), ultimas = insert_last())
		
class pagina4:
	def GET(self):
		if 'user' not in session:
			form = formLogin()
			return templates.template(titulo = "Pagina 4", form = form)
		else:
			session.tercera = session.segunda
			session.segunda = session.primera
			session.primera = "<a href='pagina4'>Pagina 4</a>"
			return templates.template(titulo = "Pagina 4", message = insert_message(session.user), content = str(lorem), ultimas = insert_last())

class logout:
	def GET(self):
		session.kill()
		raise web.seeother('/')

if __name__ == "__main__":
	app.run()