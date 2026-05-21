import os
import time
import requests

TOKEN_URL = "https://auth.interbanking.com.ar/cas/oidc/accessToken"
SCOPE = "info-financiera"
TTL = 7200  # seconds

_cache: dict = {}  # key → (token, expires_at)


def _pedir_token(client_id, client_secret, url_servicio):
    cache_key = client_id
    cached = _cache.get(cache_key)
    if cached and time.time() < cached[1]:
        return cached[0]

    r = requests.post(
        f"{TOKEN_URL}?scope={SCOPE}",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "service": url_servicio,
        },
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        },
        timeout=30,
    )

    if not r.ok:
        raise Exception(f"Error al pedir token: {r.text}")

    token = r.json()["access_token"]
    _cache[cache_key] = (token, time.time() + TTL)
    return token


def obtener_token(empresa: str):
    """
    Obtiene token usando variables de entorno en Azure.
    Variables esperadas:
        {EMPRESA}_CLIENTID
        {EMPRESA}_SECRET
        {EMPRESA}_USER  -> customer_id
        {EMPRESA}_URL_SERVICIO
    """
    
    
    empresa_upper = empresa.upper()
    client_id = os.environ.get(f"{empresa_upper}_CLIENTID")
    client_secret = os.environ.get(f"{empresa_upper}_SECRET")
    customer_id = os.environ.get(f"{empresa_upper}_USER")
    url_servicio = os.environ.get(f"{empresa_upper}_URL_SERVICIO")

    if not all([client_id, client_secret, customer_id, url_servicio]):
        raise ValueError(f"Faltan variables de entorno para {empresa}")

    # Devolvemos también customer_id si la función de movimientos lo necesita
    token = _pedir_token(client_id, client_secret, url_servicio)
    return token, customer_id