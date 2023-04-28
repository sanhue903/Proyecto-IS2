
const body = document.querySelector('body'),
      sidebar = body.querySelector('nav'),
      toggle = body.querySelector(".toggle"),
      /* searchBtn = body.querySelector(".search-box"), */
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");

const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

if (prefersDarkScheme.matches) {
    body.classList.toggle("dark");
    modeText.innerText = "Modo claro";
}

toggle.addEventListener("click" , () =>{
    sidebar.classList.toggle("close");
})

/* searchBtn.addEventListener("click" , () =>{
    sidebar.classList.remove("close");
}) */

modeSwitch.addEventListener("click" , () =>{
    body.classList.toggle("dark");
    
    if(body.classList.contains("dark")){
        modeText.innerText = "Modo claro";
    }else{
        modeText.innerText = "Modo oscuro";
        
    }
});

