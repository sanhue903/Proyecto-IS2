document.addEventListener('DOMContentLoaded', function() {
  // Obtener el botón de flecha para abrir el contenido de la pestaña
  var botonAbrir = document.getElementById("abrir-modal");

  // Obtener el contenido de la pestaña
  var contenidoPestana = document.querySelector("#modal-proyectos .modal-contenido");

  // Obtener el modal
  var modal = document.getElementById("modal-proyectos");

  // Cuando el usuario haga clic en el botón de flecha, mostrar/ocultar el contenido de la pestaña
  botonAbrir.onclick = function() {
    contenidoPestana.classList.toggle("visible");
    botonAbrir.classList.toggle("abierto");
  }

  // Cuando el usuario haga clic fuera del modal o en el botón para cerrar el modal, cerrarlo
  window.addEventListener("click", function(event) {
    if (!modal.contains(event.target)) {
      contenidoPestana.classList.remove("visible");
      botonAbrir.classList.remove("abierto");
    }
  });

  // Obtener el botón de flecha para abrir el contenido de la pestaña de estados
  var botonAbrirEstados = document.getElementById("abrir-estados");

  // Obtener el contenido de la pestaña de estados
  var contenidoPestanaEstados = document.querySelector("#modal-estados .modal-contenido");

  // Obtener el modal de estados
  var modalEstados = document.getElementById("modal-estados");

  // Cuando el usuario haga clic en el botón de flecha de estados, mostrar/ocultar el contenido de la pestaña de estados
  botonAbrirEstados.onclick = function() {
    contenidoPestanaEstados.classList.toggle("visible");
    botonAbrirEstados.classList.toggle("abierto");
  }

  // Cuando el usuario haga clic fuera del modal de estados o en el botón para cerrar el modal, cerrarlo
  window.addEventListener("click", function(event) {
    if (!modalEstados.contains(event.target)) {
      contenidoPestanaEstados.classList.remove("visible");
      botonAbrirEstados.classList.remove("abierto");
    }
  });



});