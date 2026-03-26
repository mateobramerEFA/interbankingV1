class CuentaBancaria:
    def __init__(self, numero: str, tipo: str,peso: str ,banco: str, nombre: str, abreviatura : str):
        self.numero = numero
        self.tipo = tipo
        self.peso = peso      # CC, CA
        self.banco = banco    # código banco, ej: "017"
        self.nombre = nombre
        self.abreviatura = abreviatura

    def __repr__(self):
        return (
            f"CuentaBancaria("
            f"numero={self.numero}, "
            f"tipo={self.tipo}, "
            f"peso={self.peso}, "
            f"banco={self.banco})"
            f"abreviatura={self.abreviatura}"
        )


cuentaICBC = CuentaBancaria(
    numero="08760200120518",
    tipo="CC",
    peso="ARS",
    banco="015",
    nombre= "ICBC_08760200120518",
    abreviatura="ICBC"
)

cuentaBBVA = CuentaBancaria(
    numero="1930126448",
    tipo="CC",
    peso="ARS",
    banco="017",
    nombre = "BBVA_1930126448",
    abreviatura="BBVA"
)

cuentaGALICIA_1 = CuentaBancaria(
    numero="000090073835",
    tipo="CC",
    peso="ARS",
    banco="007",
    nombre = "GALICIA_000090073835",
    abreviatura="Galicia1"
)


cuentaGALICIA_2 = CuentaBancaria(
    numero="000021126941",
    tipo="CC",
    peso="ARS",
    banco="007",
    nombre = "Galicia_000021126941",
    abreviatura="Galicia2"
)


cuentaPATAGONIA = CuentaBancaria(
    numero="04310075429500020",
    tipo="CC",
    peso="ARS",
    banco="034",
    nombre = "PATAGONIA_04310075429500020",
    abreviatura="Patagonia"
)

cuentaBNA = CuentaBancaria(
    numero ="00010006157326",
    tipo ="CC",
    peso="ARS",
    banco ="011",
    nombre = "BNA_00010006157326",
    abreviatura="BNA"
)

cuentaMACRO = CuentaBancaria(
    numero="330209419872938",
    tipo="CC",
    peso="ARS",
    banco="285",
    nombre ="MACRO_330209419872938",
    abreviatura="Macro"
)

cuentaSANTANDER = CuentaBancaria(
    numero="72700090047",
    tipo="CC",
    peso="ARS",
    banco="072",
    nombre = "SANTANDER_72700090047",
    abreviatura="Santander"
)

cuentaPROVINCIABSAS = CuentaBancaria(
    numero="51380543190",
    tipo="CC",
    peso="ARS",
    banco="014",
    nombre = "PROVINCIA_51380543190",
    abreviatura="Provincia"
)

cuentaCREDICOOP = CuentaBancaria(
    numero="3090004574",
    tipo="CC",
    peso="ARS",
    banco="191",
    nombre = "CREDICOOP_3090004574",
    abreviatura="Credicoop"
)

CUENTAS = [
    cuentaICBC,
    cuentaBBVA,
    cuentaGALICIA_1,
    cuentaGALICIA_2,
    cuentaPATAGONIA,
    cuentaBNA,
    cuentaMACRO,
    cuentaSANTANDER,
    cuentaPROVINCIABSAS,
    cuentaCREDICOOP
]
