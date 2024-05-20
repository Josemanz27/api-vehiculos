from pydantic import BaseModel,Field
from datetime import date

# Modelo de Pydantic para los datos de entrada

class Vehiculo(BaseModel):
    marca: str = Field(..., example="Toyota", description="Marca del vehículo")
    modelo: str = Field(..., example="Corolla", description="Modelo del vehículo")
    ano: int = Field(..., example=2020, description="Año de fabricación del vehículo")
    placa: str = Field(..., example="XYZ123", description="Placa de registro del vehículo")

class Propietario(BaseModel):
    name: str = Field(..., example="Juan Perez", description="Nombre completo del propietario del vehículo")

class Propiedad(BaseModel):
    id_propietario: int = Field(..., example=1, description="ID del propietario asociado a la propiedad")
    id_vehiculo: int = Field(..., example=2, description="ID del vehículo asociado a la propiedad")
    fecha_reg: date = Field(..., example="2024-01-01", description="Fecha de registro de la propiedad")

class TasaImpuesto(BaseModel):
    descripcion: str = Field(..., example="IVA Vehicular", description="Descripción del tipo de impuesto aplicado")
    tasa: float = Field(..., example=0.16, description="Porcentaje de la tasa de impuesto aplicada")

class Impuesto(BaseModel):
    vehiculo_id: int = Field(..., example=1, description="ID del vehículo asociado al impuesto")
    tasa_id: int = Field(..., example=1, description="ID de la tasa de impuesto aplicada")
    fecha: date = Field(..., example="2024-01-01", description="Fecha en que se registra el impuesto")
    valor_imp: float = Field(..., example=200.50, description="Valor monetario del impuesto")

class Deuda(BaseModel):
    vehiculo_id: int = Field(..., example=1, description="ID del vehículo asociado a la deuda")
    monto: float = Field(..., example=500.00, description="Monto total de la deuda")
    descripcion: str = Field(..., example="Multa por estacionamiento incorrecto", description="Descripción de la deuda")

class Robo(BaseModel):
    vehiculo_id: int = Field(..., example=1, description="ID del vehículo asociado al robo")
    fecha: date = Field(..., example="2024-01-01", description="Fecha en que ocurrió el robo")
    descripcion: str = Field(..., example="Robo en estacionamiento público", description="Descripción del incidente de robo")

class Robo(BaseModel):
    vehiculo_id: int = Field(..., example=1, description="ID del vehículo asociado al robo")
    fecha: date = Field(..., example="2024-01-01", description="Fecha en que ocurrió el robo")
    descripcion: str = Field(..., example="Robo en estacionamiento público", description="Descripción del incidente de robo")

class Accidente(BaseModel):
    vehiculo_id: int = Field(..., example=1, description="ID del vehículo asociado al accidente")
    fecha: date = Field(..., example="2024-01-01", description="Fecha en que ocurrió el accidente")
    descripcion: str = Field(..., example="Colisión con poste de luz", description="Descripción detallada del accidente")

class Papeleta(BaseModel):
    vehiculo_id: int = Field(..., example=1, description="ID del vehículo asociado a la papeleta")
    fecha: date = Field(..., example="2024-01-01", description="Fecha en que se emitió la papeleta")
    descripcion: str = Field(..., example="Exceso de velocidad en zona urbana", description="Descripción del motivo de la papeleta")
