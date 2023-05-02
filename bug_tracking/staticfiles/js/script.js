const body = document.querySelector('body');
const sidebar = body.querySelector('nav');
const toggle = body.querySelector(".toggle");
const modeSwitch = body.querySelector(".toggle-switch");
const modeText = body.querySelector(".mode-text");

const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

if (prefersDarkScheme.matches) {
    document.body.classList.toggle("dark", localStorage.getItem('darkmode') === 'true');
    modeText.innerText = "Modo claro";
}


/* searchBtn.addEventListener("click" , () =>{
    sidebar.classList.remove("close");
}) */

modeSwitch.addEventListener("click" , () =>{

    const WasDarkMode = localStorage.getItem('darkmode') === 'true'
    localStorage.setItem('darkmode', !WasDarkMode);
    const element = document.body;
    element.classList.toggle("dark");

});

function onload(){
    document.body.classList.toggle("dark", localStorage.getItem('darkmode') === 'true');
}
