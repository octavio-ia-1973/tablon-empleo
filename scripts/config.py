# -*- coding: utf-8 -*-
"""
Configuración de filtrado de ofertas.
Edita estas listas para ajustar qué ofertas se guardan.
"""

# Se busca cada palabra en el título + descripción de la oferta (sin distinguir mayúsculas/acentos)
KEYWORDS = [
    "comedor escolar", "monitor de comedor", "monitora de comedor",
    "monitor comedor", "monitora comedor",
    "extraescolar", "extraescolares", "monitor de tiempo libre",
    "monitora de tiempo libre", "actividades extraescolares",
    "canguro", "niñera", "niñero", "cuidado de niños", "cuidado de ninos",
    "au pair", "conciliacion familiar",
    "dependiente", "dependienta", "cajero", "cajera",
    "reponedor", "reponedora", "auxiliar de tienda", "auxiliar de venta",
    "supermercado", "hipermercado",
    "camarero", "camarera", "ayudante de cocina", "ayudante de camarero",
]

# La oferta debe mencionar alguno de estos municipios/zonas (o no mencionar ninguna ubicación conflictiva)
LOCATIONS = [
    "elche", "elx", "san vicente del raspeig", "sant vicent del raspeig",
    "alicante", "alacant",
]

# Si el título o descripción contiene alguna de estas palabras, la oferta se descarta
# aunque coincida con KEYWORDS (para quitar ruido: comerciales, puestos que piden
# titulación superior, jornadas incompatibles, etc.)
EXCLUDE_KEYWORDS = [
    "comercial de seguros", "teleoperador", "teleoperadora",
    "ingeniero", "ingeniera", "grado superior", "licenciatura",
    "master", "experiencia minima de 3 años", "experiencia mínima de 3 años",
]

# Cuántos días hacia atrás conservar ofertas en data/offers.json (limpieza automática)
DIAS_RETENCION = 120
