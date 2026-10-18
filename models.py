import re
from datetime import datetime

class ClienteDuplicadoException(Exception):
    pass

class DatosInvalidosException(Exception):
    pass

class Cliente:
    def __init__(self, nombre_completo, dni_ruc, correo, fecha_nacimiento, id_cliente=None):
        self.__id_cliente = id_cliente
        self.__nombre_completo = nombre_completo
        self.__dni_ruc = dni_ruc
        self.__correo = correo
        self.__fecha_nacimiento = fecha_nacimiento

    @property
    def id_cliente(self):
        return self.__id_cliente

    @property
    def nombre_completo(self):
        return self.__nombre_completo

    @property
    def dni_ruc(self):
        return self.__dni_ruc

    @property
    def correo(self):
        return self.__correo

    @property
    def fecha_nacimiento(self):
        return self.__fecha_nacimiento
    @id_cliente.setter
    def id_cliente(self, valor):
        self.__id_cliente = valor

    # --- MÉTODO DE VALIDACIÓN ---
    def validar_datos(self):
        if not self.__dni_ruc or not self.__dni_ruc.strip():
            raise DatosInvalidosException("El DNI/RUC no puede estar vacío.")

        if not self.__nombre_completo or not self.__nombre_completo.strip():
            raise DatosInvalidosException("El nombre completo no puede estar vacío.")

        patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not self.__correo or not re.match(patron_correo, self.__correo):
            raise DatosInvalidosException("El formato del correo electrónico es incorrecto.")

        if not self.__fecha_nacimiento:
            raise DatosInvalidosException("Debe ingresar una fecha de nacimiento.")

        try:
            fecha_nac = datetime.strptime(self.__fecha_nacimiento, '%Y-%m-%d')
            hoy = datetime.now()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            
            if edad < 0 or edad > 120:
                raise DatosInvalidosException("La fecha de nacimiento no representa una edad válida.")
        except ValueError:
            raise DatosInvalidosException("Formato de fecha inválido. Debe ser AAAA-MM-DD.")
