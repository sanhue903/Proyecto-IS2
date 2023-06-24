// Obtener referencias a los campos de entrada y mensajes de advertencia
const usernameInput = document.getElementById('user');
const passwordInput = document.getElementById('pass');
const confirmPasswordInput = document.getElementById('pass2');
const emailInput = document.getElementById('email');

const usernameWarningIcon = document.getElementById('username-warning-icon');
const usernameWarningMessage = document.getElementById('username-warning-message');
const passwordWarningIcon = document.getElementById('password-warning-icon');
const passwordWarningMessage = document.getElementById('password-warning-message');
const confirmPasswordWarningIcon = document.getElementById('confirm-password-warning-icon');
const confirmPasswordWarningMessage = document.getElementById('confirm-password-warning-message');
const emailWarningIcon = document.getElementById('email-warning-icon');
const emailWarningMessage = document.getElementById('email-warning-message');

// Obtener referencia boton "Registrarme"
const registerButton = document.getElementById('register-button');

// Listeners
usernameInput.addEventListener('input', validateForm);
passwordInput.addEventListener('input', validateForm);
confirmPasswordInput.addEventListener('input', validateForm);
emailInput.addEventListener('input', validateForm);

// Mostrar advertencia
function showWarning(icon, message) {
  icon.style.display = 'inline';
  message.style.display = 'block';
}

// Ocultar advertencia
function hideWarning(icon, message) {
  icon.style.display = 'none';
  message.style.display = 'none';
}

// Validación para nombre de usuario
function validateUsername() {
  const value = usernameInput.value;
  const isValidUsername = /^[A-Za-z0-9@.+_-]+$/.test(value);
  if (value.length > 0 && (!isValidUsername || value.length < 8)) {
    showWarning(usernameWarningIcon, usernameWarningMessage);
    usernameWarningMessage.innerText = 'El usuario debe tener al menos 8 caracteres.';
  } else {
    hideWarning(usernameWarningIcon, usernameWarningMessage);
  }
}

function validatePassword() {
  const value = passwordInput.value;
  const hasNumber = /\d/.test(value);
  const similarToPersonalInfo = value.includes(usernameInput.value);
  const isCommonPassword = isCommonlyUsedPassword(value);
  const isNumericPassword = /^\d+$/.test(value);

  if (value.length > 0 && value.length < 8) {
    showWarning(passwordWarningIcon, passwordWarningMessage);
    passwordWarningMessage.innerText = 'La contraseña debe tener al menos 8 caracteres.';
  } else if (similarToPersonalInfo) {
    showWarning(passwordWarningIcon, passwordWarningMessage);
    passwordWarningMessage.innerText = 'La contraseña no puede asemejarse tanto a su otra información personal.';
  } else if (isCommonPassword) {
    showWarning(passwordWarningIcon, passwordWarningMessage);
    passwordWarningMessage.innerText = 'La contraseña no puede ser una clave utilizada comúnmente.';
  } else if (isNumericPassword) {
    showWarning(passwordWarningIcon, passwordWarningMessage);
    passwordWarningMessage.innerText = 'La contraseña no puede ser completamente numérica.';
  } else {
    hideWarning(passwordWarningIcon, passwordWarningMessage);
  }
}

function validateConfirmPassword() {
  const passwordValue = passwordInput.value;
  const confirmPasswordValue = confirmPasswordInput.value;
  if (confirmPasswordValue.length > 0 && passwordValue !== confirmPasswordValue) {
    showWarning(confirmPasswordWarningIcon, confirmPasswordWarningMessage);
    confirmPasswordWarningMessage.innerText = 'Las contraseñas no coinciden.';
  } else {
    hideWarning(confirmPasswordWarningIcon, confirmPasswordWarningMessage);
  }
}

function validateEmail() {
  const value = emailInput.value;
  const isValidEmail = /\S+@\S+\.\S+/.test(value);
  if (value.length > 0 && (!isValidEmail || value.length < 1)) {
    showWarning(emailWarningIcon, emailWarningMessage);
    emailWarningMessage.innerText = 'Ingrese un correo válido.';
  } else {
    hideWarning(emailWarningIcon, emailWarningMessage);
  }
}

function isCommonlyUsedPassword(password) {
  // ver si la contraseña es usada comunmente
  return false;
}

// Validar el formulario completo
function validateForm() {
  validateUsername();
  validatePassword();
  validateConfirmPassword();
  validateEmail();

  // Habilitar/deshabilitar boton "Registrarme"
  if (
    usernameWarningMessage.style.display === 'none' &&
    passwordWarningMessage.style.display === 'none' &&
    confirmPasswordWarningMessage.style.display === 'none' &&
    emailWarningMessage.style.display === 'none'
  ) {
    registerButton.disabled = false;
  } else {
    registerButton.disabled = true;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var modal = document.querySelector('.modal');
  var closeModalButton = document.querySelector('#closeModalButton');
  var submitButton = document.querySelector('#register-button');
  var form = document.querySelector('#myForm');
  var formularioEnviadoValue = document.getElementById('formularioEnviadoValue').getAttribute('data-formulario-enviado');
  var formularioEnviado = JSON.parse(formularioEnviadoValue);

  if (formularioEnviado) {
    modal.style.display = 'block';
  }

  submitButton.addEventListener('click', function(e) {
    e.preventDefault();

    var formFields = form.querySelectorAll('input, textarea, select');
    var formValid = true;

    // Validar cada campo del formulario
    formFields.forEach(function(field) {
      if (!field.checkValidity()) {
        field.reportValidity();
        formValid = false;
      }
    });

    if (formValid) {
      fetch(form.action, {
        method: form.method,
        body: new FormData(form)
      })
      .then(function(response) {
        modal.style.display = 'block';
        form.reset();
      })
      .catch(function(error) {
        console.error('Error:', error);
      });
    }
  });

  closeModalButton.addEventListener('click', function() {
    modal.style.display = 'none';
  });

  window.addEventListener('click', function(event) {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });
});