document.addEventListener("DOMContentLoaded", function() {
    // 1. Obtener las imágenes desde el HTML
    const imagenesJson = document.getElementById('datos-imagenes');
    if (!imagenesJson) return; // Si no estamos en el index, no hace nada
    
    const listaImagenes = JSON.parse(imagenesJson.textContent);
    const hero = document.querySelector('.hero-section');
    let indiceActual = 0;

    // 2. Función para cambiar la imagen con efecto
    function cambiarImagen() {
        // 1. Incrementamos el índice primero para evitar repetir la imagen actual
        indiceActual = (indiceActual + 1) % listaImagenes.length;

        // 2. Iniciamos el oscurecimiento
        hero.classList.add('hero-dark');

        // 3. Esperamos a que la transición de oscuridad termine (800ms)
        setTimeout(() => {
            // 4. Cambiamos la imagen de fondo
            hero.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('${listaImagenes[indiceActual]}')`;

            // 5. Quitamos la clase para que vuelva a iluminarse
            hero.classList.remove('hero-dark');
        }, 800); 
    }

    // 3. Iniciar el ciclo cada 15 segundos
    if (hero && listaImagenes.length > 0) {
        setInterval(cambiarImagen, 15000);
    }
});
