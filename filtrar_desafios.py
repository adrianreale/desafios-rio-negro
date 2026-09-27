from pathlib import Path
from bs4 import BeautifulSoup
import re


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARCHIVO_ORIGINAL = Path("desafios_original.html")
ARCHIVO_SALIDA = Path("index.html")

# Números de los desafíos que queremos analizar
DESAFIOS_INTERESADOS = [3,16,20,21,23,25,27,28,32,33,34,36,38,44,46,47,49,50,53,62,63,70,79,83]


# ============================================================
# LEER HTML ORIGINAL
# ============================================================

html_original = ARCHIVO_ORIGINAL.read_text(
    encoding="utf-8"
)

soup = BeautifulSoup(
    html_original,
    "html.parser"
)

tarjetas_originales = soup.select(
    "div.card"
)

print(
    f"Tarjetas encontradas en el HTML original: "
    f"{len(tarjetas_originales)}"
)


# ============================================================
# FILTRAR DESAFÍOS
# ============================================================

tarjetas_seleccionadas = []

for tarjeta in tarjetas_originales:

    titulo = tarjeta.select_one("h3")

    if not titulo:
        continue

    texto_titulo = titulo.get_text(
        " ",
        strip=True
    )

    match = re.search(
        r"Desafío\s*#(\d+)",
        texto_titulo,
        re.IGNORECASE
    )

    if not match:
        continue

    numero = int(
        match.group(1)
    )

    if numero in DESAFIOS_INTERESADOS:

        tarjetas_seleccionadas.append(
            tarjeta
        )


print(
    f"Desafíos seleccionados: "
    f"{len(tarjetas_seleccionadas)}"
)


# ============================================================
# EXTRAER OPCIONES PARA LOS FILTROS
# ============================================================

localidades = set()
sectores = set()
ejes = set()


for tarjeta in tarjetas_seleccionadas:

    # --------------------------------------------------------
    # LOCALIDAD
    # --------------------------------------------------------

    localidad_elemento = tarjeta.select_one(
        ".detail-item label:-soup-contains('Localidad')"
    )

    if localidad_elemento:

        contenedor = localidad_elemento.find_parent(
            "div",
            class_="detail-item"
        )

        if contenedor:

            divs = contenedor.find_all("div")

            if divs:

                valor = divs[-1].get_text(
                    " ",
                    strip=True
                )

                if valor:
                    localidades.add(valor)


    # --------------------------------------------------------
    # SECTOR / RUBRO
    # --------------------------------------------------------

    sector_elemento = tarjeta.select_one(
        ".detail-item label:-soup-contains('Sector / Rubro')"
    )

    if sector_elemento:

        contenedor = sector_elemento.find_parent(
            "div",
            class_="detail-item"
        )

        if contenedor:

            divs = contenedor.find_all("div")

            if divs:

                valor = divs[-1].get_text(
                    " ",
                    strip=True
                )

                if valor:
                    sectores.add(valor)


    # --------------------------------------------------------
    # EJES
    # --------------------------------------------------------

    for elemento in tarjeta.select(
        ".badge-eje"
    ):

        valor = elemento.get_text(
            " ",
            strip=True
        )

        if valor:
            ejes.add(valor)


# ============================================================
# CREAR HTML
# ============================================================

html = """

<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Mis desafíos - Río Negro</title>


<style>


/* ============================================================
   GENERAL
   ============================================================ */

* {
    box-sizing: border-box;
}


body {

    margin: 0;

    padding: 30px;

    font-family: Arial, sans-serif;

    background: #f5f5f5;

    color: #222;

}


h1 {

    margin-top: 0;

    margin-bottom: 8px;

}


.subtitulo {

    margin-top: 0;

    margin-bottom: 25px;

    color: #666;

}


/* ============================================================
   PANEL DE FILTROS
   ============================================================ */

.panel-filtros {

    background: white;

    border-radius: 10px;

    padding: 20px;

    margin-bottom: 25px;

    box-shadow:
        0 2px 8px rgba(0,0,0,0.08);

}


.filtros {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(180px, 1fr));

    gap: 15px;

}


.campo-filtro label {

    display: block;

    margin-bottom: 6px;

    font-size: 0.85rem;

    font-weight: bold;

    color: #555;

}


.campo-filtro input,
.campo-filtro select {

    width: 100%;

    padding: 9px;

    border: 1px solid #ccc;

    border-radius: 6px;

    background: white;

    font-size: 0.95rem;

}


.campo-filtro input:focus,
.campo-filtro select:focus {

    outline: none;

    border-color: #777;

}


/* ============================================================
   ACCIONES
   ============================================================ */

.acciones-filtros {

    margin-top: 18px;

    display: flex;

    align-items: center;

    gap: 10px;

    flex-wrap: wrap;

}


#resultado-info {

    margin-right: auto;

    font-weight: bold;

    color: #555;

}


.btn-accion {

    padding: 9px 14px;

    border: none;

    border-radius: 6px;

    color: white;

    cursor: pointer;

    font-size: 0.9rem;

}


#btn-exportar {

    background: #356859;

}


#btn-exportar:hover {

    background: #284f43;

}


#btn-importar {

    background: #52759b;

}


#btn-importar:hover {

    background: #3f5e7d;

}


#btn-limpiar {

    background: #555;

}


#btn-limpiar:hover {

    background: #333;

}


#archivo-importar {

    display: none;

}


/* ============================================================
   TARJETAS
   ============================================================ */

#contenedor-tarjetas {

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(420px, 1fr));

    gap: 20px;

}


.card {

    background: white;

    border-radius: 10px;

    padding: 20px;

    box-shadow:
        0 2px 8px rgba(0,0,0,0.08);

}


.card[style*="display: none"] {

    display: none !important;

}


/* ============================================================
   ENCABEZADO
   ============================================================ */

.titulo-row {

    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    gap: 10px;

}


.titulo-row h3 {

    margin-top: 0;

    margin-bottom: 10px;

}


.card-org {

    margin-bottom: 12px;

    font-weight: bold;

    color: #555;

}


.card-desc {

    margin-bottom: 15px;

    line-height: 1.5;

}


/* ============================================================
   META
   ============================================================ */

.meta {

    display: flex;

    flex-wrap: wrap;

    gap: 8px 15px;

    align-items: center;

    margin-bottom: 15px;

    font-size: 0.9rem;

    color: #555;

}


.badge-eje {

    display: inline-block;

    padding: 4px 8px;

    margin: 2px;

    border-radius: 12px;

    background: #eee;

    color: #444;

    font-size: 0.8rem;

}


/* ============================================================
   BOTÓN FICHA
   ============================================================ */

.btn-ver-mas {

    border: none;

    background: none;

    color: #444;

    font-weight: bold;

    cursor: pointer;

    padding: 4px;

}


.btn-ver-mas:hover {

    text-decoration: underline;

}


/* ============================================================
   MI INTERÉS
   ============================================================ */

.mi-interes {

    margin-top: 15px;

    padding-top: 15px;

    border-top: 1px solid #eee;

}


.mi-interes label {

    display: block;

    margin-bottom: 6px;

    font-size: 0.85rem;

    font-weight: bold;

    color: #555;

}


.selector-interes {

    width: 100%;

    padding: 9px;

    border: 1px solid #ccc;

    border-radius: 7px;

    background: white;

    font-size: 0.95rem;

}


/* ============================================================
   MIS NOTAS
   ============================================================ */

.mis-notas {

    margin-top: 15px;

}


.mis-notas label {

    display: block;

    margin-bottom: 6px;

    font-size: 0.85rem;

    font-weight: bold;

    color: #555;

}


.campo-notas {

    width: 100%;

    min-height: 110px;

    padding: 10px;

    resize: vertical;

    border: 1px solid #ccc;

    border-radius: 7px;

    font-family: inherit;

    font-size: 0.95rem;

    line-height: 1.4;

}


.campo-notas:focus {

    outline: none;

    border-color: #777;

}


/* ============================================================
   FICHA COMPLETA
   ============================================================ */

.detail-box-inline {

    margin-top: 20px;

    padding-top: 20px;

    border-top: 1px solid #ddd;

}


.detail-grid {

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));

    gap: 15px;

    margin-bottom: 20px;

}


.detail-item label {

    display: block;

    margin-bottom: 4px;

    font-size: 0.8rem;

    font-weight: bold;

    color: #777;

}


.detail-item div {

    line-height: 1.4;

}


/* ============================================================
   MENSAJE DE ESTADO
   ============================================================ */

.mensaje-estado {

    position: fixed;

    bottom: 20px;

    right: 20px;

    padding: 10px 15px;

    background: #333;

    color: white;

    border-radius: 7px;

    font-size: 0.9rem;

    opacity: 0;

    transform: translateY(10px);

    pointer-events: none;

    transition:
        opacity 0.2s ease,
        transform 0.2s ease;

}


.mensaje-estado.visible {

    opacity: 1;

    transform: translateY(0);

}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1100px) {

    .filtros {

        grid-template-columns:
            repeat(2, minmax(180px, 1fr));

    }

}


@media (max-width: 700px) {

    body {

        padding: 15px;

    }


    .filtros {

        grid-template-columns: 1fr;

    }


    #contenedor-tarjetas {

        grid-template-columns: 1fr;

    }


    .acciones-filtros {

        align-items: stretch;

    }


    #resultado-info {

        width: 100%;

        margin-right: 0;

    }


    .btn-accion {

        flex: 1;

    }

}


</style>

</head>


<body>


<h1>
    Mis desafíos — Río Negro
</h1>


<p class="subtitulo">
    Exploración y clasificación personal de los desafíos disponibles.
</p>


<!-- ============================================================
     PANEL DE FILTROS
     ============================================================ -->

<div class="panel-filtros">


    <div class="filtros">


        <div class="campo-filtro">

            <label for="buscador">
                Buscar
            </label>

            <input
                type="text"
                id="buscador"
                placeholder="Buscar por palabra..."
            >

        </div>


        <div class="campo-filtro">

            <label for="filtro-localidad">
                Localidad
            </label>

            <select id="filtro-localidad">

                <option value="">
                    Todas
                </option>

"""


# ============================================================
# OPCIONES DE LOCALIDAD
# ============================================================

for localidad in sorted(localidades):

    html += f"""
                <option value="{localidad}">
                    {localidad}
                </option>
"""


html += """

            </select>

        </div>


        <div class="campo-filtro">

            <label for="filtro-sector">
                Sector / Rubro
            </label>

            <select id="filtro-sector">

                <option value="">
                    Todos
                </option>

"""


# ============================================================
# OPCIONES DE SECTOR
# ============================================================

for sector in sorted(sectores):

    html += f"""
                <option value="{sector}">
                    {sector}
                </option>
"""


html += """

            </select>

        </div>


        <div class="campo-filtro">

            <label for="filtro-eje">
                Eje
            </label>

            <select id="filtro-eje">

                <option value="">
                    Todos
                </option>

"""


# ============================================================
# OPCIONES DE EJE
# ============================================================

for eje in sorted(ejes):

    html += f"""
                <option value="{eje}">
                    {eje}
                </option>
"""


html += """

            </select>

        </div>


        <div class="campo-filtro">

            <label for="filtro-interes">
                Mi interés
            </label>

            <select id="filtro-interes">

                <option value="">
                    Todos
                </option>

                <option value="sin-clasificar">
                    Sin clasificar
                </option>

                <option value="explorar">
                    🔎 Para explorar
                </option>

                <option value="interesa">
                    ⭐ Me interesa
                </option>

                <option value="prioritario">
                    🎯 Prioritario
                </option>

            </select>

        </div>


        <div class="campo-filtro">

            <label for="filtro-notas">
                Mis notas
            </label>

            <select id="filtro-notas">

                <option value="">
                    Todos
                </option>

                <option value="con-notas">
                    📝 Con notas
                </option>

                <option value="sin-notas">
                    Sin notas
                </option>

            </select>

        </div>


    </div>


    <div class="acciones-filtros">


        <span id="resultado-info"></span>


        <button
            id="btn-exportar"
            class="btn-accion"
        >
            💾 Exportar mi análisis
        </button>


        <button
            id="btn-importar"
            class="btn-accion"
        >
            📂 Importar mi análisis
        </button>


        <input
            type="file"
            id="archivo-importar"
            accept=".json,application/json"
        >


        <button
            id="btn-limpiar"
            class="btn-accion"
        >
            Limpiar filtros
        </button>


    </div>


</div>


<!-- ============================================================
     MENSAJE DE ESTADO
     ============================================================ -->

<div
    id="mensaje-estado"
    class="mensaje-estado"
></div>


<!-- ============================================================
     TARJETAS
     ============================================================ -->

<div id="contenedor-tarjetas">
"""


# ============================================================
# INSERTAR TARJETAS
# ============================================================

for tarjeta in tarjetas_seleccionadas:


    # --------------------------------------------------------
    # NÚMERO
    # --------------------------------------------------------

    titulo = tarjeta.select_one("h3")

    texto_titulo = titulo.get_text(
        " ",
        strip=True
    )

    match = re.search(
        r"Desafío\s*#(\d+)",
        texto_titulo,
        re.IGNORECASE
    )

    numero = (
        match.group(1)
        if match
        else ""
    )


    # --------------------------------------------------------
    # TEXTO DE BÚSQUEDA
    # --------------------------------------------------------

    texto_busqueda = tarjeta.get_text(
        " ",
        strip=True
    ).lower()


    # --------------------------------------------------------
    # LOCALIDAD
    # --------------------------------------------------------

    localidad = ""

    localidad_elemento = tarjeta.select_one(
        ".detail-item label:-soup-contains('Localidad')"
    )

    if localidad_elemento:

        contenedor = localidad_elemento.find_parent(
            "div",
            class_="detail-item"
        )

        if contenedor:

            divs = contenedor.find_all(
                "div"
            )

            if divs:

                localidad = divs[-1].get_text(
                    " ",
                    strip=True
                )


    # --------------------------------------------------------
    # SECTOR
    # --------------------------------------------------------

    sector = ""

    sector_elemento = tarjeta.select_one(
        ".detail-item label:-soup-contains('Sector / Rubro')"
    )

    if sector_elemento:

        contenedor = sector_elemento.find_parent(
            "div",
            class_="detail-item"
        )

        if contenedor:

            divs = contenedor.find_all(
                "div"
            )

            if divs:

                sector = divs[-1].get_text(
                    " ",
                    strip=True
                )


    # --------------------------------------------------------
    # EJES
    # --------------------------------------------------------

    ejes_tarjeta = [

        elemento.get_text(
            " ",
            strip=True
        )

        for elemento in tarjeta.select(
            ".badge-eje"
        )

    ]


    # --------------------------------------------------------
    # ATRIBUTOS DATA
    # --------------------------------------------------------

    tarjeta["data-numero"] = numero

    tarjeta["data-busqueda"] = (
        texto_busqueda
    )

    tarjeta["data-localidad"] = (
        localidad
    )

    tarjeta["data-sector"] = (
        sector
    )

    tarjeta["data-ejes"] = "||".join(
        ejes_tarjeta
    )


    # ========================================================
    # QUITAR "ABIERTO"
    # ========================================================

    badge_estado = tarjeta.select_one(
        ".badge-estado"
    )

    if badge_estado:

        badge_estado.decompose()


    # ========================================================
    # OCULTAR FICHA
    # ========================================================

    detalle = tarjeta.select_one(
        ".detail-box-inline"
    )

    if detalle:

        detalle["style"] = (
            "display: none;"
        )


    # ========================================================
    # BOTÓN FICHA
    # ========================================================

    boton_ver_mas = tarjeta.select_one(
        ".btn-ver-mas"
    )

    if boton_ver_mas:

        boton_ver_mas.string = (
            "Ver ficha completa ↓"
        )


    # ========================================================
    # BLOQUE MI INTERÉS
    # ========================================================

    bloque_interes = BeautifulSoup(
        """
        <div class="mi-interes">

            <label>
                Mi interés:
            </label>

            <select class="selector-interes">

                <option value="sin-clasificar">
                    Sin clasificar
                </option>

                <option value="explorar">
                    🔎 Para explorar
                </option>

                <option value="interesa">
                    ⭐ Me interesa
                </option>

                <option value="prioritario">
                    🎯 Prioritario
                </option>

            </select>

        </div>
        """,
        "html.parser"
    )


    # ========================================================
    # BLOQUE MIS NOTAS
    # ========================================================

    bloque_notas = BeautifulSoup(
        """
        <div class="mis-notas">

            <label>
                Mis notas:
            </label>

            <textarea
                class="campo-notas"
                placeholder="Escribir aquí mis observaciones..."
            ></textarea>

        </div>
        """,
        "html.parser"
    )


    # ========================================================
    # INSERTAR BLOQUES
    # ========================================================

    if detalle:

        detalle.insert_before(
            bloque_notas
        )

        detalle.insert_before(
            bloque_interes
        )

    else:

        tarjeta.append(
            bloque_interes
        )

        tarjeta.append(
            bloque_notas
        )


    html += str(
        tarjeta
    )


html += """

</div>


<script>


// ============================================================
// ELEMENTOS
// ============================================================

const tarjetas =
    document.querySelectorAll(".card");


const buscador =
    document.getElementById(
        "buscador"
    );


const filtroLocalidad =
    document.getElementById(
        "filtro-localidad"
    );


const filtroSector =
    document.getElementById(
        "filtro-sector"
    );


const filtroEje =
    document.getElementById(
        "filtro-eje"
    );


const filtroInteres =
    document.getElementById(
        "filtro-interes"
    );


const filtroNotas =
    document.getElementById(
        "filtro-notas"
    );


const resultadoInfo =
    document.getElementById(
        "resultado-info"
    );


const btnLimpiar =
    document.getElementById(
        "btn-limpiar"
    );


const btnExportar =
    document.getElementById(
        "btn-exportar"
    );


const btnImportar =
    document.getElementById(
        "btn-importar"
    );


const archivoImportar =
    document.getElementById(
        "archivo-importar"
    );


const mensajeEstado =
    document.getElementById(
        "mensaje-estado"
    );


// ============================================================
// CLAVES DE LOCAL STORAGE
// ============================================================

const CLAVE_INTERESES =
    "desafios-rio-negro-intereses";


const CLAVE_NOTAS =
    "desafios-rio-negro-notas";


// ============================================================
// MENSAJES
// ============================================================

let temporizadorMensaje;


function mostrarMensaje(
    mensaje
) {

    mensajeEstado.textContent =
        mensaje;

    mensajeEstado.classList.add(
        "visible"
    );


    clearTimeout(
        temporizadorMensaje
    );


    temporizadorMensaje =
        setTimeout(
            () => {

                mensajeEstado.classList.remove(
                    "visible"
                );

            },
            2500
        );

}


// ============================================================
// INTERESES
// ============================================================

function obtenerIntereses() {

    try {

        return JSON.parse(
            localStorage.getItem(
                CLAVE_INTERESES
            )
        ) || {};

    } catch (error) {

        return {};

    }

}


function guardarIntereses(
    intereses
) {

    localStorage.setItem(
        CLAVE_INTERESES,
        JSON.stringify(
            intereses
        )
    );

}


function cargarIntereses() {

    const intereses =
        obtenerIntereses();


    tarjetas.forEach(
        tarjeta => {

            const numero =
                tarjeta.dataset.numero;


            const selector =
                tarjeta.querySelector(
                    ".selector-interes"
                );


            if (
                selector &&
                intereses[numero]
            ) {

                selector.value =
                    intereses[numero];

            }

        }
    );

}


// ============================================================
// NOTAS
// ============================================================

function obtenerNotas() {

    try {

        return JSON.parse(
            localStorage.getItem(
                CLAVE_NOTAS
            )
        ) || {};

    } catch (error) {

        return {};

    }

}


function guardarNotas(
    notas
) {

    localStorage.setItem(
        CLAVE_NOTAS,
        JSON.stringify(
            notas
        )
    );

}


function cargarNotas() {

    const notas =
        obtenerNotas();


    tarjetas.forEach(
        tarjeta => {

            const numero =
                tarjeta.dataset.numero;


            const textarea =
                tarjeta.querySelector(
                    ".campo-notas"
                );


            if (
                textarea &&
                notas[numero]
            ) {

                textarea.value =
                    notas[numero];

            }

        }
    );

}


// ============================================================
// APLICAR FILTROS
// ============================================================

function aplicarFiltros() {

    const texto =
        buscador.value
            .toLowerCase()
            .trim();


    const localidad =
        filtroLocalidad.value;


    const sector =
        filtroSector.value;


    const eje =
        filtroEje.value;


    const interes =
        filtroInteres.value;


    const filtroNota =
        filtroNotas.value;


    let visibles = 0;


    tarjetas.forEach(
        tarjeta => {


            // ------------------------------------------------
            // TEXTO
            // ------------------------------------------------

            const coincideTexto =
                !texto ||
                tarjeta.dataset.busqueda.includes(
                    texto
                );


            // ------------------------------------------------
            // LOCALIDAD
            // ------------------------------------------------

            const coincideLocalidad =
                !localidad ||
                tarjeta.dataset.localidad ===
                    localidad;


            // ------------------------------------------------
            // SECTOR
            // ------------------------------------------------

            const coincideSector =
                !sector ||
                tarjeta.dataset.sector ===
                    sector;


            // ------------------------------------------------
            // EJE
            // ------------------------------------------------

            const listaEjes =
                tarjeta.dataset.ejes
                    ? tarjeta.dataset.ejes.split(
                        "||"
                    )
                    : [];


            const coincideEje =
                !eje ||
                listaEjes.includes(
                    eje
                );


            // ------------------------------------------------
            // INTERÉS
            // ------------------------------------------------

            const selector =
                tarjeta.querySelector(
                    ".selector-interes"
                );


            const estadoInteres =
                selector
                    ? selector.value
                    : "sin-clasificar";


            const coincideInteres =
                !interes ||
                estadoInteres ===
                    interes;


            // ------------------------------------------------
            // NOTAS
            // ------------------------------------------------

            const textarea =
                tarjeta.querySelector(
                    ".campo-notas"
                );


            const tieneNotas =
                textarea &&
                textarea.value.trim().length > 0;


            let coincideNotas = true;


            if (
                filtroNota ===
                "con-notas"
            ) {

                coincideNotas =
                    tieneNotas;

            }


            if (
                filtroNota ===
                "sin-notas"
            ) {

                coincideNotas =
                    !tieneNotas;

            }


            // ------------------------------------------------
            // RESULTADO
            // ------------------------------------------------

            const mostrar =
                coincideTexto &&
                coincideLocalidad &&
                coincideSector &&
                coincideEje &&
                coincideInteres &&
                coincideNotas;


            tarjeta.style.display =
                mostrar
                    ? ""
                    : "none";


            if (mostrar) {

                visibles++;

            }

        }
    );


    resultadoInfo.textContent =
        `${visibles} desafío${
            visibles === 1
                ? ""
                : "s"
        } mostrado${
            visibles === 1
                ? ""
                : "s"
        }`;

}


// ============================================================
// EVENTOS DE FILTROS
// ============================================================

buscador.addEventListener(
    "input",
    aplicarFiltros
);


filtroLocalidad.addEventListener(
    "change",
    aplicarFiltros
);


filtroSector.addEventListener(
    "change",
    aplicarFiltros
);


filtroEje.addEventListener(
    "change",
    aplicarFiltros
);


filtroInteres.addEventListener(
    "change",
    aplicarFiltros
);


filtroNotas.addEventListener(
    "change",
    aplicarFiltros
);


// ============================================================
// LIMPIAR FILTROS
// ============================================================

btnLimpiar.addEventListener(
    "click",
    () => {

        buscador.value = "";

        filtroLocalidad.value = "";

        filtroSector.value = "";

        filtroEje.value = "";

        filtroInteres.value = "";

        filtroNotas.value = "";

        aplicarFiltros();

    }
);


// ============================================================
// CAMBIAR INTERÉS
// ============================================================

document
    .querySelectorAll(
        ".selector-interes"
    )
    .forEach(
        selector => {

            selector.addEventListener(
                "change",
                () => {

                    const tarjeta =
                        selector.closest(
                            ".card"
                        );


                    const numero =
                        tarjeta.dataset.numero;


                    const intereses =
                        obtenerIntereses();


                    intereses[numero] =
                        selector.value;


                    guardarIntereses(
                        intereses
                    );


                    aplicarFiltros();


                    mostrarMensaje(
                        "Clasificación guardada"
                    );

                }
            );

        }
    );


// ============================================================
// GUARDAR NOTAS AUTOMÁTICAMENTE
// ============================================================

document
    .querySelectorAll(
        ".campo-notas"
    )
    .forEach(
        textarea => {

            textarea.addEventListener(
                "input",
                () => {

                    const tarjeta =
                        textarea.closest(
                            ".card"
                        );


                    const numero =
                        tarjeta.dataset.numero;


                    const notas =
                        obtenerNotas();


                    const contenido =
                        textarea.value;


                    if (
                        contenido.trim()
                    ) {

                        notas[numero] =
                            contenido;

                    } else {

                        delete notas[numero];

                    }


                    guardarNotas(
                        notas
                    );


                    aplicarFiltros();

                }
            );

        }
    );


// ============================================================
// ABRIR / CERRAR FICHA
// ============================================================

document
    .querySelectorAll(
        ".btn-ver-mas"
    )
    .forEach(
        boton => {

            boton.addEventListener(
                "click",
                () => {

                    const tarjeta =
                        boton.closest(
                            ".card"
                        );


                    const detalle =
                        tarjeta.querySelector(
                            ".detail-box-inline"
                        );


                    if (!detalle) {
                        return;
                    }


                    const estaOculto =
                        detalle.style.display ===
                            "none";


                    if (estaOculto) {

                        detalle.style.display =
                            "block";


                        boton.textContent =
                            "Cerrar ficha ↑";

                    } else {

                        detalle.style.display =
                            "none";


                        boton.textContent =
                            "Ver ficha completa ↓";

                    }

                }
            );

        }
    );


// ============================================================
// EXPORTAR ANÁLISIS
// ============================================================

btnExportar.addEventListener(
    "click",
    () => {

        const intereses =
            obtenerIntereses();


        const notas =
            obtenerNotas();


        const desafios = {};


        tarjetas.forEach(
            tarjeta => {

                const numero =
                    tarjeta.dataset.numero;


                const interes =
                    intereses[numero] ||
                    "sin-clasificar";


                const nota =
                    notas[numero] ||
                    "";


                // Solamente exportamos
                // desafíos que tengan
                // alguna información personal.

                if (
                    interes !==
                        "sin-clasificar" ||
                    nota.trim() !== ""
                ) {

                    desafios[numero] = {

                        interes:
                            interes,

                        notas:
                            nota

                    };

                }

            }
        );


        const datos = {

            version: 1,

            proyecto:
                "Desafíos Río Negro",

            fecha_exportacion:
                new Date().toISOString(),

            desafios:
                desafios

        };


        const contenido =
            JSON.stringify(
                datos,
                null,
                2
            );


        const blob =
            new Blob(
                [contenido],
                {
                    type:
                        "application/json"
                }
            );


        const url =
            URL.createObjectURL(
                blob
            );


        const enlace =
            document.createElement(
                "a"
            );


        const fecha =
            new Date()
                .toISOString()
                .slice(
                    0,
                    10
                );


        enlace.href =
            url;


        enlace.download =
            `analisis-desafios-rio-negro-${fecha}.json`;


        document.body.appendChild(
            enlace
        );


        enlace.click();


        enlace.remove();


        URL.revokeObjectURL(
            url
        );


        mostrarMensaje(
            "Análisis exportado correctamente"
        );

    }
);


// ============================================================
// IMPORTAR ANÁLISIS
// ============================================================

btnImportar.addEventListener(
    "click",
    () => {

        archivoImportar.click();

    }
);


archivoImportar.addEventListener(
    "change",
    event => {

        const archivo =
            event.target.files[0];


        if (!archivo) {
            return;
        }


        const lector =
            new FileReader();


        lector.onload =
            function () {

                try {

                    const datos =
                        JSON.parse(
                            lector.result
                        );


                    if (
                        !datos ||
                        typeof datos !==
                            "object" ||
                        !datos.desafios ||
                        typeof datos.desafios !==
                            "object"
                    ) {

                        throw new Error(
                            "Formato inválido"
                        );

                    }


                    const intereses =
                        {};


                    const notas =
                        {};


                    Object.entries(
                        datos.desafios
                    ).forEach(
                        ([numero, desafio]) => {

                            if (
                                !desafio ||
                                typeof desafio !==
                                    "object"
                            ) {
                                return;
                            }


                            const interes =
                                desafio.interes;


                            const nota =
                                desafio.notas;


                            if (
                                [
                                    "sin-clasificar",
                                    "explorar",
                                    "interesa",
                                    "prioritario"
                                ].includes(
                                    interes
                                )
                            ) {

                                if (
                                    interes !==
                                        "sin-clasificar"
                                ) {

                                    intereses[
                                        numero
                                    ] =
                                        interes;

                                }

                            }


                            if (
                                typeof nota ===
                                    "string" &&
                                nota.trim() !== ""
                            ) {

                                notas[numero] =
                                    nota;

                            }

                        }
                    );


                    // Reemplazamos los datos
                    // actuales por los importados.

                    localStorage.setItem(
                        CLAVE_INTERESES,
                        JSON.stringify(
                            intereses
                        )
                    );


                    localStorage.setItem(
                        CLAVE_NOTAS,
                        JSON.stringify(
                            notas
                        )
                    );


                    cargarIntereses();

                    cargarNotas();

                    aplicarFiltros();


                    mostrarMensaje(
                        "Análisis importado correctamente"
                    );


                } catch (error) {

                    alert(
                        "No se pudo importar el archivo. " +
                        "Verificá que sea un archivo " +
                        "de análisis válido."
                    );

                }

            };


        lector.readAsText(
            archivo
        );


        // Permite volver a seleccionar
        // el mismo archivo posteriormente.

        event.target.value = "";

    }
);


// ============================================================
// INICIALIZACIÓN
// ============================================================

cargarIntereses();

cargarNotas();

aplicarFiltros();


</script>


</body>

</html>
"""


# ============================================================
# GUARDAR ARCHIVO
# ============================================================

ARCHIVO_SALIDA.write_text(
    html,
    encoding="utf-8"
)


print(
    f"Archivo generado correctamente: "
    f"{ARCHIVO_SALIDA}"
)