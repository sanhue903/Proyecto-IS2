const body = document.querySelector('body');
const sidebar = body.querySelector('nav');
const toggle = body.querySelector(".toggle");
const modeSwitch = body.querySelector(".toggle-switch");
const modeText = body.querySelector(".mode-text");

let isDarkMode = localStorage.getItem("isDarkMode");

if (isDarkMode === null) {
  isDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
} else {
  isDarkMode = isDarkMode === "true";
}

setMode(isDarkMode);

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});

modeSwitch.addEventListener("click", () => {
  isDarkMode = !isDarkMode;
  setMode(isDarkMode);
  localStorage.setItem("isDarkMode", isDarkMode);
});

function setMode(isDarkMode) {
  if (isDarkMode) {
    body.classList.remove("light");
    body.classList.add("dark");
    modeText.innerText = "Modo claro";
  } else {
    body.classList.remove("dark");
    body.classList.add("light");
    modeText.innerText = "Modo oscuro";
  }
}
