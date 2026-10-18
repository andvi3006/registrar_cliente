function cambiarPestana(idSeccion) {
    const secciones = document.querySelectorAll('.dashboard-section');
    secciones.forEach(sec => sec.classList.remove('active'));

    const botones = document.querySelectorAll('.nav-btn');
    botones.forEach(btn => btn.classList.remove('active'));

    const seccionActiva = document.getElementById(idSeccion);
    if (seccionActiva) {
        seccionActiva.classList.add('active');
    }

    if (event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    }
}

function filtrarTabla() {
    const input = document.getElementById('input-busqueda');
    const filtro = input.value.toLowerCase();
    const tabla = document.getElementById('tabla-clientes');
    if (!tabla) return;
    
    const filas = tabla.getElementsByTagName('tr');
    for (let i = 1; i < filas.length; i++) {
        const celdaNombre = filas[i].getElementsByTagName('td')[1];
        const celdaDNI = filas[i].getElementsByTagName('td')[2];

        if (celdaNombre || celdaDNI) {
            const textoNombre = celdaNombre.textContent || celdaNombre.innerText;
            const textoDNI = celdaDNI.textContent || celdaDNI.innerText;

            if (textoNombre.toLowerCase().indexOf(filtro) > -1 || textoDNI.toLowerCase().indexOf(filtro) > -1) {
                filas[i].style.display = "";
            } else {
                filas[i].style.display = "none";
            }
        }
    }
}
