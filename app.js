// ---------------------------------------------------------------------------
// Tablón de ofertas — lógica de frontend
// ---------------------------------------------------------------------------

firebase.initializeApp(FIREBASE_CONFIG);
const db = firebase.firestore();
const ESTADO_REF = db.collection("family_state").doc("main");

const hoyISO = () => new Date().toISOString().slice(0, 10);
const diasAtras = (n) => {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString().slice(0, 10);
};

let OFERTAS = [];
let DESCARTADAS = new Set();
let FECHA_UMBRAL_ULTIMA_VISITA = null; // fecha (distinta de hoy) de la visita anterior

async function cargarEstado() {
  const snap = await ESTADO_REF.get();
  const hoy = hoyISO();

  if (!snap.exists) {
    // Primera vez que se abre la web nunca: no hay "última visita", así que
    // "nuevas desde tu última visita" equivale a "todas".
    await ESTADO_REF.set({ lastVisitDate: hoy, dismissed: [] });
    FECHA_UMBRAL_ULTIMA_VISITA = null;
    DESCARTADAS = new Set();
    return;
  }

  const datos = snap.data();
  DESCARTADAS = new Set(datos.dismissed || []);

  if (datos.lastVisitDate === hoy) {
    // Ya se abrió hoy antes: el umbral sigue siendo el de la última vez
    // que se abrió en un día distinto (guardado en localStorage al vuelo).
    FECHA_UMBRAL_ULTIMA_VISITA = localStorage.getItem("umbral_dia_distinto") || null;
  } else {
    // Primera apertura de hoy: el umbral pasa a ser la fecha de la visita anterior.
    FECHA_UMBRAL_ULTIMA_VISITA = datos.lastVisitDate;
    localStorage.setItem("umbral_dia_distinto", datos.lastVisitDate);
    await ESTADO_REF.update({ lastVisitDate: hoy });
  }
}

async function descartarOferta(id) {
  DESCARTADAS.add(id);
  await ESTADO_REF.update({
    dismissed: firebase.firestore.FieldValue.arrayUnion(id),
  });
}

function aplicarFiltro(valorFiltro) {
  const hoy = hoyISO();
  let minFecha = null;

  if (valorFiltro === "today") minFecha = hoy;
  else if (valorFiltro === "week") minFecha = diasAtras(7);
  else if (valorFiltro === "month") minFecha = diasAtras(30);
  else if (valorFiltro === "since_last") minFecha = FECHA_UMBRAL_ULTIMA_VISITA;
  // "all" -> minFecha queda null, no se filtra por fecha

  return OFERTAS
    .filter((o) => !DESCARTADAS.has(o.id))
    .filter((o) => !minFecha || o.first_seen >= minFecha)
    .sort((a, b) => b.first_seen.localeCompare(a.first_seen));
}

function render(ofertas) {
  const contenedor = document.getElementById("tablon");
  const plantilla = document.getElementById("tarjeta-template");
  const hoy = hoyISO();

  contenedor.innerHTML = "";

  if (ofertas.length === 0) {
    contenedor.innerHTML = '<p class="vacio">No hay ofertas que mostrar con este filtro. Prueba a elegir "Todas".</p>';
  }

  for (const oferta of ofertas) {
    const nodo = plantilla.content.cloneNode(true);
    const tarjeta = nodo.querySelector(".tarjeta");

    if (oferta.first_seen === hoy) tarjeta.classList.add("es-nueva");

    nodo.querySelector(".tarjeta-titulo").textContent = oferta.title;
    nodo.querySelector(".tarjeta-meta").textContent = `${oferta.source} · vista el ${oferta.first_seen}`;
    nodo.querySelector(".tarjeta-desc").textContent = oferta.location_hint || "";

    const enlace = nodo.querySelector(".btn-ver");
    enlace.href = oferta.url;

    const btnDescartar = nodo.querySelector(".btn-descartar");
    btnDescartar.addEventListener("click", async () => {
      await descartarOferta(oferta.id);
      actualizarVista();
    });

    contenedor.appendChild(nodo);
  }

  document.getElementById("contador").textContent = `${ofertas.length} oferta(s)`;
}

function actualizarVista() {
  const filtro = document.getElementById("filtro").value;
  render(aplicarFiltro(filtro));
}

async function iniciar() {
  try {
    const resp = await fetch("data/offers.json", { cache: "no-store" });
    OFERTAS = await resp.json();
  } catch (e) {
    document.getElementById("tablon").innerHTML =
      '<p class="vacio">No se pudieron cargar las ofertas (data/offers.json).</p>';
    return;
  }

  await cargarEstado();

  document.getElementById("filtro").addEventListener("change", actualizarVista);
  document.getElementById("fecha-datos").textContent =
    OFERTAS.length ? OFERTAS[0].first_seen : "sin datos todavía";

  actualizarVista();
}

iniciar();
