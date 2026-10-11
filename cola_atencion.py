# ===================================================================
# cola_atencion.py - Gestion de Colas de Atencion con Prioridad
# ===================================================================
# Actividad Individual N° 2 - Colas de Atencion
# Programacion 2 - Universidad de Manizales (2026-2)
# Estudiante: Nicolas David Solano Plazas
# Codigo: 106202524246
# ===================================================================

from collections import deque
from cliente import Cliente


class ColaAtencion:
    """
    Administra la llegada y atencion de pacientes en el consultorio
    utilizando estructuras de datos lineales tipo Cola

    Implementa gestion de prioridades con rotacion balanceada
    para evitar el problema de inanicion de los pacientes normales
    """

    def __init__(self, nombre_consultorio: str = "Consultorio Odontologico"):
        self.nombre_consultorio = nombre_consultorio
        # Cola para pacientes con prioridad urgente (extracciones urgentes, dolores agudos)
        self.cola_urgencias = deque()
        # Cola para pacientes con prioridad normal (citas regulares de agenda)
        self.cola_general = deque()
        # Historial de pacientes que ya fueron atendidos en el dia
        self.historial_atendidos = []
        # Contador de turnos urgentes atendidos para rotar con pacientes normales
        self.urgentes_consecutivos = 0

    def encolar_paciente(self, cliente: Cliente) -> str:
        """
        Inserta un paciente al final de la cola correspondiente
        Retorna el nombre de la cola a la que fue asignado
        """
        if cliente.es_urgente():
            self.cola_urgencias.append(cliente)
            return "Cola de Urgencias"
        else:
            self.cola_general.append(cliente)
            return "Cola General"

    def esta_vacia(self) -> bool:
        """Verifica si no hay pacientes en ninguna de las dos colas"""
        return len(self.cola_urgencias) == 0 and len(self.cola_general) == 0

    def existe_cedula_en_cola(self, cedula: str) -> bool:
        """Verifica si un documento ya se encuentra esperando turno"""
        for c in self.cola_urgencias:
            if c.cedula == cedula:
                return True
        for c in self.cola_general:
            if c.cedula == cedula:
                return True
        return False

    def consultar_siguiente_en_cola(self):
        """
        Operacion PEEK: consulta quien es el siguiente paciente a ser llamado
        segun la politica de prioridad balanceada, sin sacarlo de la cola
        """
        if self.esta_vacia():
            return None, "Vacia"

        # Si hay pacientes en ambas colas, aplicamos la regla de balance
        if self.cola_urgencias and self.cola_general:
            if self.urgentes_consecutivos < 2:
                return self.cola_urgencias[0], "Urgencias"
            else:
                return self.cola_general[0], "General"
        elif self.cola_urgencias:
            return self.cola_urgencias[0], "Urgencias"
        else:
            return self.cola_general[0], "General"

    def atender_siguiente_paciente(self):
        """
        Operacion DEQUEUE: atiende y retira al siguiente paciente de la cola
        Aplica politica de prioridad:
          - Da preferencia a urgencias
          - Al atender 2 urgentes seguidos, da paso a 1 normal si hay en espera,
            evitando que los pacientes regulares sufran inanicion
        """
        if self.esta_vacia():
            return None, "No hay pacientes esperando en la cola."

        paciente_atendido = None
        tipo_cola = ""

        # Caso 1: Hay pacientes en ambas colas
        if self.cola_urgencias and self.cola_general:
            if self.urgentes_consecutivos < 2:
                paciente_atendido = self.cola_urgencias.popleft()
                tipo_cola = "Cola de Urgencias"
                self.urgentes_consecutivos += 1
            else:
                paciente_atendido = self.cola_general.popleft()
                tipo_cola = "Cola General (Turno balanceado)"
                self.urgentes_consecutivos = 0

        # Caso 2: Solo hay urgentes
        elif self.cola_urgencias:
            paciente_atendido = self.cola_urgencias.popleft()
            tipo_cola = "Cola de Urgencias"
            self.urgentes_consecutivos = 0

        # Caso 3: Solo hay generales
        else:
            paciente_atendido = self.cola_general.popleft()
            tipo_cola = "Cola General"
            self.urgentes_consecutivos = 0

        # Registrar en el historial de atenciones de la jornada
        self.historial_atendidos.append(paciente_atendido)
        return paciente_atendido, tipo_cola

    def _calcular_anchos(self, lista_clientes):
        """Calcula el ancho necesario para imprimir las tablas alineadas"""
        ancho_num = max(2, len(str(len(lista_clientes))))
        ancho_ced = len("Documento")
        ancho_nom = len("Nombre")
        ancho_tel = len("Telefono")
        ancho_cli = len("Afiliacion")
        ancho_ate = len("Atencion")
        ancho_can = len("Cant")
        ancho_pri = len("Prioridad")
        ancho_fec = len("Fecha")
        ancho_hor = len("Hora")
        ancho_tot = len("Valor Total")

        for c in lista_clientes:
            ancho_ced = max(ancho_ced, len(c.cedula))
            ancho_nom = max(ancho_nom, len(c.nombre))
            ancho_tel = max(ancho_tel, len(c.telefono))
            ancho_cli = max(ancho_cli, len(c.tipo_cliente))
            ancho_ate = max(ancho_ate, len(c.tipo_atencion))
            ancho_can = max(ancho_can, len(str(c.cantidad)))
            ancho_pri = max(ancho_pri, len(c.prioridad_atencion))
            ancho_fec = max(ancho_fec, len(c.fecha_cita))
            ancho_hor = max(ancho_hor, len(c.hora_cita))
            ancho_tot = max(ancho_tot, len(f"${c.valor_total:,.2f}"))

        return (ancho_num, ancho_ced, ancho_nom, ancho_tel,
                ancho_cli, ancho_ate, ancho_can, ancho_pri,
                ancho_fec, ancho_hor, ancho_tot)

    def _imprimir_tabla_pacientes(self, lista_clientes, titulo: str):
        """Imprime una tabla de pacientes con diseno claro y ordenado"""
        if len(lista_clientes) == 0:
            print(f"\n  [!] {titulo}: No hay pacientes para mostrar.\n")
            return

        anchos = self._calcular_anchos(lista_clientes)
        (a_num, a_ced, a_nom, a_tel, a_cli, a_ate, a_can, a_pri, a_fec, a_hor, a_tot) = anchos

        encabezado = (
            f"  {'#':<{a_num}} | "
            f"{'Documento':<{a_ced}} | "
            f"{'Nombre':<{a_nom}} | "
            f"{'Telefono':<{a_tel}} | "
            f"{'Afiliacion':<{a_cli}} | "
            f"{'Atencion':<{a_ate}} | "
            f"{'Cant':<{a_can}} | "
            f"{'Prioridad':<{a_pri}} | "
            f"{'Fecha':<{a_fec}} | "
            f"{'Hora':<{a_hor}} | "
            f"{'Valor Total':>{a_tot}}"
        )

        ancho_linea = len(encabezado) + 2
        separador = "  " + "-" * (ancho_linea - 2)

        print()
        print("  " + "=" * (ancho_linea - 2))
        print(f"  {titulo}")
        print("  " + "=" * (ancho_linea - 2))
        print(encabezado)
        print(separador)

        for i, c in enumerate(lista_clientes, 1):
            fila = (
                f"  {i:<{a_num}} | "
                f"{c.cedula:<{a_ced}} | "
                f"{c.nombre:<{a_nom}} | "
                f"{c.telefono:<{a_tel}} | "
                f"{c.tipo_cliente.capitalize():<{a_cli}} | "
                f"{c.tipo_atencion.capitalize():<{a_ate}} | "
                f"{c.cantidad:<{a_can}} | "
                f"{c.prioridad_atencion.capitalize():<{a_pri}} | "
                f"{c.fecha_cita:<{a_fec}} | "
                f"{c.hora_cita:<{a_hor}} | "
                f"{'$' + f'{c.valor_total:,.2f}':>{a_tot}}"
            )
            print(fila)

        print("  " + "=" * (ancho_linea - 2))
        print(f"  Total listados: {len(lista_clientes)} pacientes\n")

    def consultar_todas_las_colas(self):
        """
        Recorre y muestra todas las colas de atencion activas, totalizando
        el numero de pacientes pendientes y el monto total en dinero acumulado
        """
        print("\n" + "=" * 70)
        print(f"   ESTADO GENERAL DE LAS COLAS DE ATENCION - {self.nombre_consultorio.upper()}")
        print("=" * 70)

        # 1 Cola de Urgencias
        total_urgentes = len(self.cola_urgencias)
        monto_urgentes = float(sum(c.valor_total for c in self.cola_urgencias))
        self._imprimir_tabla_pacientes(list(self.cola_urgencias), "1. COLA DE URGENCIAS (ALTA PRIORIDAD)")
        print(f"  --> Pacientes en espera (Urgencias): {total_urgentes}")
        print(f"  --> Monto acumulado (Urgencias):     ${monto_urgentes:,.2f}")

        # 2 Cola General
        total_general = len(self.cola_general)
        monto_general = float(sum(c.valor_total for c in self.cola_general))
        self._imprimir_tabla_pacientes(list(self.cola_general), "2. COLA GENERAL (CITAS REGULARES)")
        print(f"  --> Pacientes en espera (General):   {total_general}")
        print(f"  --> Monto acumulado (General):       ${monto_general:,.2f}")

        # Resumen consolidado
        total_global = total_urgentes + total_general
        monto_global = float(monto_urgentes + monto_general)

        print("\n  " + "-" * 66)
        print("  RESUMEN TOTAL DE LA SALA DE ESPERA")
        print("  " + "-" * 66)
        print(f"  Total de pacientes pendientes en clinica: {total_global}")
        print(f"  Total monto transacciones pendientes:     ${monto_global:,.2f}")
        print("  " + "=" * 66 + "\n")

    def mostrar_historial_atendidos(self):
        """Muestra el reporte de los pacientes atendidos en el transcurso del dia"""
        print("\n" + "=" * 70)
        print("   REPORTE DE PACIENTES ATENDIDOS EN LA JORNADA")
        print("=" * 70)

        if len(self.historial_atendidos) == 0:
            print("\n  Todavia no se han atendido pacientes hoy.\n")
            return

        self._imprimir_tabla_pacientes(self.historial_atendidos, "PACIENTES YA ATENDIDOS")
        recaudo_total = float(sum(c.valor_total for c in self.historial_atendidos))
        print(f"  Total de pacientes atendidos hoy: {len(self.historial_atendidos)}")
        print(f"  Recaudo total efectivo del dia:   ${recaudo_total:,.2f}\n")
