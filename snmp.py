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
    print('Cortés Coria Luis David 2020630085')
    print('Servicios de administración de red\n')
    opciones = {
        '1': ('Agregar agente', parametros_agente),
        '2': ('Modificar agente', modificar_agente),
        '3': ('Eliminar agente', eliminar_agente),
        '4': ('Generar reporte', generar_reporte),
        '5': ('Salir', salir)
    }

    generar_menu(opciones, '5')

def salir():
    print('Saliendo')

def parametros_agente():
    print('ingrese ip')
    ip = input()
    print('ingrese puerto (161)')
    puerto = input()
    print('ingrese comunidad')
    comunidad = input()
    print('ingrese versión SNMP')
    version = input()
    agregar_agente(ip, puerto, comunidad, version)

def agregar_agente(ip, puerto, comunidad, version):
    f = open('./agentes.txt', 'a')
    f.write(ip)
    f.write('\n')
    f.write(puerto)
    f.write('\n')
    f.write(comunidad)
    f.write('\n')
    f.write(version)
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
    aux = int(posicion/4)
    print(aux)
    posicion_comunidad = posicion + aux + 2
    posicion_version = posicion + aux + 3

    print('¿Qué dato desea modificar?')
    print('1. IP')
    print('2. Comunidad')
    print('3. Version SNMP')
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
        with open('agentes.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()
            print(data)
        data[posicion_comunidad] = nueva_comunidad + '\n'
        with open('agentes.txt', 'w', encoding='utf-8') as file:
            file.writelines(data)

    elif opcion == '3':
        print('Escriba la versión deseada')
        nueva_version = input()
        with open('agentes.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()

        data[posicion_version] = nueva_version + '\n'
        with open('agentes.txt', 'w', encoding='utf-8') as file:
            file.writelines(data)

def eliminar_agente():
    datos_agente = []
    print('Escriba la ip del agente a eliminar')
    ipm = input()

    with open("agentes.txt") as archivo:
        for lineas in archivo:
           datos_agente.extend(lineas.split())

    posicion = datos_agente.index(ipm)
    aux = int(posicion/4)
    print(aux)
    posicion_ip = posicion + aux
    posicion_puerto = posicion + aux + 1
    posicion_comunidad = posicion + aux + 2
    posicion_version = posicion + aux + 3
    posicion_salto = posicion + aux + 4

    with open('agentes.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    data[posicion_ip] = ''
    data[posicion_puerto] = ''
    data[posicion_comunidad] = ''
    data[posicion_version] = ''
    data[posicion_salto] = ''
    with open('agentes.txt', 'w', encoding='utf-8') as file:
        file.writelines(data)

def generar_reporte():
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    print('Escriba la ip del agente a generar reporte')
    ip_agente = input()

    w, h = letter
    c = canvas.Canvas("Reporte.pdf", pagesize=letter)
    datos = []
    ip = []
    comunidad = []

    with open('agentes.txt') as archivo:
        for lineas in archivo:
           datos.extend(lineas.split())

    numero_agentes = int(len(datos)/3)
    interlineado = 50

    indice_ip = datos.index(ip_agente)
    comunidad = datos[indice_ip + 2]

    sistema_operativo = str(imprimirRespuesta(consultaOID(comunidad,datos[indice_ip],"1.3.6.1.2.1.1.1.0"))[0])
    subcadena1 = 'Windows'
    subcadena2 = 'Linux'

    if subcadena1 in sistema_operativo:
       # c.drawString(50, h - interlineado, "Sistema: " + subcadena1)
        text = c.beginText(50, h - interlineado + 25)
        text.setFont("Times-Roman", 12)
        text.textLines( "Cortés Coria Luis David Práctica 1" + "\n\n" +
                        "Sistema: " + subcadena1 + "\n")
        c.drawText(text)

    else:
        #c.drawString(50, h - interlineado, "Sistema: " + subcadena2)
        text = c.beginText(50, h - interlineado + 25)
        text.setFont("Times-Roman", 12)
        text.textLines("Cortés Coria Luis David Práctica 1" + "\n\n" +
                        "Sistema: " + subcadena2 + "\n")
        c.drawText(text)

    nombre_dispoitivo = str(imprimirRespuesta(consultaOID(comunidad,datos[indice_ip],"1.3.6.1.2.1.1.5.0"))[0])
    nombre_split = nombre_dispoitivo.split('=')
    informacion_contacto = str(imprimirRespuesta(consultaOID(comunidad,datos[indice_ip],"1.3.6.1.2.1.1.4.0"))[0])
    info_split = informacion_contacto.split('=')
    ubicacion = str(imprimirRespuesta(consultaOID(comunidad,datos[indice_ip],"1.3.6.1.2.1.1.6.0"))[0])
    ubicacion_split = ubicacion.split('=')
    numero_interfaces = str(imprimirRespuesta(consultaOID(comunidad,datos[indice_ip],"1.3.6.1.2.1.2.1.0"))[0])
    n_int_split = numero_interfaces.split('=')
    num_int = int(n_int_split[1])

    text = c.beginText(50, h - interlineado - 15)
    text.setFont("Times-Roman", 12)
    text.textLines("Nombre: " + nombre_split[1] + "\n" +
                   "Contacto: " + info_split[1] + "\n" +
                   "Ubicación: " + ubicacion_split[1] + "\n" +
                   "Número de interfaces: " + n_int_split[1] + "\n"
                   )
    c.drawText(text)

    aux = 0
    for i in range(5):
        sistema_operativo = str(imprimirRespuesta(consultaOID(comunidad, datos[indice_ip], "1.3.6.1.2.1.1.1.0"))[0])
        sys1 = 'Windows'
        sys2 = 'Linux'
        espacios = interlineado + 60 + (aux * 20)
        if sys1 in sistema_operativo:
            oidDesc = str(imprimirRespuesta(consultaOID(comunidad,datos[indice_ip],"1.3.6.1.2.1.2.2.1.2." + str(i + 1)))[0])
            oidDesc_split = oidDesc.split('=')
            oidStatus = str(imprimirRespuesta(consultaOID(comunidad, datos[indice_ip], "1.3.6.1.2.1.2.2.1.8." + str(i + 1)))[0])
            oidStatus_split = oidStatus.split('= ')
            int_hex_split = oidDesc_split[1].split('0x')
            byte_array = bytearray.fromhex(int_hex_split[1])
            int_hex = byte_array.decode()

            if (oidStatus_split[1] == '1'):
                text = c.beginText(50, h - espacios - 20)
                text.setFont("Times-Roman", 12)
                text.textLines(str(int_hex) + " ||| UP")
                c.drawText(text)
                aux += 1

            elif (oidStatus_split[1] == '2'):
                text = c.beginText(50, h - espacios - 20)
                text.setFont("Times-Roman", 12)
                text.textLines(str(int_hex) + " ||| DOWN")
                c.drawText(text)
                aux += 1
            else:
                print(oidStatus_split[1])
                text = c.beginText(50, h - espacios - 20)
                text.setFont("Times-Roman", 12)
                text.textLines(str(int_hex) + " ||| TESTING")
                c.drawText(text)
                aux += 1

        else:
            oidDesc = str(imprimirRespuesta(consultaOID(comunidad,datos[indice_ip],"1.3.6.1.2.1.2.2.1.2." + str(i + 1)))[0])
            oidDesc_split = oidDesc.split('=')
            oidStatus = str(imprimirRespuesta(consultaOID(comunidad, datos[indice_ip], "1.3.6.1.2.1.2.2.1.8." + str(i + 1)))[0])
            oidStatus_split = oidStatus.split('= ')

            if (oidStatus_split[1] == '1'):
                text = c.beginText(50, h - espacios - 20)
                text.setFont("Times-Roman", 12)
                text.textLines(oidStatus_split[1] + " ||| UP")
                c.drawText(text)
                aux += 1

            elif (oidStatus_split[1] == '2'):
                text = c.beginText(50, h - espacios - 20)
                text.setFont("Times-Roman", 12)
                text.textLines(oidStatus_split[1] + " ||| DOWN")
                c.drawText(text)
                aux += 1
            else:
                print(oidStatus_split[1])
                text = c.beginText(50, h - espacios - 20)
                text.setFont("Times-Roman", 12)
                text.textLines(oidStatus_split[1] + " ||| TESTING")
                c.drawText(text)
                aux += 1

        if espacios % 710 == 0:
            c.showPage()
            aux = 0
    c.showPage()
    c.save()

if __name__ == "__main__":
    menu_principal()
