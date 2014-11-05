## -*- coding: utf-8 -*-
#
# Mako
# Práctica 3 - DAI - Carlos Campos Fuentes

import web
from web import form
from web.contrib.template import render_mako

web.config.debug = False

urls = ( '/', 'index' )

app = web.application(urls, globals(), autoreload=True)
formulario = form.Form(
	form.Textbox('usuario', form.notnull, maxlenght="30", description="Usuario: "),
	form.Password('password', maxlenght="10", description="Contraseña: "),
	form.Button("Login")
	)

plantillas = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )

class index:
    def GET(self):
        form = formulario()
        return plantillas.index(formu = form.render())

    def POST(self):
        usuario = web.input()
        user = usuario.nombre
        return plantillas.index(formu = "Bienvenido/a ".user)


	#def POST(self): #METER ESTO A MANO
	#	formu = formulario()
#
 #   	if not formu.validates():
  #  		return plantillas.mako(formu = formu.render())
   # 	
    #    else:
     #   	usuario = web.input()
      #  	usu_nombre = usuario.usuario
       # 	ses.nombre = usu_nombre
#
 #       	return plantillas.mako(formu = ses.nombre+" (logout)")
			

if __name__ == "__main__":
    app.run()