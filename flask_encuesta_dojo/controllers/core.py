import os
from unittest import result
from winreg import FlushKey
from wsgiref.util import request_uri
from flask_encuesta_dojo import app
#se importa el modelo que contiene la clase
from flask_encuesta_dojo.models.encuestados import Encuestado
#se importa las funciones de flask
from flask import render_template, redirect, request, session, flash, jsonify
#se importan el modulo de fechas
from datetime import datetime, date
import json


#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/')
def main_page():
  if 'id_usuario' in session:
    session.pop('id_usuario')
  #tambien se devuelve la lista de diccionarios como una variable renderizada GET como practica
  return render_template('main.html')

#Ruta para Limpiar
@app.route('/limpiar')
def limpiar():
  session.clear()
  return redirect('/')


#Ruta por si el susuario volvio atras por un boton y no por el explorador
@app.route('/regreso')
def redirigir():
  print("ESTAMOS REDIRIGIENDO A INDEX!!!!")
  return redirect('/')


#Ruta para procesar ejecutando un metodo POST
@app.route('/grabar', methods=['POST'])
def procesar_usuario():

  #se obtienen los otros inputs de texto plano del form
  #y se almacenan en variables de sesion del form post
  cadena_json = request.form.getlist('lenguaje_prog[]')

  data = {
          'nombre':request.form['nombre'],
          'ubicacion':request.form['ubicacion'],
          'idioma':request.form['idioma'],
          'lenguaje_prog':json.dumps(cadena_json),
          'edad':int(request.form['edad']),
          'comentarios':request.form['comentarios'],
          }
  #se alamacena en la base de datos
  session['id_usuario'] = Encuestado.save(data)

  #se redirige el POST hacia la pagina de checkout
  return redirect('/result')


#Ruta para el checkout
@app.route('/result')
def checkout():
  #se rederiza la pagina checkout
  diasemana = ['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
  meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

  today = diasemana[date.today().weekday()] + ', ' + str(date.today().day) + ' de ' + meses[date.today().month] + ' de ' + str(date.today().year)
  datos = {'id':session['id_usuario']}
  datos_encuestado = Encuestado.get_by_id(datos)

  return render_template('enviado.html',hoy = today,encuestado=datos_encuestado)


if __name__=="__main__":   # Asegúrate de que este archivo se esté ejecutando directamente y no desde un módulo diferente    
    app.run(debug=True)    # Ejecuta la aplicación en modo de depuración