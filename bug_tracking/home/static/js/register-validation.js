// Referencias
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

const registerButton = document.getElementById('register-button');

// Variables para guardar los errores
let usernameError = false;
let emailError = false;

// Listeners
usernameInput.addEventListener('input', validateUsername);
passwordInput.addEventListener('input', validatePassword);
confirmPasswordInput.addEventListener('input', validateConfirmPassword);
emailInput.addEventListener('input', validateEmail);

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

// Validación nombre de usuario
function validateUsername() {
  const value = usernameInput.value;
  const isValidUsername = /^[A-Za-z0-9@.+_-]+$/.test(value);

  if (value.length > 0 && (!isValidUsername || value.length < 8)) {
    showWarning(usernameWarningIcon, usernameWarningMessage);
    usernameWarningMessage.innerText = 'El usuario debe tener al menos 8 caracteres.';
    usernameError = true;
  } else {
    hideWarning(usernameWarningIcon, usernameWarningMessage);
    if (value.length >= 8) {
      checkUsernameAvailability(value)
        .then(isAvailable => {
          if (!isAvailable) {
            showWarning(usernameWarningIcon, usernameWarningMessage);
            usernameWarningMessage.innerText = 'Ya existe un usuario con este nombre.';
            registerButton.disabled = true;
            usernameError = true;
          } else {
            hideWarning(usernameWarningIcon, usernameWarningMessage);
            usernameError = false;
            checkFormValidity();
          }
        })
        .catch(error => {
          console.error('Error al verificar la disponibilidad del nombre de usuario:', error);
        });
    } else {
      usernameError = false;
      checkFormValidity();
    }
  }
}

// Validación correo electrónico
function validateEmail() {
  const value = emailInput.value;
  const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

  if (value.length > 0 && !isValidEmail) {
    showWarning(emailWarningIcon, emailWarningMessage);
    emailWarningMessage.innerText = 'Por favor, introduce un correo electrónico válido.';
    emailError = true;
  } else {
    hideWarning(emailWarningIcon, emailWarningMessage);
    if (isValidEmail) {
      checkEmailAvailability(value)
        .then(isAvailable => {
          if (!isAvailable) {
            showWarning(emailWarningIcon, emailWarningMessage);
            emailWarningMessage.innerText = 'Ya existe un usuario con este correo electrónico.';
            registerButton.disabled = true;
            emailError = true;
          } else {
            hideWarning(emailWarningIcon, emailWarningMessage);
            emailError = false;
            checkFormValidity();
          }
        })
        .catch(error => {
          console.error('Error al verificar la disponibilidad del correo electrónico:', error);
        });
    } else {
      emailError = false;
      checkFormValidity();
    }
  }
}

// Validar contraseña
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

// Validar confirmación de contraseña
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

function isCommonlyUsedPassword(password) {
  // Ver si contraseña es comunmente usada
  return false;
}

// Verificar disponibilidad de nombre de usuario en la base de datos
function checkUsernameAvailability(username) {
  const formData = new FormData();
  formData.append('username', username);

  return fetch('/check-username-availability/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken()
    },
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      return data.available;
    });
}

// Verificar disponibilidad de correo electrónico en la base de datos
function checkEmailAvailability(email) {
  const formData = new FormData();
  formData.append('email', email);
  return fetch('/check-email-availability/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken()
    },
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      return data.available;
    });
}

// Obtener el token CSRF
function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(cookie => cookie.startsWith('csrftoken='))
    .split('=')[1];
  return cookieValue;
}

// Verificar la validez del formulario completo
function checkFormValidity() {
  if (!usernameError && !emailError) {
    registerButton.disabled = false;
  } else {
    registerButton.disabled = true;
  }
}
