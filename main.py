# ===================================================================
# main.py - Punto de Entrada del Sistema de Colas Odontologico
# ===================================================================
# Actividad Individual N° 2 - Colas de Atencion
# Programacion 2 - Universidad de Manizales (2026-2)
# Estudiante: Nicolas David Solano Plazas
# Codigo: 106202524246
# ===================================================================

from cola_atencion import ColaAtencion
from utilidades import (
    registrar_paciente_por_consola,
    cargar_datos_agenda_prueba
)


def mostrar_menu():
    """Imprime el menu de opciones del sistema de colas"""
    print("=" * 64)
    print("        CONSULTORIO ODONTOLOGICO - GESTION DE COLAS")
    print("=" * 64)
    print("    1. Registrar y encolar nuevo paciente (Enqueue)")
    print("    2. Atender siguiente paciente en turno (Dequeue)")
    print("    3. Consultar proximo paciente en ser llamado (Peek)")
    print("    4. Consultar todas las colas (Pacientes y montos)")
    print("    5. Cargar agenda de pacientes de prueba")
    print("    6. Ver reporte de pacientes atendidos hoy")
    print("    7. Salir")
    print("=" * 64)


def mostrar_ticket_atencion(paciente, tipo_cola: str):
    """Muestra un comprobante detallado de la atencion odontologica"""
    valor_cita, valor_atencion = paciente.obtener_desglose()
    ancho = 48

    print()
    print("  +" + "-" * ancho + "+")
    print("  |" + "  TICKET DE ATENCION EN CONSULTORIO".center(ancho) + "|")
    print("  +" + "-" * ancho + "+")
    print(f"  |  Origen:        {tipo_cola:<30} |")
    print(f"  |  Documento:     {paciente.cedula:<30} |")
    print(f"  |  Paciente:      {paciente.nombre:<30} |")
    print(f"  |  Telefono:      {paciente.telefono:<30} |")
    print(f"  |  Afiliacion:    {paciente.tipo_cliente.capitalize():<30} |")
    print(f"  |  Tratamiento:   {paciente.tipo_atencion.capitalize():<30} |")
    print(f"  |  Piezas:        {str(paciente.cantidad):<30} |")
    print(f"  |  Prioridad:     {paciente.prioridad_atencion.upper():<30} |")
    print(f"  |  Hora cita:     {paciente.hora_cita:<30} |")
    print("  +" + "-" * ancho + "+")
    print(f"  |  Valor consulta base:   ${valor_cita:>14,.2f}   |")
    print(f"  |  Valor por pieza:       ${valor_atencion:>14,.2f}   |")
    print(f"  |  Procedimiento x {paciente.cantidad} pzs:  ${valor_atencion * paciente.cantidad:>14,.2f}   |")
    print("  |" + "-" * ancho + "|")
    print(f"  |  TOTAL A COBRAR (FLOAT): ${paciente.valor_total:>14,.2f}   |")
    print("  +" + "-" * ancho + "+\n")


def menu_principal():
    """Funcion principal que ejecuta el ciclo de la aplicacion"""
    sistema_colas = ColaAtencion("Consultorio Odontologico Especializado")

    ancho_marco = 68
    print()
    print("  " + "*" * ancho_marco)
    print("  *" + " " * (ancho_marco - 2) + "*")
    print("  *  " + "SISTEMA DE GESTION DE COLAS DE ATENCION CLINICA ODONTOLOGICA".ljust(ancho_marco - 6) + "  *")
    print("  *  " + "Programacion 2 - Universidad de Manizales (2026-2)".ljust(ancho_marco - 6) + "  *")
    print("  *  " + "Estudiante: Nicolas David Solano Plazas".ljust(ancho_marco - 6) + "  *")
    print("  *  " + "Codigo: 106202524246".ljust(ancho_marco - 6) + "  *")
    print("  *" + " " * (ancho_marco - 2) + "*")
    print("  " + "*" * ancho_marco)
    print()

    # Preguntamos si desea cargar datos de prueba al iniciar para comodidad
    print("¿Cargar datos de prueba?")
    opc_inicio = input("  (S = Si, cualquier otra tecla = Empezar vacio): ").strip().upper()
    if opc_inicio == "S":
        cargar_datos_agenda_prueba(sistema_colas)

    while True:
        mostrar_menu()
        opcion = input("    Seleccione una opcion (1-7): ").strip()

        if opcion == "1":
            registrar_paciente_por_consola(sistema_colas)

        elif opcion == "2":
            print("\n  [Procesando] Llamando al siguiente paciente en turno...")
            paciente, origen = sistema_colas.atender_siguiente_paciente()
            if paciente is None:
                print(f"  [!] {origen}\n")
            else:
                print(f"  [OK] Paciente llamado: {paciente.nombre} desde {origen}")
                mostrar_ticket_atencion(paciente, origen)

        elif opcion == "3":
            paciente, tipo_cola = sistema_colas.consultar_siguiente_en_cola()
            if paciente is None:
                print("\n  [!] La sala de espera esta vacia. No hay pacientes en cola.\n")
            else:
                print("\n  " + "-" * 50)
                print("  PROXIMO PACIENTE EN TURNO (PEEK)")
                print("  " + "-" * 50)
                print(f"  Paciente:   {paciente.nombre}")
                print(f"  Documento:  {paciente.cedula}")
                print(f"  Cola:       {tipo_cola}")
                print(f"  Tratamiento:{paciente.tipo_atencion.capitalize()}")
                print(f"  Prioridad:  {paciente.prioridad_atencion.upper()}")
                print(f"  Hora:       {paciente.hora_cita}")
                print(f"  Valor:      ${paciente.valor_total:,.2f}")
                print("  " + "-" * 50 + "\n")

        elif opcion == "4":
            sistema_colas.consultar_todas_las_colas()

        elif opcion == "5":
            cargar_datos_agenda_prueba(sistema_colas)

        elif opcion == "6":
            sistema_colas.mostrar_historial_atendidos()

        elif opcion == "7":
            print("\n  Cerrando sistema de colas. Que tenga un buen dia.\n")
            break

        else:
            print("\n  [Error] Opcion invalida. Ingrese un numero del 1 al 7.\n")


if __name__ == "__main__":
    menu_principal()
