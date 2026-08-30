# -*- coding: utf-8 -*-
"""
Fuentes de ofertas de empleo.

Cómo añadir una fuente nueva que tenga RSS:
    1. Crea la búsqueda en la web del portal (con tus palabras clave y ubicación).
    2. Busca el botón/enlace de "RSS" o "suscribirse" de esa búsqueda y copia la URL.
    3. Añade un diccionario a SOURCES con 'name' y 'rss_url'.

Cómo añadir una fuente sin RSS (requiere más trabajo):
    1. Escribe una función en scripts/parsers.py que reciba el HTML/JSON de la página
       y devuelva una lista de dicts con las claves: title, url, location, published (opcional).
    2. Añade aquí un diccionario con 'type': 'custom' y 'parser': nombre_de_la_funcion.
    3. Regístrala también en fetch_jobs.py (ver el bloque "fuentes custom").
"""

SOURCES = [
    {
        "name": "InfoJobs",
        "type": "rss",
        # Sustituye por la URL RSS de tu búsqueda guardada en infojobs.net
        "rss_url": "PON_AQUI_TU_URL_RSS_DE_INFOJOBS",
    },
    {
        "name": "Talent.com",
        "type": "rss",
        # Sustituye por la URL RSS de tu búsqueda guardada en talent.com
        "rss_url": "PON_AQUI_TU_URL_RSS_DE_TALENT",
    },
]
