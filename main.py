from datetime import datetime
import uuid

class Ticket:
    """
    Representa un ticket de incidencia.

    Atributos:
        id (str): Identificador único del ticket.
        cliente (Client): Cliente que crea el ticket.
        tecnico (Technician): Técnico asignado (puede ser None al inicio).
        prioridad (str): Nivel de prioridad ('alta', 'media', 'baja').
        estado (str): Estado del ticket ('pendiente', 'en proceso', 'cerrado').
        fecha_creacion (datetime): Fecha y hora de creación.
        comentarios (list of str): Historial de comentarios.
    """
    def __init__(self, cliente, prioridad='media'):
        self.id = str(uuid.uuid4())
        self.cliente = cliente
        self.tecnico = None
        self.prioridad = prioridad
        self.estado = 'pendiente'
        self.fecha_creacion = datetime.now()
        self.comentarios = []

    def agregar_comentario(self, texto):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.comentarios.append(f"[{timestamp}] {texto}")

    def __repr__(self):
        return (f"Ticket(id={self.id}, cliente={self.cliente.nombre}, "
                f"tecnico={(self.tecnico.nombre if self.tecnico else 'Sin asignar')}, "
                f"prioridad={self.prioridad}, estado={self.estado})")


class User:
    """Clase base para clientes y técnicos."""
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo


class Client(User):
    """Cliente que genera tickets."""
    pass


class Technician(User):
    """Técnico que puede ser asignado a tickets."""
    def __init__(self, nombre, correo):
        super().__init__(nombre, correo)

    def __repr__(self):
        return f"Technician(nombre={self.nombre}, correo={self.correo})"


class TicketManager:
    """
    Gestiona la colección de tickets y técnicos.

    Funcionalidades implementadas:
    - Registrar ticket.
    - Listar tickets asignados por técnico.
    - Registrar técnico.
    """
    def __init__(self):
        self.tickets = []  # Colección de Ticket
        self.tecnicos = []  # Colección de Technician

    def registrar_tecnico(self, nombre, correo):
        tecnico = Technician(nombre, correo)
        self.tecnicos.append(tecnico)
        print(f"Técnico registrado: {tecnico.nombre} ({tecnico.correo})")
        return tecnico

    def registrar_ticket(self, cliente_nombre, prioridad='media'):
        cliente = Client(cliente_nombre, '')
        ticket = Ticket(cliente, prioridad)
        self.tickets.append(ticket)
        print(f"Ticket registrado: {ticket.id} para cliente {cliente.nombre} con prioridad {prioridad}")
        return ticket

    def asignar_tecnico(self, ticket_id, tecnico_nombre):
        ticket = next((t for t in self.tickets if t.id == ticket_id), None)
        tecnico = next((tech for tech in self.tecnicos if tech.nombre == tecnico_nombre), None)
        if not ticket:
            print("Ticket no encontrado.")
            return
        if not tecnico:
            print("Técnico no encontrado.")
            return
        ticket.tecnico = tecnico
        print(f"Ticket {ticket.id} asignado a {tecnico.nombre}.")

    def listar_tickets_por_tecnico(self, tecnico_nombre):
        tecnico = next((tech for tech in self.tecnicos if tech.nombre == tecnico_nombre), None)
        if not tecnico:
            print("Técnico no encontrado.")
            return []
        asignados = [t for t in self.tickets if t.tecnico == tecnico]
        if not asignados:
            print(f"No hay tickets asignados para el técnico {tecnico.nombre}.")
        else:
            print(f"Tickets asignados a {tecnico.nombre}:")
            for t in asignados:
                print(t)
        return asignados


def mostrar_menu():
    print("\n----- Q-Track Menu -----")
    print("1. Registrar técnico")
    print("2. Registrar ticket")
    print("3. Asignar técnico a ticket")
    print("4. Listar tickets por técnico")
    print("5. Salir")


def main():
    manager = TicketManager()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            nombre = input("Nombre del técnico: ")
            correo = input("Correo del técnico: ")
            manager.registrar_tecnico(nombre, correo)
        elif opcion == '2':
            cliente = input("Nombre del cliente: ")
            prioridad = input("Prioridad (alta/media/baja): ") or 'media'
            manager.registrar_ticket(cliente, prioridad)
        elif opcion == '3':
            ticket_id = input("ID del ticket: ")
            tecnico_nombre = input("Nombre del técnico a asignar: ")
            manager.asignar_tecnico(ticket_id, tecnico_nombre)
        elif opcion == '4':
            tecnico_nombre = input("Nombre del técnico: ")
            manager.listar_tickets_por_tecnico(tecnico_nombre)
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == '__main__':
    main()
