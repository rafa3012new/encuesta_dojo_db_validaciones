#la idea de esta clase es poder grabar las friendships
from flask_encuesta_dojo.config.mysqlconnection import connectToMySQL
import json
BASE_DATOS="encuesta_dojo"

# modelar la clase después de la tabla friendships de nuestra base de datos
class Encuestado:
    def __init__( self , data ):
        self.id_usuario= data['id']
        self.nombre = data['nombre']
        self.ubicacion = data['ubicacion']
        self.idioma = data['idioma']
        self.lenguaje_prog = data['lenguaje_prog']
        self.edad = data['edad']
        self.comentarios = data['comentarios']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM encuestados;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL(BASE_DATOS).query_db(query)
        # crear una lista vacía para agregar nuestras instancias de friendships
        datos = []
        # Iterar sobre los resultados de la base de datos y crear instancias de friendships con cls
        for dato in results:
            datos.append( cls(dato))
        return datos

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_by_id(cls,data):
        #armar la consulta con cadenas f
        query = 'SELECT * FROM encuestados where id = %(id)s;'
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL(BASE_DATOS).query_db(query, data)
        # var_lenguajes_prog = json.loads(results[0]['lenguaje_prog'])
        results[0]['lenguaje_prog'] = json.loads(results[0]['lenguaje_prog'])
        #devolver el primerl registro de los resultados si resultados devuelve algo sino que devuelva None
        return cls(results[0]) if len(results) > 0 else None


    @classmethod
    def save(cls, data):
        query = "INSERT INTO encuestados (nombre , ubicacion, idioma, lenguaje_prog,  edad, comentarios) VALUES ( %(nombre)s, %(ubicacion)s, %(idioma)s, %(lenguaje_prog)s, %(edad)s, %(comentarios)s);"
        # data es un diccionario que se pasará al método de guardar desde server.py
        datos = connectToMySQL(BASE_DATOS).query_db( query, data)
        return datos


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM encuestados WHERE id = %(id)s;"
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        return resultado