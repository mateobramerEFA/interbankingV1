import http.client
import json
import os


def obtener_extractos_Eliantus(cuenta, token, desde, hasta, limit=10000):
    """
    Obtiene extractos de la cuenta usando variables de entorno en Azure
    """
    client_id    = os.environ.get("ELIANTUS_CLIENTID")
    customer_id  = os.environ.get("ELIANTUS_USER")

    if not client_id or not customer_id:
        raise ValueError("No se encontraron las variables de entorno necesarias para Eliantus")

    conn = http.client.HTTPSConnection("api-gw.interbanking.com.ar")
    headers = {
        "client_id": client_id,
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }

    path = (
        f"/api/prod/v1/accounts/{cuenta.numero}/statements"
        f"?account-type={cuenta.tipo}&bank-number={cuenta.banco}&currency={cuenta.peso}"
        f"&customer-id={customer_id}&date-since={desde}&date-until={hasta}&limit={limit}"
    )

    conn.request("GET", path, headers=headers)
    data = json.loads(conn.getresponse().read().decode("utf-8"))
    return data.get("general_data", {}), data.get("statements", [])