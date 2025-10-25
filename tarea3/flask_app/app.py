from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from database import db
from utils import validations
from markupsafe import escape
import hashlib
import filetype
import os

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def portada():
    avisos = db.obtenerUltimosAvisos(limit=5)
    return render_template('portada.html', ultimos_avisos=avisos)


@app.route('/agregar_aviso', methods=['GET', 'POST'])
def agregar_aviso():
    regiones = db.obtenerRegiones()
    comunas = db.obtenerComunas()
    redes_sociales = db.obtenerRedesSociales()
    max_fotos = 5
    max_redes = 5
    

    fecha_minima = datetime.now().replace(second=0, microsecond=0) + timedelta(hours=3)
    fecha_str = fecha_minima.strftime("%Y-%m-%dT%H:%M")

    if request.method == "POST":
        aviso_fecha_default_str = request.form.get("fecha_minima")
        aviso_fecha_default = datetime.strptime(aviso_fecha_default_str, "%Y-%m-%dT%H:%M")

        aviso_region = request.form.get("region")
        aviso_comuna = request.form.get("comuna")
        aviso_sector = request.form.get("sector")
        aviso_nombre = request.form.get("nombre")
        aviso_email = request.form.get("email")
        aviso_celular = request.form.get("celular")
        aviso_redes = []

        for i in range(1, max_redes + 1):
            red_select = request.form.get(f"red_social_{i}")
            red_usuario = request.form.get(f"red_social_input_{i}")
            if red_select and red_usuario:
                aviso_redes.append({"medio": red_select, "usuario": red_usuario})

        aviso_tipo = request.form.get("tipo")
        aviso_cantidad = request.form.get("cantidad")
        aviso_edad = request.form.get("edad")
        aviso_unidad = request.form.get("unidad")
        
        aviso_fecha_entrega_str = request.form.get("fecha_entrega")
        aviso_fecha_entrega = datetime.strptime(aviso_fecha_entrega_str, "%Y-%m-%dT%H:%M")
        
        aviso_descripcion = request.form.get("descripcion")
        aviso_fotos = request.files.getlist("foto")

        errores = []


        if not aviso_region or aviso_region.strip() == "":
            errores.append("Debe seleccionar una región.")
        if not aviso_comuna or aviso_comuna.strip() == "":
            errores.append("Debe seleccionar una comuna.")
        if not validations.validate_sector(aviso_sector):
            errores.append("El sector es opcional, no puede superar los 100 caracteres.")
        if not validations.validate_nombre(aviso_nombre):
            errores.append("El nombre es obligatorio, debe tener entre 3 y 200 caracteres.")
        if not validations.validate_email(aviso_email):
            errores.append("Email obligatorio, formato incorrecto.")
        if not validations.validate_celular(aviso_celular):
            errores.append("celular opcional, debe tener el formato +NNN.NNNNNNNN.")
        for red in aviso_redes:
            if not validations.validate_red_social(red["usuario"]):
                errores.append(f"Red social opcional, {red['medio']} formato invalido.")
        if not validations.validate_tipo(aviso_tipo):
            errores.append("Debe seleccionar un tipo válido de mascota (Perro o Gato).")
        if not validations.validate_cantidad(aviso_cantidad):
            errores.append("Cantidad mínima 1.")
        if not validations.validate_edad(aviso_edad):
            errores.append("Edad mínima 1.")
        if not validations.validate_unidad(aviso_unidad):
            errores.append("Debe seleccionar una unidad válida (Meses o Años).")
        if not validations.validate_fecha(aviso_fecha_entrega, aviso_fecha_default):
            errores.append(f"La fecha debe ser igual o posterior a {fecha_minima.strftime('%Y-%m-%d %H:%M')}.")
        if not validations.validate_descripcion(aviso_descripcion):
            errores.append("Descripcion opcional, formato invalido.")
        if not validations.validate_fotos(aviso_fotos):
            errores.append("Debes subir al menos una foto válida (jpg, png, gif).")

        if errores:
            return render_template(
                'agregar_aviso.html',
                regiones=regiones,
                comunas=comunas,
                max_fotos=max_fotos,
                redes_sociales=redes_sociales,
                max_redes=max_redes,
                fecha_default=aviso_fecha_default_str,
                errores=errores
            )

        tipo_enum = db.Tipo(aviso_tipo)
        unidad_enum = db.Unidad(aviso_unidad)

        aviso_id = db.crear_aviso(
            comuna=aviso_comuna,
            sector=aviso_sector,
            nombre=aviso_nombre,
            email=aviso_email,
            celular=aviso_celular,
            tipo=tipo_enum,
            cantidad=int(aviso_cantidad),
            edad=int(aviso_edad),
            unidad=unidad_enum,
            fecha_entrega=aviso_fecha_entrega,
            descripcion=aviso_descripcion
        )

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])


        for file in aviso_fotos:
            if not file or file.filename == "":
                continue

            _filename = hashlib.sha256(
                secure_filename(file.filename).encode("utf-8")
            ).hexdigest()
            
            contenido = file.read()
            file.seek(0)  
            
            tipo = filetype.guess(contenido)
            if tipo is None:
                continue  
                
            _extension = tipo.extension
            img_filename = f"{_filename}.{_extension}"
            path = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
            file.save(path)

            ruta_relativa = os.path.join('uploads', img_filename)
            db.crear_foto(ruta_archivo=ruta_relativa, nombre_archivo=img_filename, aviso_id=aviso_id)

        for red in aviso_redes:
            medio_enum = db.MedioContacto(red["medio"])
            db.crear_contactar_por(nombre=medio_enum, identificador=red["usuario"], aviso_id=aviso_id)

        return redirect(url_for("portada"))

    return render_template(
        'agregar_aviso.html',
        regiones=regiones,
        comunas=comunas,
        max_fotos=max_fotos,
        redes_sociales=redes_sociales,
        max_redes=max_redes,
        fecha_default=fecha_str
    )


@app.route('/lista_avisos')
@app.route('/lista_avisos/<int:pagina>')
def lista_avisos(pagina=1):
    datos_paginados = db.obtenerAvisosPaginados(pagina=pagina, por_pagina=5)
    return render_template('lista_avisos.html', **datos_paginados)

@app.route('/api/avisos/<int:aviso_id>/comentarios', methods=['GET', 'POST'])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def comentarios_por_aviso(aviso_id):
    if request.method == 'GET':
        comentarios = db.obtenerComentariosPorAviso(aviso_id)
        items = []
        for c in comentarios:
            fecha_str = (c.fecha_creacion.strftime("%Y-%m-%d %H:%M")
                         if getattr(c, "fecha_creacion", None) else "")
            items.append({
                "id": int(c.id),
                "aviso_id": int(c.aviso_id),
                "nombre": c.nombre,
                "texto": c.texto,
                "fecha": fecha_str,
                "html": {
                    "nombre": escape(c.nombre),
                    "texto": escape(c.texto).replace("\n", "<br>")
                }
            })

        return jsonify({
            "ok": True,
            "comentarios": items
        })

    # POST
    data = request.get_json(silent=True) or {}

    comentario_nombre = (data.get("nombre") or "").strip()
    comentario_texto  = (data.get("texto") or "").strip()

    errores = []
    if not validations.validate_comentario_nombre(comentario_nombre):
        errores.append("El nombre es obligatorio y debe tener entre 3 y 80 caracteres.")
    if not validations.validate_comentario_texto(comentario_texto):
        errores.append("El comentario es obligatorio y debe tener entre 5 y 200 caracteres.")

    if errores:
        return jsonify({
            "ok": False,
            "errores": errores
        })

    comentario_id = db.crear_comentario(
        aviso_id=aviso_id,
        nombre=comentario_nombre,
        texto=comentario_texto
    )

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")

    return jsonify({
        "ok": True,
        "comentario": {
            "id": int(comentario_id),
            "aviso_id": int(aviso_id),
            "nombre": comentario_nombre,   
            "texto": comentario_texto,     
            "fecha": fecha_actual,
            "html": {
                "nombre": escape(comentario_nombre),
                "texto": escape(comentario_texto).replace("\n", "<br>")
            }
        }
    })


@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    return render_template('estadisticas.html')


@app.route("/estadisticas/avisos_por_dia", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def estadisticas_avisos_por_dia():
    data = db.obtenerAvisosPorDia() 
    return jsonify(data)


@app.route("/estadisticas/avisos_por_tipo", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def estadisticas_avisos_por_tipo():
    data = db.obtenerAvisosPorTipo()
    return jsonify(data)

@app.route("/estadisticas/avisos_por_mes_tipo", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def estadisticas_avisos_por_mes_y_tipo():
    data = db.obtenerAvisosPorMesTipo()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)