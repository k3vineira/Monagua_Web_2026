const imagenesHero = [
    'img/Fondo2.jpg',
    'img/Fondo.jpg',
    'img/Fondo4.jpg'
];

let indiceActual = 0;
const heroSection = document.getElementById('home'); 

function iniciarTransicion() {

    heroSection.classList.add('hero-dark');

    setTimeout(() => {
        indiceActual = (indiceActual + 1) % imagenesHero.length;
        heroSection.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('${imagenesHero[indiceActual]}')`;
        heroSection.classList.remove('hero-dark');
    }, 800); 
}
// transición cada 15 segundos
setInterval(iniciarTransicion, 15000);
