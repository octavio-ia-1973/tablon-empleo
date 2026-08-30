# -*- coding: utf-8 -*-
"""
Descarga ofertas de las fuentes configuradas, las filtra y actualiza data/offers.json.
Se ejecuta cada día vía GitHub Actions (ver .github/workflows/update-jobs.yml),
pero también puedes lanzarlo a mano con: python scripts/fetch_jobs.py
"""
import json
import hashlib
import unicodedata
import datetime
import os
import sys

import feedparser

sys.path.insert(0, os.path.dirname(__file__))
from config import KEYWORDS, LOCATIONS, EXCLUDE_KEYWORDS, DIAS_RETENCION
from sources import SOURCES

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "offers.json")


def normalizar(texto):
    """minúsculas y sin acentos, para comparar sin líos de tildes"""
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def contiene_alguna(texto_normalizado, lista_terminos):
    return any(normalizar(t) in texto_normalizado for t in lista_terminos)


def id_oferta(url):
    return hashlib.md5(url.encode("utf-8")).hexdigest()[:16]


def cargar_existentes():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def guardar(ofertas):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(ofertas, f, ensure_ascii=False, indent=2)


def procesar_fuente_rss(fuente):
    url = fuente["rss_url"]
    if not url or url.startswith("PON_AQUI"):
        print(f"[aviso] Fuente '{fuente['name']}' sin URL configurada, se salta.")
        return []

    feed = feedparser.parse(url)
    resultados = []
    for entrada in feed.entries:
        titulo = entrada.get("title", "").strip()
        enlace = entrada.get("link", "").strip()
        descripcion = entrada.get("summary", "") or entrada.get("description", "")
        if not titulo or not enlace:
            continue
        resultados.append({
            "title": titulo,
            "url": enlace,
            "description": descripcion,
            "source": fuente["name"],
        })
    return resultados


def pasa_filtros(oferta):
    texto = normalizar(oferta["title"] + " " + oferta.get("description", ""))

    if contiene_alguna(texto, EXCLUDE_KEYWORDS):
        return False
    if not contiene_alguna(texto, KEYWORDS):
        return False
    if LOCATIONS and not contiene_alguna(texto, LOCATIONS):
        return False
    return True


def main():
    hoy = datetime.date.today().isoformat()
    existentes = cargar_existentes()
    existentes_por_id = {o["id"]: o for o in existentes}

    total_nuevas = 0

    for fuente in SOURCES:
        if fuente.get("type") == "rss":
            crudas = procesar_fuente_rss(fuente)
        elif fuente.get("type") == "custom":
            # Punto de extensión para fuentes sin RSS. Ver sources.py.
            parser = fuente.get("parser")
            crudas = parser() if callable(parser) else []
        else:
            crudas = []

        for oferta in crudas:
            if not pasa_filtros(oferta):
                continue
            oid = id_oferta(oferta["url"])
            if oid in existentes_por_id:
                continue  # ya la teníamos, no tocar su fecha de "primera vez vista"
            existentes_por_id[oid] = {
                "id": oid,
                "title": oferta["title"],
                "url": oferta["url"],
                "location_hint": oferta.get("description", "")[:200],
                "source": oferta["source"],
                "first_seen": hoy,
            }
            total_nuevas += 1

    # limpieza: quitar ofertas muy antiguas para que el JSON no crezca sin límite
    limite = (datetime.date.today() - datetime.timedelta(days=DIAS_RETENCION)).isoformat()
    todas = [o for o in existentes_por_id.values() if o["first_seen"] >= limite]
    todas.sort(key=lambda o: o["first_seen"], reverse=True)

    guardar(todas)
    print(f"Ofertas nuevas añadidas: {total_nuevas}. Total en el tablón: {len(todas)}.")


if __name__ == "__main__":
    main()
