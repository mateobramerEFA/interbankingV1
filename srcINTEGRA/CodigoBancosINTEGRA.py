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



cuentaBBVA = CuentaBancaria(
    numero="1930126202",
    tipo="CC",
    peso="ARS",
    banco="017",
    nombre = "BBVA_1930126202",
    abreviatura="BBVA"
)

cuentaGALICIA = CuentaBancaria(
    numero="000089983831",
    tipo="CC",
    peso="ARS",
    banco="007",
    nombre = "GALICIA_000089983831",
    abreviatura="Galicia"
)



cuentaPATAGONIA = CuentaBancaria(
    numero="04310075660600020",
    tipo="CC",
    peso="ARS",
    banco="034",
    nombre = "PATAGONIA_04310075660600020",
    abreviatura="Patagonia"
)


cuentaMACRO = CuentaBancaria(
    numero="330209419871696",
    tipo="CC",
    peso="ARS",
    banco="285",
    nombre ="MACRO_330209419871696",
    abreviatura="Macro"
)

cuentaSANTANDER = CuentaBancaria(
    numero="72700150309",
    tipo="CC",
    peso="ARS",
    banco="072",
    nombre = "SANTANDER_72700150309",
    abreviatura="Santander"
)

cuentaPROVINCIABSAS = CuentaBancaria(
    numero="51380544049",
    tipo="CC",
    peso="ARS",
    banco="014",
    nombre = "PROVINCIA_51380544049",
    abreviatura="Provincia"
)



CUENTAS = [
    cuentaBBVA,
    cuentaGALICIA,
    cuentaPATAGONIA,
    cuentaMACRO,
    cuentaSANTANDER,
    cuentaPROVINCIABSAS
]
