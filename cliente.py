# ===================================================================
# cliente.py - Clase Cliente (Paciente del Consultorio)
# ===================================================================
# Actividad Individual N° 2 - Colas de Atencion
# Programacion 2 - Universidad de Manizales (2026-2)
# Estudiante: Nicolas David Solano Plazas
# Codigo: 106202524246
# ===================================================================

class Cliente:
    """
    Representa a un paciente que asiste al consultorio odontologico
    Gestiona sus datos personales, tipo de cita, prioridad y calculo
    estricto de tarifas
    """

    # Tarifas del consultorio segun el tipo de afiliacion del paciente
    TARIFAS = {
        "particular": {
            "valor_cita": 80000.0,
            "limpieza": 60000.0,
            "calzas": 80000.0,
            "extraccion": 100000.0,
            "diagnostico": 50000.0
        },
        "eps": {
            "valor_cita": 5000.0,
            "limpieza": 0.0,
            "calzas": 40000.0,
            "extraccion": 40000.0,
            "diagnostico": 0.0
        },
        "prepagada": {
            "valor_cita": 30000.0,
            "limpieza": 0.0,
            "calzas": 10000.0,
            "extraccion": 10000.0,
            "diagnostico": 0.0
        }
    }

    def __init__(self, cedula: str, nombre: str, telefono: str, tipo_cliente: str,
                 tipo_atencion: str, cantidad: int, prioridad_atencion: str,
                 fecha_cita: str, hora_cita: str = "08:00"):
        # Validacion de datos obligatorios en constructor
        self.cedula = str(cedula).strip()
        self.nombre = str(nombre).strip()
        self.telefono = str(telefono).strip()
        self.tipo_cliente = str(tipo_cliente).strip().lower()
        self.tipo_atencion = str(tipo_atencion).strip().lower()
        self.prioridad_atencion = str(prioridad_atencion).strip().lower()
        self.fecha_cita = str(fecha_cita).strip()
        self.hora_cita = str(hora_cita).strip()

        # Si el procedimiento es limpieza o diagnostico siempre es 1 pieza
        if self.tipo_atencion in ["limpieza", "diagnostico"]:
            self.cantidad = 1
        else:
            self.cantidad = int(cantidad) if int(cantidad) > 0 else 1

        # Calculo exacto del valor como float
        self.valor_total = float(self.calcular_valor_servicio())

    def calcular_valor_servicio(self) -> float:
        """Calcula el valor total a cobrar como tipo float no negativo"""
        tarifa = self.TARIFAS.get(self.tipo_cliente, {})
        valor_cita = float(tarifa.get("valor_cita", 0.0))
        valor_atencion = float(tarifa.get(self.tipo_atencion, 0.0))

        total = valor_cita + (valor_atencion * float(self.cantidad))
        return round(float(total), 2)

    def obtener_desglose(self):
        """Devuelve el desglose de valores en formato float"""
        tarifa = self.TARIFAS.get(self.tipo_cliente, {})
        valor_cita = float(tarifa.get("valor_cita", 0.0))
        valor_atencion = float(tarifa.get(self.tipo_atencion, 0.0))
        return valor_cita, valor_atencion

    def es_urgente(self) -> bool:
        """Determina si el paciente requiere atencion prioritaria"""
        return self.prioridad_atencion == "urgente"
