function editarUsuario(userId) {
    const url = `/administracion/cuentas/get-user-details/${userId}/`;
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
      })
      .then(data => {
        if (!data) {
          console.error('Datos del usuario no están disponibles o la respuesta no está estructurada correctamente');
          return;
        }
        let formulario = '';
        if (data.is_alumno) {
          formulario = `
            <form id="edit-form">
              <input type="text" name="nombre" placeholder="Nombre" class="swal2-input" value="${data.nombre}">
              <input type="text" name="apellido" placeholder="Apellido" class="swal2-input" value="${data.apellido}">
              <input type="email" name="correo_electronico" placeholder="Correo Electrónico" class="swal2-input" value="${data.correo_electronico}">
              <input type="text" placeholder="Tipo de Usuario: Alumno" class="swal2-input" readonly>
              <input type="text" name="matricula" placeholder="Matrícula" class="swal2-input" value="${data.matricula}">
              <input type="text" name="programa_academico" placeholder="Programa Académico" class="swal2-input" value="${data.programa_academico}">
              <select name="estatus" class="swal2-input">
                <option value="activo" ${data.estatus === 'activo' ? 'selected' : ''}>Activo</option>
                <option value="egresado" ${data.estatus === 'egresado' ? 'selected' : ''}>Egresado</option>
              </select>
            </form>
          `;
        }else if (data.is_docente) {
          formulario = `
            <form id="edit-form">
              <input type="text" name="nombre" placeholder="Nombre" class="swal2-input" value="${data.nombre}">
              <input type="text" name="apellido" placeholder="Apellido" class="swal2-input" value="${data.apellido}">
              <input type="email" name="correo_electronico" placeholder="Correo Electrónico" class="swal2-input" value="${data.correo_electronico}">
              <input type="text" placeholder="Tipo de Usuario: Docente" class="swal2-input" readonly>
              <input type="text" name="especialidad" placeholder="Especialidad" class="swal2-input" value="${data.especialidad}">
              <input type="text" name="departamento_docente" placeholder="Departamento" class="swal2-input" value="${data.departamento_docente}">
            </form>
          `;
        } else if (data.is_administrador) {
          formulario = `
            <form id="edit-form">
              <input type="text" name="nombre" placeholder="Nombre" class="swal2-input" value="${data.nombre}">
              <input type="text" name="apellido" placeholder="Apellido" class="swal2-input" value="${data.apellido}">
              <input type="email" name="correo_electronico" placeholder="Correo Electrónico" class="swal2-input" value="${data.correo_electronico}">
              <input type="text" placeholder="Tipo de Usuario: Administrador" class="swal2-input" readonly>
              <input type="text" name="cargo" placeholder="Cargo" class="swal2-input" value="${data.cargo}">
              <input type="text" name="departamento_admin" placeholder="Departamento" class="swal2-input" value="${data.departamento_admin}">
            </form>
          `;
        }
  
        if (formulario) {
          Swal.fire({
            title: 'Editar Usuario',
            html: formulario,
            showCancelButton: true,
            confirmButtonText: 'Actualizar',
            cancelButtonText: 'Cancelar',
            preConfirm: () => {
    const form = Swal.getPopup().querySelector('#edit-form');
    const nombre = form.querySelector('[name="nombre"]').value;
    const apellido = form.querySelector('[name="apellido"]').value;
    const correo_electronico = form.querySelector('[name="correo_electronico"]').value;
    
    // Define un objeto para capturar los valores de los campos
    let data = {
      nombre: nombre,
      apellido: apellido,
      correo_electronico: correo_electronico
    };
  
    // Comprobar y añadir campos de alumno si están presentes
    const matricula = form.querySelector('[name="matricula"]');
    const programa_academico = form.querySelector('[name="programa_academico"]');
    const estatus = form.querySelector('[name="estatus"]');
    if (matricula && programa_academico && estatus) {
      data.matricula = matricula.value;
      data.programa_academico = programa_academico.value;
      data.estatus = estatus.value;
    }
  
    // Comprobar y añadir campos de docente si están presentes
    const especialidad = form.querySelector('[name="especialidad"]');
    const departamento_docente = form.querySelector('[name="departamento_docente"]');
    if (especialidad && departamento_docente) {
      data.especialidad = especialidad.value;
      data.departamento_docente = departamento_docente.value;
    }
  
    // Comprobar y añadir campos de administrador si están presentes
    const cargo = form.querySelector('[name="cargo"]');
    const departamento_admin = form.querySelector('[name="departamento_admin"]');
    if (cargo && departamento_admin) {
      data.cargo = cargo.value;
      data.departamento_admin = departamento_admin.value;
    }
  
    return data;
  }
  
          }).then((result) => {
            if (result.isConfirmed) {
              actualizarUsuario(userId, result.value);
            }
          });
        }
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
      });
  }
  
  function cerrarFormulario() {
    document.body.removeChild(document.querySelector('#edit-form').parentNode);
  }
  
  function actualizarUsuario(userId, userData) {
    fetch(`/administracion/cuentas/update-user/${userId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') // Asegúrate de obtener el token CSRF de Django
      },
      body: JSON.stringify(userData)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      Swal.fire('Actualizado', 'El usuario ha sido actualizado con éxito.', 'success').then((result) => {
        if (result.isConfirmed || result.isDismissed) {
          window.location.reload(); // Esto recargará la página
        }
      });
    })
    .catch(error => {
      console.error('Failed to update user:', error);
      Swal.fire('Error', 'Hubo un problema al actualizar el usuario.', 'error');
    });
  }
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  function deleteUsuario(userId) {
      let userUrl = `/administracion/cuentas/${userId}/delete/`;
  
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
              fetch(userUrl, {
                  method: 'DELETE',
                  headers: {
                      'X-CSRFToken': getCookie('csrftoken')
                  }
              })
              .then(response => {
                  if (!response.ok) {
                      throw new Error('Network response was not ok');
                  }
                  return response.json();
              })
              .then(data => {
                  if (data.status === 'success') {
                      swal.fire(
                          'Eliminado!',
                          'El usuario ha sido eliminado.',
                          'success'
                      );
                      location.reload(); 
                  } else {
                      swal.fire(
                          'Error!',
                          'No se pudo eliminar el usuario.',
                          'error'
                      );
                  }
              })
              .catch(error => {
                  console.error('Error during fetch:', error);
                  swal.fire(
                      'Error!',
                      'Hubo un problema con la petición.',
                      'error'
                  );
              });
          }
      });
  }
  
  