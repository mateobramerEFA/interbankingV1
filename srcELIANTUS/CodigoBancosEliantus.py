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



cuentaGALICIA= CuentaBancaria(
    numero="000157473836",
    tipo="CC",
    peso="ARS",
    banco="007",
    nombre = "GALICIA_000157473836",
    abreviatura="Galicia"
)


cuentaMACRO_1 = CuentaBancaria(
    numero="330209424492138",
    tipo="CC",
    peso= "ARS",
    banco="285",
    nombre ="MACRO_330209424492138",
    abreviatura="Macro"
)

cuentaMACRO_2 = CuentaBancaria(
    numero="430209591789116",
    tipo="CA",
    peso="ARS",
    banco="285",
    nombre ="MACRO_430209591789116",
    abreviatura="Macro"
)

cuentaMACRO_3 = CuentaBancaria(
    numero="230209591789347",
    tipo="CA",
    peso="USD",
    banco="285",
    nombre ="MACRO_230209591789347",
    abreviatura="Macro"
)

cuentaSANTANDER_1 = CuentaBancaria(
    numero="72700153964",
    tipo="CC",
    peso="ARS",
    banco="072",
    nombre = "SANTANDER_72700090047",
    abreviatura="Santander"
)

cuentaSANTANDER_2 = CuentaBancaria(
    numero="72720156406",
    tipo="CC",
    peso="USD",
    banco="072",
    nombre = "SANTANDER_72720156406",
    abreviatura="Santander"
)

cuentaPROVINCIABSAS = CuentaBancaria(
    numero="51380606277",
    tipo="CC",
    peso="ARS",
    banco="014",
    nombre = "PROVINCIA_51380606277",
    abreviatura="Provincia"
)

cuentaSUPERVILLE_1 = CuentaBancaria(
    numero="020006085458001",
    tipo="CC",
    peso="ARS",
    banco="027",
    nombre = "SUPERVILLE_020006085458001",
    abreviatura="Superville"
)

cuentaSUPERVILLE_2 = CuentaBancaria(
    numero="020006085458002",
    tipo="CC",
    peso="USD",
    banco="027",
    nombre = "SUPERVILLE_020006085458002",
    abreviatura="Superville"
)

CUENTAS = [
    cuentaGALICIA,
    cuentaMACRO_1,
    cuentaMACRO_2,
    cuentaMACRO_3,
    cuentaSANTANDER_1,
    cuentaSANTANDER_2,
    cuentaSUPERVILLE_1,
    cuentaSUPERVILLE_2,
    cuentaPROVINCIABSAS,
]
