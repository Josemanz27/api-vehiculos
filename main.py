from fastapi import FastAPI, HTTPException, Depends, Form, APIRouter
import mysql.connector
from typing import List
from mysql.connector import Error
import schemas  # Importar los esquemas desde schemas.py

app = FastAPI(title="Documentacion de API-Vechiculos", description="La API gestiona la informacion de los vehiculos registradas en el sistema", version="1.0.0")

host_name = "52.6.145.141"
port_number = "8007"
user_name = "root"
password_db = "jjj"
database_name = "bd_api_licencias"

# Conectar a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para crear un regitro en la tabla vehiculo
@app.post("/vehiculos/", summary="Agregar un nuevo vehículo")
def create_vehiculo(vehiculo: schemas.Vehiculo, db=Depends(get_db_connection)):
    cursor = db.cursor()
    try:
        sql = "INSERT INTO vehiculo (marca, modelo, ano, placa) VALUES (%s, %s, %s, %s)"
        val = (vehiculo.marca, vehiculo.modelo, vehiculo.ano, vehiculo.placa)
        cursor.execute(sql, val)
        db.commit()
    except Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()
    return {"message": "Vehículo agregado exitosamente"}

@app.get("/vehiculos/{vehiculo_id}", summary="Obtener detalles de un vehículo")
def read_vehiculo(vehiculo_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM vehiculo WHERE id = %s", (vehiculo_id,))
        vehiculo = cursor.fetchone()
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()
    if vehiculo:
        return vehiculo
    else:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

@app.put("/vehiculos/{vehiculo_id}", summary="Actualizar un vehículo existente")
def update_vehiculo(vehiculo_id: int, vehiculo: schemas.Vehiculo, db=Depends(get_db_connection)):
    cursor = db.cursor()
    try:
        sql = "UPDATE vehiculo SET marca = %s, modelo = %s, ano = %s, placa = %s WHERE id = %s"
        val = (vehiculo.marca, vehiculo.modelo, vehiculo.ano, vehiculo.placa, vehiculo_id)
        cursor.execute(sql, val)
        db.commit()
    except Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()
    return {"message": "Vehículo actualizado exitosamente"}

@app.delete("/vehiculos/{vehiculo_id}", summary="Eliminar un vehículo")
def delete_vehiculo(vehiculo_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM vehiculo WHERE id = %s", (vehiculo_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado para eliminar")
    except Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()
    return {"message": "Vehículo eliminado exitosamente"}

# Propietario
@app.post("/propietarios/", summary="Agregar un nuevo propietario", response_model=schemas.Propietario)
def create_propietario(propietario: schemas.Propietario, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "INSERT INTO propietario (name) VALUES (%s)"
    val = (propietario.name,)
    cursor.execute(sql, val)
    db.commit()
    propietario_id = cursor.lastrowid
    db.close()
    return {**propietario.dict(), "id": propietario_id}

@app.get("/propietarios/{propietario_id}", summary="Obtener detalles de un propietario", response_model=schemas.Propietario)
def read_propietario(propietario_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM propietario WHERE id = %s", (propietario_id,))
    propietario = cursor.fetchone()
    db.close()
    if propietario:
        return propietario
    else:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")

@app.put("/propietarios/{propietario_id}", summary="Actualizar un propietario existente", response_model=schemas.Propietario)
def update_propietario(propietario_id: int, propietario: schemas.Propietario, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "UPDATE propietario SET name = %s WHERE id = %s"
    val = (propietario.name, propietario_id)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    return {**propietario.dict(), "id": propietario_id}

@app.delete("/propietarios/{propietario_id}", summary="Eliminar un propietario")
def delete_propietario(propietario_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM propietario WHERE id = %s", (propietario_id,))
    db.commit()
    rows_deleted = cursor.rowcount
    db.close()
    if rows_deleted:
        return {"message": "Propietario eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Propietario no encontrado para eliminar")

# propiedad
@app.post("/propiedades/", summary="Agregar una nueva propiedad", response_model=schemas.Propiedad)
def create_propiedad(propiedad: schemas.Propiedad, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "INSERT INTO propiedad (id_propietario, id_vehiculo, fecha_reg) VALUES (%s, %s, %s)"
    val = (propiedad.id_propietario, propiedad.id_vehiculo, propiedad.fecha_reg)
    cursor.execute(sql, val)
    db.commit()
    propiedad_id = cursor.lastrowid
    db.close()
    return {**propiedad.dict(), "id": propiedad_id}

@app.get("/propiedades/{propiedad_id}", summary="Obtener detalles de una propiedad", response_model=schemas.Propiedad)
def read_propiedad(propiedad_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM propiedad WHERE id = %s", (propiedad_id,))
    propiedad = cursor.fetchone()
    db.close()
    if propiedad:
        return propiedad
    else:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")

@app.put("/propiedades/{propiedad_id}", summary="Actualizar una propiedad existente", response_model=schemas.Propiedad)
def update_propiedad(propiedad_id: int, propiedad: schemas.Propiedad, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "UPDATE propiedad SET id_propietario = %s, id_vehiculo = %s, fecha_reg = %s WHERE id = %s"
    val = (propiedad.id_propietario, propiedad.id_vehiculo, propiedad.fecha_reg, propiedad_id)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    return {**propiedad.dict(), "id": propiedad_id}

@app.delete("/propiedades/{propiedad_id}", summary="Eliminar una propiedad")
def delete_propiedad(propiedad_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM propiedad WHERE id = %s", (propiedad_id,))
    db.commit()
    rows_deleted = cursor.rowcount
    db.close()
    if rows_deleted:
        return {"message": "Propiedad eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada para eliminar")

# TasaImpuestos
@app.post("/tasa_impuesto/", summary="Agregar una nueva tasa de impuesto", response_model=schemas.TasaImpuesto)
def create_tasa_impuesto(tasa_impuesto: schemas.TasaImpuesto, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "INSERT INTO tasa_impuesto (descripcion, tasa) VALUES (%s, %s)"
    val = (tasa_impuesto.descripcion, tasa_impuesto.tasa)
    cursor.execute(sql, val)
    db.commit()
    tasa_impuesto_id = cursor.lastrowid
    db.close()
    return {**tasa_impuesto.dict(), "id": tasa_impuesto_id}

@app.get("/tasa_impuesto/{tasa_impuesto_id}", summary="Obtener detalles de una tasa de impuesto", response_model=schemas.TasaImpuesto)
def read_tasa_impuesto(tasa_impuesto_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasa_impuesto WHERE id = %s", (tasa_impuesto_id,))
    tasa_impuesto = cursor.fetchone()
    db.close()
    if tasa_impuesto:
        return tasa_impuesto
    else:
        raise HTTPException(status_code=404, detail="Tasa de impuesto no encontrada")

@app.put("/tasa_impuesto/{tasa_impuesto_id}", summary="Actualizar una tasa de impuesto existente", response_model=schemas.TasaImpuesto)
def update_tasa_impuesto(tasa_impuesto_id: int, tasa_impuesto: schemas.TasaImpuesto, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "UPDATE tasa_impuesto SET descripcion = %s, tasa = %s WHERE id = %s"
    val = (tasa_impuesto.descripcion, tasa_impuesto.tasa, tasa_impuesto_id)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    return {**tasa_impuesto.dict(), "id": tasa_impuesto_id}

@app.delete("/tasa_impuesto/{tasa_impuesto_id}", summary="Eliminar una tasa de impuesto")
def delete_tasa_impuesto(tasa_impuesto_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasa_impuesto WHERE id = %s", (tasa_impuesto_id,))
    db.commit()
    rows_deleted = cursor.rowcount
    db.close()
    if rows_deleted:
        return {"message": "Tasa de impuesto eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Tasa de impuesto no encontrada para eliminar")

# impuestos
@app.post("/impuestos/", summary="Agregar un nuevo impuesto", response_model=schemas.Impuesto)
def create_impuesto(impuesto: schemas.Impuesto, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "INSERT INTO impuesto (vehiculo_id, tasa_id, fecha, valor_imp) VALUES (%s, %s, %s, %s)"
    val = (impuesto.vehiculo_id, impuesto.tasa_id, impuesto.fecha, impuesto.valor_imp)
    cursor.execute(sql, val)
    db.commit()
    impuesto_id = cursor.lastrowid
    db.close()
    return {**impuesto.dict(), "id": impuesto_id}

@app.get("/impuestos/{impuesto_id}", summary="Obtener detalles de un impuesto", response_model=schemas.Impuesto)
def read_impuesto(impuesto_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM impuesto WHERE id = %s", (impuesto_id,))
    impuesto = cursor.fetchone()
    db.close()
    if impuesto:
        return impuesto
    else:
        raise HTTPException(status_code=404, detail="Impuesto no encontrado")

@app.put("/impuestos/{impuesto_id}", summary="Actualizar un impuesto existente", response_model=schemas.Impuesto)
def update_impuesto(impuesto_id: int, impuesto: schemas.Impuesto, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "UPDATE impuesto SET vehiculo_id = %s, tasa_id = %s, fecha = %s, valor_imp = %s WHERE id = %s"
    val = (impuesto.vehiculo_id, impuesto.tasa_id, impuesto.fecha, impuesto.valor_imp, impuesto_id)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    return {**impuesto.dict(), "id": impuesto_id}

@app.delete("/impuestos/{impuesto_id}", summary="Eliminar un impuesto")
def delete_impuesto(impuesto_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM impuesto WHERE id = %s", (impuesto_id,))
    db.commit()
    rows_deleted = cursor.rowcount
    db.close()
    if rows_deleted:
        return {"message": "Impuesto eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Impuesto no encontrado para eliminar")

# deudas
@app.post("/deudas/", summary="Agregar una nueva deuda", response_model=schemas.Deuda)
def create_deuda(deuda: schemas.Deuda, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "INSERT INTO deuda (vehiculo_id, monto, descripcion) VALUES (%s, %s, %s)"
    val = (deuda.vehiculo_id, deuda.monto, deuda.descripcion)
    cursor.execute(sql, val)
    db.commit()
    deuda_id = cursor.lastrowid
    db.close()
    return {**deuda.dict(), "id": deuda_id}

@app.get("/deudas/{deuda_id}", summary="Obtener detalles de una deuda", response_model=schemas.Deuda)
def read_deuda(deuda_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM deuda WHERE id = %s", (deuda_id,))
    deuda = cursor.fetchone()
    db.close()
    if deuda:
        return deuda
    else:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")

@app.put("/deudas/{deuda_id}", summary="Actualizar una deuda existente", response_model=schemas.Deuda)
def update_deuda(deuda_id: int, deuda: schemas.Deuda, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "UPDATE deuda SET vehiculo_id = %s, monto = %s, descripcion = %s WHERE id = %s"
    val = (deuda.vehiculo_id, deuda.monto, deuda.descripcion, deuda_id)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    return {**deuda.dict(), "id": deuda_id}

@app.delete("/deudas/{deuda_id}", summary="Eliminar una deuda")
def delete_deuda(deuda_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM deuda WHERE id = %s", (deuda_id,))
    db.commit()
    rows_deleted = cursor.rowcount
    db.close()
    if rows_deleted:
        return {"message": "Deuda eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Deuda no encontrada para eliminar")

# robos
@app.post("/robos/", summary="Agregar un nuevo robo", response_model=schemas.Robo)
def create_robo(robo: schemas.Robo, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "INSERT INTO robo (vehiculo_id, fecha, descripcion) VALUES (%s, %s, %s)"
    val = (robo.vehiculo_id, robo.fecha, robo.descripcion)
    cursor.execute(sql, val)
    db.commit()
    robo_id = cursor.lastrowid
    db.close()
    return {**robo.dict(), "id": robo_id}

@app.get("/robos/{robo_id}", summary="Obtener detalles de un robo", response_model=schemas.Robo)
def read_robo(robo_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM robo WHERE id = %s", (robo_id,))
    robo = cursor.fetchone()
    db.close()
    if robo:
        return robo
    else:
        raise HTTPException(status_code=404, detail="Robo no encontrado")

@app.put("/robos/{robo_id}", summary="Actualizar un robo existente", response_model=schemas.Robo)
def update_robo(robo_id: int, robo: schemas.Robo, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "UPDATE robo SET vehiculo_id = %s, fecha = %s, descripcion = %s WHERE id = %s"
    val = (robo.vehiculo_id, robo.fecha, robo.descripcion, robo_id)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    return {**robo.dict(), "id": robo_id}

@app.delete("/robos/{robo_id}", summary="Eliminar un robo")
def delete_robo(robo_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM robo WHERE id = %s", (robo_id,))
    db.commit()
    rows_deleted = cursor.rowcount
    db.close()
    if rows_deleted:
        return {"message": "Robo eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Robo no encontrado para eliminar")

# accidente
@app.post("/accidentes/", summary="Agregar un nuevo accidente", response_model=schemas.Accidente)
def create_accidente(accidente: schemas.Accidente, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "INSERT INTO accidente (vehiculo_id, fecha, descripcion) VALUES (%s, %s, %s)"
    val = (accidente.vehiculo_id, accidente.fecha, accidente.descripcion)
    cursor.execute(sql, val)
    db.commit()
    accidente_id = cursor.lastrowid
    db.close()
    return {**accidente.dict(), "id": accidente_id}

@app.get("/accidentes/{accidente_id}", summary="Obtener detalles de un accidente", response_model=schemas.Accidente)
def read_accidente(accidente_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accidente WHERE id = %s", (accidente_id,))
    accidente = cursor.fetchone()
    db.close()
    if accidente:
        return accidente
    else:
        raise HTTPException(status_code=404, detail="Accidente no encontrado")

@app.put("/accidentes/{accidente_id}", summary="Actualizar un accidente existente", response_model=schemas.Accidente)
def update_accidente(accidente_id: int, accidente: schemas.Accidente, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "UPDATE accidente SET vehiculo_id = %s, fecha = %s, descripcion = %s WHERE id = %s"
    val = (accidente.vehiculo_id, accidente.fecha, accidente.descripcion, accidente_id)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    return {**accidente.dict(), "id": accidente_id}

@app.delete("/accidentes/{accidente_id}", summary="Eliminar un accidente")
def delete_accidente(accidente_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM accidente WHERE id = %s", (accidente_id,))
    db.commit()
    rows_deleted = cursor.rowcount
    db.close()
    if rows_deleted:
        return {"message": "Accidente eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Accidente no encontrado para eliminar")

# papeletas
@app.post("/papeletas/", summary="Agregar una nueva papeleta", response_model=schemas.Papeleta)
def create_papeleta(papeleta: schemas.Papeleta, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "INSERT INTO papeleta (vehiculo_id, fecha, descripcion) VALUES (%s, %s, %s)"
    val = (papeleta.vehiculo_id, papeleta.fecha, papeleta.descripcion)
    cursor.execute(sql, val)
    db.commit()
    papeleta_id = cursor.lastrowid
    db.close()
    return {**papeleta.dict(), "id": papeleta_id}

@app.get("/papeletas/{papeleta_id}", summary="Obtener detalles de una papeleta", response_model=schemas.Papeleta)
def read_papeleta(papeleta_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM papeleta WHERE id = %s", (papeleta_id,))
    papeleta = cursor.fetchone()
    db.close()
    if papeleta:
        return papeleta
    else:
        raise HTTPException(status_code=404, detail="Papeleta no encontrada")

@app.put("/papeletas/{papeleta_id}", summary="Actualizar una papeleta existente", response_model=schemas.Papeleta)
def update_papeleta(papeleta_id: int, papeleta: schemas.Papeleta, db=Depends(get_db_connection)):
    cursor = db.cursor()
    sql = "UPDATE papeleta SET vehiculo_id = %s, fecha = %s, descripcion = %s WHERE id = %s"
    val = (papeleta.vehiculo_id, papeleta.fecha, papeleta.descripcion, papeleta_id)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    return {**papeleta.dict(), "id": papeleta_id}

@app.delete("/papeletas/{papeleta_id}", summary="Eliminar una papeleta")
def delete_papeleta(papeleta_id: int, db=Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM papeleta WHERE id = %s", (papeleta_id,))
    db.commit()
    rows_deleted = cursor.rowcount
    db.close()
    if rows_deleted:
        return {"message": "Papeleta eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Papeleta no encontrada para eliminar")