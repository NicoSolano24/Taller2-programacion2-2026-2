# ===================================================================
# utilidades.py - Funciones de Validacion y Entrada Segura de Datos
# ===================================================================
# Actividad Individual N° 2 - Colas de Atencion
# Programacion 2 - Universidad de Manizales (2026-2)
# Estudiante: Nicolas David Solano Plazas
# Codigo: 106202524246
# ===================================================================

from datetime import datetime
import random
from cliente import Cliente
from cola_atencion import ColaAtencion


def leer_texto_no_vacio(mensaje: str) -> str:
    """
    Solicita una cadena de texto obligatoria
    Garantiza que no sea vacia ni este compuesta unicamente por espacios en blanco
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada != "":
            return entrada
        print("  [Error] Este campo es obligatorio y no puede quedar vacio.")


def leer_entero_positivo(mensaje: str) -> int:
    """
    Solicita un numero entero estrictamente mayor que cero como cantidad de piezas
    Garantiza que el tipo retornado sea 'int' y no permita negativos o letras
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if valor > 0:
                return valor
            print("  [Error] Debe ingresar un numero entero mayor que 0 (no se permiten ceros ni negativos).")
        except ValueError:
            print("  [Error] Valor invalido. Debe ingresar un numero entero valido.")


def leer_float_positivo(mensaje: str, permitir_cero: bool = True) -> float:
    """
    Solicita un valor decimal (float)
    Garantiza que el valor sea de tipo 'float' y no negativo
    Acepta tanto punto como coma decimal
    """
    while True:
        entrada = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if permitir_cero and valor >= 0.0:
                return float(valor)
            elif not permitir_cero and valor > 0.0:
                return float(valor)
            print("  [Error] El monto debe ser un numero positivo no negativo.")
        except ValueError:
            print("  [Error] Valor invalido. Debe ingresar un numero decimal o entero valido.")


def leer_telefono(mensaje: str) -> str:
    """
    Solicita un numero de telefono celular colombiano
    Valida que contenga exactamente 10 digitos numericos
    """
    while True:
        entrada = input(mensaje).strip()
        if entrada.isdigit() and len(entrada) == 10:
            return entrada
        print("  [Error] El telefono debe tener exactamente 10 digitos numericos.")


def leer_documento(mensaje: str, cola_atencion: ColaAtencion = None) -> str:
    """
    Solicita el documento de identidad del paciente
    Valida que no este vacio, sea numerico y que no se encuentre repetido en las colas
    """
    while True:
        cedula = input(mensaje).strip()
        if cedula == "":
            print("  [Error] El documento de identidad no puede estar vacio.")
        elif not cedula.isdigit():
            print("  [Error] El documento debe contener unicamente digitos numericos.")
        elif cola_atencion is not None and cola_atencion.existe_cedula_en_cola(cedula):
            print(f"  [Error] El documento {cedula} ya esta en la sala de espera. Ingrese otro.")
        else:
            return cedula


def leer_opcion_valida(mensaje: str, opciones: list) -> str:
    """
    Solicita al usuario una opcion de una lista predeterminada
    Valida sin importar si se escribe en mayusculas o minusculas
    """
    opciones_lower = [op.lower() for op in opciones]
    while True:
        entrada = input(mensaje).strip().lower()
        if entrada in opciones_lower:
            return entrada
        print(f"  [Error] Opcion no valida. Opciones permitidas: {', '.join(opciones)}")


def leer_fecha(mensaje: str) -> str:
    """
    Solicita una fecha de cita y valida el formato estricto DD-MM-AAAA
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            datetime.strptime(entrada, "%d-%m-%Y")
            return entrada
        except ValueError:
            print("  [Error] Formato de fecha invalido. Debe usar el formato DD-MM-AAAA (ejemplo: 27-08-2026).")


def leer_hora(mensaje: str) -> str:
    """
    Solicita una hora y valida el formato HH:MM (ejemplo: 08:30)
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            datetime.strptime(entrada, "%H:%M")
            return entrada
        except ValueError:
            print("  [Error] Formato de hora invalido. Debe usar el formato HH:MM (ejemplo: 09:15).")


def registrar_paciente_por_consola(cola_atencion: ColaAtencion):
    """
    Formulario interactivo para registrar un paciente y encolarlo
    de acuerdo con su nivel de prioridad
    """
    print("\n" + "-" * 55)
    print("  INGRESO Y ENCOLADO DE NUEVO PACIENTE A LA CLINICA")
    print("-" * 55)

    cedula = leer_documento("  Documento (Cedula o TI): ", cola_atencion)
    nombre = leer_texto_no_vacio("  Nombre completo del paciente: ")
    telefono = leer_telefono("  Telefono celular (10 digitos): ")

    tipo_cliente = leer_opcion_valida(
        "  Tipo de afiliacion (particular / eps / prepagada): ",
        ["particular", "eps", "prepagada"]
    )

    tipo_atencion = leer_opcion_valida(
        "  Tipo de atencion (limpieza / calzas / extraccion / diagnostico): ",
        ["limpieza", "calzas", "extraccion", "diagnostico"]
    )

    if tipo_atencion in ["calzas", "extraccion"]:
        cantidad = leer_entero_positivo("  Numero de piezas a intervenir: ")
    else:
        cantidad = 1
        print(f"  Numero de piezas: 1 (Fija para {tipo_atencion})")

    prioridad = leer_opcion_valida(
        "  Nivel de prioridad (normal / urgente): ",
        ["normal", "urgente"]
    )

    fecha = leer_fecha("  Fecha de la cita (DD-MM-AAAA): ")
    hora = leer_hora("  Hora de llegada o cita (HH:MM): ")

    nuevo_paciente = Cliente(
        cedula=cedula,
        nombre=nombre,
        telefono=telefono,
        tipo_cliente=tipo_cliente,
        tipo_atencion=tipo_atencion,
        cantidad=cantidad,
        prioridad_atencion=prioridad,
        fecha_cita=fecha,
        hora_cita=hora
    )

    cola_asignada = cola_atencion.encolar_paciente(nuevo_paciente)

    print("\n  [OK] Paciente registrado e ingresado a la cola exitosamente!")
    print(f"      Asignado a:        {cola_asignada}")
    print(f"      Valor liquidado:   ${nuevo_paciente.valor_total:,.2f} (float)")
    print(f"      Prioridad:         {nuevo_paciente.prioridad_atencion.upper()}\n")


def cargar_datos_agenda_prueba(cola_atencion: ColaAtencion, cantidad: int = 10):
    """
    Carga datos de pacientes de prueba generados de manera aleatoria
    para probar la gestion de colas y rotacion de turnos en cada ejecucion
    """
    nombres = [
        "Ana Maria", "Luis Fernando", "Marta Lucia", "Juan Pablo",
        "Sofia Valentina", "Carlos Andres", "Maria Fernanda", "Diego Alejandro",
        "Valentina", "Andres Felipe", "Camila Andrea", "Mateo",
        "Daniela", "Sebastian", "Laura Daniela", "Santiago"
    ]
    apellidos = [
        "Perez", "Gomez", "Diaz", "Ruiz", "Cely", "Mendoza",
        "Torres", "Vargas", "Castro", "Rivera", "Lopez", "Morales",
        "Ramirez", "Herrera", "Silva", "Rojas"
    ]
    afiliaciones = ["particular", "eps", "prepagada"]
    atenciones = ["limpieza", "calzas", "extraccion", "diagnostico"]

    cargados = 0
    intentos = 0
    while cargados < cantidad and intentos < 200:
        intentos += 1
        cedula = f"10{random.randint(10000000, 99999999)}"
        if cola_atencion.existe_cedula_en_cola(cedula):
            continue

        nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"
        telefono = f"3{random.choice(['00', '10', '15', '20', '14', '18'])}{random.randint(1000000, 9999999)}"
        tipo_cliente = random.choice(afiliaciones)
        tipo_atencion = random.choice(atenciones)

        if tipo_atencion in ["calzas", "extraccion"]:
            cant_piezas = random.randint(1, 4)
        else:
            cant_piezas = 1

        # Genera tanto urgentes como normales de manera aleatoria
        prioridad = random.choice(["urgente", "normal"])
        fecha = "27-08-2026"
        hora = f"{random.randint(7, 16):02d}:{random.choice(['00', '15', '30', '45'])}"

        paciente = Cliente(
            cedula=cedula,
            nombre=nombre,
            telefono=telefono,
            tipo_cliente=tipo_cliente,
            tipo_atencion=tipo_atencion,
            cantidad=cant_piezas,
            prioridad_atencion=prioridad,
            fecha_cita=fecha,
            hora_cita=hora
        )
        cola_atencion.encolar_paciente(paciente)
        cargados += 1

    print("\n  se cargaron datos de pasientes de prueba de manera aleatoria para probar colas de atencion\n")
