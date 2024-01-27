let subMenu = document.getElementById("subMenu");
function toggleMenu() {
    subMenu.classList.toggle("open-menu");
}

const switchElement = document.querySelector('.switch');
switchElement.addEventListener('click', () => {
    document.body.classList.toggle('dark');
})