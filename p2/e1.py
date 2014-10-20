# -*- coding: UTF-8 -*-
# 
#

import web
from web import form

# Plantillas en el directorio ./plantillas
render = web.template.render('plantillas/')        
urls = (
    '/', 'hello',
    '/form', 'form'
)

app = web.application(urls, globals())

def notfound():
		return web.notfound("No se encuentra la página que estas buscando.")

app.notfound = notfound

login = form.Form(
    form.Textbox('username'),
    form.Password('password'),
    form.Button('Login'),
)

class hello:        
    def GET(self	):
        return render.inicio()

class form: 
    def GET(self): 
        form = login()
        # Hay que hacer una copia del formuario (linea superior)
        # O los cambios al mismo serían globales
        return """<html><body>
        <form name="input" action="/" method="post">
        %s
        </form>
        </body></html>
        """ % (form.render())

    def POST(self): 
        form = login() 
        if not form.validates(): 
            return render.formtest(form)
        else:
            return "Usuario: %s, Contrasenia: %s" % (form.d.username, form['password'].value)


if __name__ == "__main__":
    app.run()