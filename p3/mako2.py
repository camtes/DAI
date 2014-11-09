## -*- coding: utf-8 -*-
#
# Mako
# Práctica 3 - DAI - Carlos Campos Fuentes

import web
from web import form
from web.contrib.template import render_mako

# Para poder usar sesiones con web.py
web.config.debug = False

# Paginas enlazadas
urls = ( '/', 'index',
        '/logout', 'logout' )

app = web.application(urls, globals(), autoreload=True)

# Inicializamos la variable session a cadena vacía porque inicialmente no hay ningún usuario que haya iniciado sesion
session = web.session.Session(app, web.session.DiskStore('sessions'))

# Formulario para hacer login
formulario = form.Form(
	form.Textbox('usuario', form.notnull, maxlenght="30", description="Usuario: "),
	form.Password('password', maxlenght="10", description="Contraseña: "),
	form.Button("Login")
	)

# Plantilla de mako
plantillas = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )

class index:
  def GET(self):
    formLogin = formulario()
    return plantillas.index(form = formLogin)

  def POST(self):
    formLogin = formulario()

    if not formLogin.validates():
      return plantillas.index(form = formLogin)

    else:
      i = web.input()
      usuario = i.usuario
      session.usuario = usuario
      return plantillas.index(mensaje = "Bienvenido " + str(session.usuario) + "(<a href='/logout'>Logout</a>)")

class logout:
  session.usuario = False
  raise web.seeother('/')

if __name__ == "__main__":
    app.run()