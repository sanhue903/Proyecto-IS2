function onload() {
  const body = document.querySelector("body");
  const sidebar = body.querySelector("nav");
  const toggle = body.querySelector(".toggle");
  const modeSwitch = body.querySelector(".toggle-switch");
  const modeText = body.querySelector(".mode-text");
  const home = document.querySelector("#home .toggle");


  const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

  /* if (prefersDarkScheme.matches) {
        document.body.classList.toggle("dark", localStorage.getItem('darkmode') === 'true');
        modeText.innerText = "Modo claro";
    } */

  toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    sidebar.classList.toggle("hide");
  });

  home.addEventListener("click", () => {
    
    sidebar.classList.toggle("unhide");
  });

  modeSwitch.addEventListener("click", () => {
    const WasDarkMode = localStorage.getItem("darkmode") === "true";
    localStorage.setItem("darkmode", !WasDarkMode);
    const element = document.body;
    element.classList.toggle("dark");
    sendDarkMode(darkMode); // Envía la notificación al servidor
  });

  document.body.classList.toggle(
    "dark",
    localStorage.getItem("darkmode") === "true"
  );

  window.addEventListener("load", () => {
    home.style.display = "none";
    if (screen.width > 850) {
      sidebar.classList.remove("close");
    } else {
      if (screen.width < 850) {
        sidebar.classList.add("close");
      }
      if (screen.width < 600) {
        sidebar.classList.add("close");
        sidebar.classList.add("hide");
        home.style.display = "block";
      } else {
        sidebar.classList.remove("hide");
      }
    }
  });

  console.log(screen.width);
  window.addEventListener("resize", () => {
    home.style.display = "none";
    if (screen.width > 850) {
      sidebar.classList.remove("close");
    } else {
      if (screen.width < 850) {
        sidebar.classList.add("close");

        if (screen.width < 600) {
          sidebar.classList.add("close");
          sidebar.classList.add("hide");
          home.style.display = "block";
        } else {
          sidebar.classList.remove("hide");
        }
      }
    }
  });

  // Agrega el siguiente código en la función 'onload'

  function sendDarkMode(darkMode) {
    fetch('', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'  // Asegúrate de tener la etiqueta CSRF en tu formulario
      },
      body: JSON.stringify({ dark_mode: darkMode })
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          console.log('Modo oscuro cambiado correctamente');
        } else {
          console.error('Error al cambiar el modo oscuro');
        }
      })
      .catch(error => {
        console.error('Error de red:', error);
      });
  }
}

document.addEventListener("DOMContentLoaded", onload);
