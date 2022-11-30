from CrudAgentes import parametros_agente, agregar_agente, modificar_agente, eliminar_agente
from TrendUpdate import consultas
from Notify import send_alert_attached
#from trendGraphDetection import graficar

def mostrar_menu(opciones):
    print('Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')

def leer_opcion(opciones):
    while (a := input('Opcion: ')) not in opciones:
        print('Opcion incorrecta, vuelva a intentarlo')
    return a

def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()

def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()

def menu_principal():
    print('Cortés Coria Luis David 2020630085')
    print('Servicios de administración de red\n')
    opciones = {
        '1': ('Agregar agente', parametros_agente),
        '2': ('Modificar agente', modificar_agente),
        '3': ('Eliminar agente', eliminar_agente),
        '4': ('Ejecutar analisis', consultas),
        '5': ('Salir', salir)
    }

    generar_menu(opciones, '5')

def salir():
    print('Saliendo')

if __name__ == "__main__":
    menu_principal()
