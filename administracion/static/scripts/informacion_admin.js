function editarDatosGenerales(nombre_administrador, apellido_administrador, departamento_administrador, cargo_administrador, correo_administrador, csrf_token) {
    Swal.fire({
        title: 'Editar datos generales',
        html:
            '<p>Nombre:</p> '+
            '<input id="nombre" class="swal2-input" placeholder="Nombre" value="' + nombre_administrador + '">' +
            '<p>Apellido:</p> '+
            '<input id="apellido" class="swal2-input" placeholder="Apellido" value="' + apellido_administrador + '">' +
            '<p>Departamento:</p> '+
            '<input id="departamento" class="swal2-input" placeholder="Departamento" value="' + departamento_administrador + '">' +
            '<p>Cargo:</p> '+
            '<input id="cargo" class="swal2-input" placeholder="Cargo" value="' + cargo_administrador + '">' +
            '<p>Correo electronico:</p> '+
            '<input id="correo" class="swal2-input" placeholder="Correo" value="' + correo_administrador + '">',
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
        preConfirm: () => {
            return {
                nombre: document.getElementById('nombre').value,
                apellido: document.getElementById('apellido').value,
                departamento: document.getElementById('departamento').value,
                cargo: document.getElementById('cargo').value,
                correo: document.getElementById('correo').value
            };
        }
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/administracion/editar_datos_generales/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token
                },
                body: JSON.stringify(result.value)
            }).then(response => {
                if (response.ok) {
                    Swal.fire('Datos generales actualizados', '', 'success').then(() => {
                        window.location.reload();
                    });
                } else {
                    Swal.fire('Error al actualizar los datos generales', '', 'error');
                }
            });
        }
    });
}

function cambiarContrasena(csrf_token) {
    Swal.fire({
        title: 'Cambiar contraseña',
        html:
            '<input id="old_password" type="password" class="swal2-input" placeholder="Contraseña antigua">' +
            '<input id="new_password" type="password" class="swal2-input" placeholder="Nueva contraseña">',
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
        preConfirm: () => {
            return {
                old_password: document.getElementById('old_password').value,
                new_password: document.getElementById('new_password').value
            };
        }
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/administracion/cambiar_contrasena/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token
                },
                body: JSON.stringify(result.value)
            }).then(response => {
                if (response.ok) {
                    Swal.fire('Contraseña cambiada', '', 'success').then(() => {
                        window.location.reload();
                    });
                } else {
                    Swal.fire('Error al cambiar la contraseña', '', 'error');
                }
            });
        }
    });
}
