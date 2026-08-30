# Tablón de ofertas

Web que cada día recoge ofertas de empleo nuevas (comedores, extraescolares,
tiendas, cuidado de niños...) en Elche, San Vicente del Raspeig y Alicante,
y las muestra en un tablón con filtros por fecha y opción de descartar.

Todo gratis: GitHub (alojamiento + tarea diaria automática) + Firebase (recordar
qué se ha visto/descartado entre el móvil y el ordenador).

## 1. Crear el repositorio en GitHub

1. Entra en github.com y crea una cuenta si no tienes (gratis).
2. Crea un repositorio nuevo, público, por ejemplo `tablon-empleo`.
3. Sube todos los archivos de esta carpeta a ese repositorio (puedes arrastrarlos
   directamente en la web de GitHub con "Add file > Upload files", o usar `git`).

## 2. Activar GitHub Pages

1. En el repositorio: Settings > Pages.
2. En "Source" elige "Deploy from a branch", rama `main`, carpeta `/ (root)`.
3. Guarda. En un par de minutos tu web estará en
   `https://TU_USUARIO.github.io/tablon-empleo/`.

## 3. Activar la actualización diaria (GitHub Actions)

No hay que hacer nada más: el archivo `.github/workflows/update-jobs.yml` ya
está en el repo y GitHub lo ejecutará solo cada día a las 06:00 UTC. Puedes
cambiar la hora editando la línea `cron` de ese archivo.

Para lanzarlo manualmente una vez (por ejemplo, para probar): pestaña
"Actions" del repositorio > "Actualizar ofertas de empleo" > "Run workflow".

## 4. Configurar las fuentes de ofertas (InfoJobs y Talent.com)

**InfoJobs:**
1. Ve a infojobs.net y haz una búsqueda con las palabras y ubicación que
   interesen (o deja la búsqueda amplia, el filtrado ya lo hace el script).
2. En los resultados busca el icono/enlace de RSS de esa búsqueda.
3. Copia esa URL y pégala en `scripts/sources.py`, sustituyendo
   `PON_AQUI_TU_URL_RSS_DE_INFOJOBS`.

**Talent.com:** mismo proceso, buscando el enlace RSS de tu búsqueda guardada
en talent.com, y pegándolo donde pone `PON_AQUI_TU_URL_RSS_DE_TALENT`.

Puedes añadir más búsquedas (por ejemplo una por cada tipo de trabajo) como
entradas adicionales en la lista `SOURCES`.

## 5. Crear el proyecto de Firebase (gratis)

Esto es lo que permite que "última visita" y "ofertas descartadas" se
recuerden entre el móvil y el ordenador.

1. Ve a console.firebase.google.com y crea un proyecto nuevo (gratis).
2. En el menú lateral: Build > Firestore Database > Create database.
   Elige modo "producción" y la región más cercana (europe-west).
3. Ve a la pestaña "Rules" de Firestore y pon esto (solo permite leer/escribir
   ese único documento de estado, nada más):

   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /family_state/main {
         allow read, write: if true;
       }
     }
   }
   ```

   Esto es intencionadamente simple para un proyecto familiar sin datos
   sensibles (solo guarda IDs de ofertas descartadas y una fecha). No metas
   aquí ningún dato personal.

4. En Configuración del proyecto (icono de engranaje) > "Tus apps" > añade
   una app web (icono `</>`). Te dará un objeto de configuración con
   `apiKey`, `projectId`, etc.
5. Copia esos valores en `firebase-config.js`, sustituyendo los
   `PON_AQUI_...`.
6. Sube el `firebase-config.js` actualizado al repositorio.

## 6. Usar la web

Abre `https://TU_USUARIO.github.io/tablon-empleo/` desde el móvil o el
ordenador. Por defecto se muestran las ofertas nuevas desde la última vez
que se abrió en un día distinto. El desplegable permite ver solo las de hoy,
de la última semana, del último mes, o todas. El botón "Descartar" oculta
una oferta para siempre (en todos los dispositivos).

## Añadir más sitios de empleo en el futuro

- Si el sitio nuevo tiene RSS: añade una entrada a `SOURCES` en
  `scripts/sources.py` con su URL RSS. No hace falta tocar nada más.
- Si no tiene RSS: escribe una función en un nuevo archivo
  `scripts/parsers.py` que descargue y extraiga las ofertas a mano, y
  regístrala en `sources.py` con `"type": "custom"`. Revisa los comentarios
  de `sources.py` y `fetch_jobs.py` para el formato exacto esperado.

## Ajustar qué ofertas se guardan

Edita `scripts/config.py`:
- `KEYWORDS`: términos que debe contener el título/descripción.
- `LOCATIONS`: municipios/zonas válidos.
- `EXCLUDE_KEYWORDS`: términos que descartan la oferta aunque coincida.
