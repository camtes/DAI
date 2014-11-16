# -*- coding: UTF-8 -*-
#
# Formulario
# Práctica 3 - DAI - Carlos Campos Fuentes

import re
import anydbm
import web
from web import form

#Plantillas en el directorio ./Plantillasr
render = web.template.render('templates/')
urls = (
	'/', 'myForm',
	)

app = web.application(urls, globals())

# 404
def notfound():
	return web.notfound("No se encuentra la página que estas buscando")

app.notfound = notfound

# Expresiones regulares
email = re.compile(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$')
visa = re.compile(r'[0-9]{4}([\ \-]?)[0-9]{4}([\ \-]?)[0-9]{4}([\ \-]?)[0-9]{4}([\ \-]?)')

# Formulario
formulario = form.Form(
	form.Textbox('nombre', form.notnull, maxlenght="30", description="Nombre: "),
	form.Textbox('apellidos', form.notnull, maxlenght="50", description="Apellidos: "),
	form.Textbox("dni", form.notnull, maxlenght="8", description="DNI: "),
	form.Textbox('correo', form.notnull, 
		form.Validator("Formato de correo no valido", lambda i: email.match(i)),
		maxlenght="50", description="Correo electrónico: "),
	form.Textbox('visa', form.notnull, 
		form.Validator("El formato de la VISA no es valido.", lambda i: visa.match(i)),
		maxlenght="19", description="VISA: "),
	form.Dropdown('dia', range(1,32), description="Día: "),
	form.Dropdown('mes', range(1,13), description="Mes: "),
	form.Dropdown('ano', range(1900, 2015), description="Año: "),
	form.Textarea("descripcion", maxlenght="120", description="Descripción: "),
	form.Password("contrasena", form.notnull, 
		form.Validator("La contraseña debe de tener 8 caracteres como mínimo.", lambda i: len(str(i))>7),
		maxlenght="8", description="Contraseña: "),
	form.Password("contrasena2", form.notnull, 
		form.Validator("La contraseña debe de tener 8 caracteres como mínimo.", lambda i: len(str(i))>7),
		maxlenght="8", description="Vuelve a introducir la contraseña: "),
	form.Radio("pago", ["PayPal", "Tarjeta"], form.notnull, description="Forma de pago: "),
	form.Checkbox('condiciones', 
		form.Validator("Debes de aceptar las clausulas", lambda i: i == 'true'), value='true'),
	form.Button("Enviar"),

	validators = [
		form.Validator("Fecha incorrecta.", lambda x: not(
			(int(x.dia)==29 and int(x.mes)==2) or
			(int(x.dia)==29 and int(x.mes)==2 and int(x.anio)%4!=0) or
			(int(x.dia)==30 and int(x.mes)==2) or
			(int(x.dia)==31 and int(x.mes)%2==0)
		)),
		form.Validator("Las contraseñas no coinciden.", lambda i: i.contrasena == i.contrasena2),
	]
)

class myForm:
	def GET(self):
		form = formulario()
		return render.formulario(form)

	def POST(self):
		form = formulario()
		if not form.validates():
			return render.formulario(form)
		else:
			aux = web.input()
			db = anydbm.open('db','c')

			# Grabo los datos en la base de datos
			db["nombre"] = str(aux.nombre)
			db["apellidos"] = str(aux.apellidos)
			db["dni"] = str(aux.dni)
			db["correo"] = str(aux.correo)
			db["visa"] = str(aux.visa)
			db["dia"] = str(aux.dia)
			db["mes"] = str(aux.mes)
			db["ano"] = str(aux.ano)
			db["descripcion"] = str(aux.descripcion)
			db["contrasena"] = str(aux.contrasena)
			db["contrasena2"] = str(aux.contrasena2)
			db["pago"] = str(aux.pago)

			# Cerramos la base de datos
			db.close()

			# Devolvemos que se a guarado correctamente.
			return str("Formulario almacenado correctamente.")


if __name__ == "__main__":
	app.run()