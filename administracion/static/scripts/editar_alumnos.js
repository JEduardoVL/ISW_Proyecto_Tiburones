
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function editAlumno(alumnoId) {
    fetch(`/administracion/alumnos/${alumnoId}/get_data/`)
    .then(response => response.json())
    .then(result => {
        const alumno = result.data;
        swal.fire({
            title: 'Editar Alumno',
            html: `
            <p>Nombre:</p>
                    <input id="nombre" class="swal2-input" value="${alumno.nombre}">
            <p>Apellido:</p>
                   <input id="apellido" class="swal2-input" value="${alumno.apellido}">
            <p>Correo electronico:</p>
                   <input id="correo_electronico" class="swal2-input" value="${alumno.correo_electronico}">
            <p>Programa academico:</p>
                   <input id="programa_academico" class="swal2-input" value="${alumno.programa_academico}">
            <p>Estatus:</p>
                   <select id="estatus" class="swal2-input">
                       <option value="activo" ${alumno.estatus === 'activo' ? 'selected' : ''}>Activo</option>
                       <option value="egresado" ${alumno.estatus === 'egresado' ? 'selected' : ''}>Egresado</option>
                   </select>`,
            focusConfirm: false,
            showCancelButton: true,  // Habilita el botón de cancelar
            confirmButtonText: 'Guardar',  // Texto del botón de guardar
            cancelButtonText: 'Cancelar',  // Texto del botón de cancelar
            preConfirm: () => {
                return {
                    nombre: document.getElementById('nombre').value,
                    apellido: document.getElementById('apellido').value,
                    correo_electronico: document.getElementById('correo_electronico').value,
                    programa_academico: document.getElementById('programa_academico').value,
                    estatus: document.getElementById('estatus').value
                }
            }
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/administracion/alumnos/${alumnoId}/update/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken() 
                    },
                    body: JSON.stringify(result.value)
                })
                .then(response => {
                    if (response.ok) {
                        swal.fire({
                            title: 'Actualizado',
                            text: 'Los datos del alumno han sido actualizados.',
                            icon: 'success',
                            timer: 2000,
                            timerProgressBar: true
                        }).then((result) => {
                            if (result.dismiss === Swal.DismissReason.timer) {
                                console.log('La alerta se cerró por el temporizador');
                            }
                            location.reload(); // Recarga la página después de cerrar la alerta
                        });
                    } else {
                        swal.fire('Error', 'No se pudo actualizar el alumno.', 'error');
                    }
                });
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                swal.fire('Cancelado', 'No se realizaron cambios en los datos del alumno.', 'error');
            }
        });
    });
}

function deleteAlumno(alumnoId) {
    swal.fire({
        title: '¿Estás seguro?',
        text: "¡No podrás revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminarlo!',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/administracion/alumnos/${alumnoId}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken() 
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    swal.fire(
                        'Eliminado!',
                        'El registro del alumno ha sido eliminado.',
                        'success'
                    );
                    location.reload(); 
                } else {
                    swal.fire(
                        'Error!',
                        'No se pudo eliminar el registro del alumno.',
                        'error'
                    );
                }
            });
        }
    });
}
