"""
SNMPv1
++++++
Send SNMP GET request using the following options:
  * with SNMPv1, community 'comunidadASR'
  * over IPv4/UDP
  * to an Agent at localhost
  * for two instances of SNMPv2-MIB::sysDescr.0 MIB object,
Functionally similar to:
| $ snmpget -v1 -c comunidadASR localhost 1.3.6.1.2.1.1.1.0
"""#
import os

from pysnmp.hlapi import *
import datetime

def consultaOID(comunidad,ip,OID):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(comunidad, mpModel=0),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(OID))
        )
    return iterator

def imprimirRespuesta(iterator):

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
            return varBinds


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
    opciones = {
        '1': ('Agregar agente', parametros_agente),
        '2': ('Modificar agente', modificar_agente),
        '3': ('Eliminar agente', eliminar_agente),
        '4': ('Generar reporte', generar_reporte),
        '5': ('Salir', salir)
    }

    generar_menu(opciones, '5')

def main():
    comunidad=input()
    ip=input()
    OIDS=['1.3.6.1.2.1.2.2.1.12.1', '1.3.6.1.2.1.4.9.0','1.3.6.1.2.1.4.9.0','1.3.6.1.2.1.6.11.0','1.3.6.1.2.1.7.2.0']
    for oid in OIDS:
        imprimirRespuesta(consultaOID(comunidad,ip,oid))

def salir():
    print('Saliendo')

def parametros_agente():
    print('ingrese ip')
    ip = input()
    print('ingrese puerto (161)')
    puerto = input()
    print('ingrese comunidad')
    comunidad = input()
    agregar_agente(ip, puerto, comunidad)

def agregar_agente(ip, puerto, comunidad):
    f = open('./agentes.txt', 'a')
    f.write(ip)
    f.write('\n')
    f.write(puerto)
    f.write('\n')
    f.write(comunidad)
    f.write('\n\n')
    f.close()

def modificar_agente():
    datos_agente = []
    print('Escriba la ip del agente a modificar')
    ipm = input()

    with open("agentes.txt") as archivo:
        for lineas in archivo:
           datos_agente.extend(lineas.split())

    posicion = datos_agente.index(ipm)
    comunidad = str(datos_agente[posicion+2])

    print('¿Qué dato desea modificar?')
    print('1. IP')
    print('2. Comunidad')
    opcion = input()

    if opcion == '1':
        print('Escriba la nueva IP')
        nueva_ip = input()

        with open("agentes.txt", "rt") as file:
            x = file.read()

        with open("agentes.txt", "wt") as file:
            x = x.replace(ipm, nueva_ip)
            file.write(x)

    elif opcion == '2':
        print('Escriba la nueva comunidad')
        nueva_comunidad = input()
        with open("agentes.txt", "rt") as file:
            x = file.read()

        with open("agentes.txt", "wt") as file:
            x = x.replace(comunidad, nueva_comunidad)
            file.write(x)

def eliminar_agente():
    print('Escriba la ip del agente a eliminar')
    ipd = input()

    archivo = open('agentes.txt', 'r')

    for x in archivo:
        xf = x.replace()

def generar_reporte():
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    w, h = letter
    c = canvas.Canvas("Reporte.pdf", pagesize=letter)
    datos = []
    ip = []
    comunidad = []

    with open('agentes.txt') as archivo:
        for lineas in archivo:
           datos.extend(lineas.split())

    for n in range(0, len(datos), 3):
        ip.append(datos[n])

    for i in range(2, len(datos), 3):
        comunidad.append(datos[i])

    numero_agentes = int(len(datos)/3)
    interlineado = 50
    for k in range(numero_agentes):
        sistema_operativo = str(imprimirRespuesta(consultaOID(comunidad[k],ip[k],"1.3.6.1.2.1.1.1.0"))[0])
        subcadena1 = 'Windows'
        subcadena2 = 'Linux'

        if subcadena1 in sistema_operativo:
            c.drawString(50, h - interlineado, "Sistema: " + subcadena1)

        else:
            c.drawString(50, h - interlineado, "Sistema: " + subcadena2)

        nombre_dispoitivo = str(imprimirRespuesta(consultaOID(comunidad[k],ip[k],"1.3.6.1.2.1.1.5.0"))[0])
        informacion_contacto = str(imprimirRespuesta(consultaOID(comunidad[k],ip[k],"1.3.6.1.2.1.1.4.0"))[0])
        ubicacion = str(imprimirRespuesta(consultaOID(comunidad[k],ip[k],"1.3.6.1.2.1.1.6.0"))[0])
        numero_interfaces = str(imprimirRespuesta(consultaOID(comunidad[k],ip[k],"1.3.6.1.2.1.2.1.0"))[0])
        estado_administrativo = str(imprimirRespuesta(consultaOID(comunidad[k],ip[k],'1.3.6.1.2.1.2.2.1.8.1'))[0])

        c.drawString(50, h - (interlineado+20), "Nombre: " + nombre_dispoitivo)
        c.drawString(50, h - (interlineado+40), "Contacto: " + informacion_contacto)
        c.drawString(50, h - (interlineado+60), "Ubicación: " + ubicacion)
        c.drawString(50, h - (interlineado+80), "Número de interfaces: " + numero_interfaces)
        c.drawString(50, h - (interlineado+100), "Estado administrativo: " + estado_administrativo)

        nuevo_interlineado = interlineado+140
        interlineado = nuevo_interlineado

    c.showPage()
    c.save()

if __name__ == "__main__":
    #main()
    menu_principal()