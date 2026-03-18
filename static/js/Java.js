document.addEventListener("DOMContentLoaded", function() {
    // 1. Obtener las imágenes desde el HTML
    const imagenesJson = document.getElementById('datos-imagenes');
    if (!imagenesJson) return; // Si no estamos en el index, no hace nada
    
    const listaImagenes = JSON.parse(imagenesJson.textContent);
    const hero = document.querySelector('.hero-section');
    let indiceActual = 0;

    // 2. Función para cambiar la imagen con efecto
    function cambiarImagen() {
        // Añadimos la clase para oscurecer (definida en tu CSS)
        hero.classList.add('hero-dark');

        // Esperamos a que esté oscuro (800ms según tu CSS) para cambiar la foto
        setTimeout(() => {
            indiceActual = (indiceActual + 1) % listaImagenes.length;
            hero.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('${listaImagenes[indiceActual]}')`;
            
            // Quitamos la clase para que brille de nuevo
            hero.classList.remove('hero-dark');
        }, 800); 
    }

    // 3. Iniciar el ciclo cada 5 segundos
    if (hero && listaImagenes.length > 0) {
        setInterval(cambiarImagen, 5000);
    }
});
