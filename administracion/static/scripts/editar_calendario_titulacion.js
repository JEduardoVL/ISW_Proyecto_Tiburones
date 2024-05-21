document.getElementById('nueva_convocatoria').addEventListener('click', function() {
    Swal.fire({
      title: 'Agregar Nueva Convocatoria',
      html: `
        <form id="convocatoria_form">
          <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
          <label for="convocatoria">Convocatoria:</label><br>
          <input type="text" id="convocatoria" name="convocatoria" required><br>
          <label for="fecha_inicio">Fecha de Inicio:</label><br>
          <input type="date" id="fecha_inicio" name="fecha_inicio" required><br>
          <label for="fecha_limite_entrega">Fecha Límite de Entrega:</label><br>
          <input type="date" id="fecha_limite_entrega" name="fecha_limite_entrega" required><br>
          <label for="descripcion">Descripción:</label><br>
          <textarea id="descripcion" name="descripcion" required></textarea><br>
          <label for="requisitos">Requisitos:</label><br>
          <textarea id="requisitos" name="requisitos" required></textarea><br>
          <label for="documentos_a_entregar">Documentos a Entregar:</label><br>
          <textarea id="documentos_a_entregar" name="documentos_a_entregar" required></textarea><br>
          <button type="submit" style="display: none;">Submit</button>
        </form>
      `,
      showCancelButton: true,
      confirmButtonText: 'Agregar',
      preConfirm: () => {
        const form = document.getElementById('convocatoria_form');
        const formData = new FormData(form);
  
        return fetch(agregarConvocatoriaUrl, {
          method: 'POST',
          body: formData,
          headers: {
            'X-CSRFToken': csrfToken
          }
        })
        .then(response => {
          if (!response.ok) {
            throw new Error(response.statusText);
          }
          return response.json();
        })
        .catch(error => {
          Swal.showValidationMessage(`Request failed: ${error}`);
        });
      }
    }).then(result => {
      if (result.isConfirmed) {
        Swal.fire('¡Convocatoria agregada!', 'La convocatoria ha sido agregada exitosamente.', 'success')
        .then(() => location.reload());
      }
    });
  });
  
  function editarConvocatoria(convocatoriaId) {
    fetch(`${obtenerConvocatoriaUrl}${convocatoriaId}/`)
      .then(response => response.json())
      .then(data => {
        Swal.fire({
          title: 'Editar Convocatoria',
          html: `
            <form id="editarConvocatoriaForm">
              <label for="convocatoria">Convocatoria:</label>
              <input type="text" id="convocatoria" name="convocatoria" value="${data.convocatoria}"><br>
              <label for="fecha_inicio">Fecha de Inicio:</label>
              <input type="date" id="fecha_inicio" name="fecha_inicio" value="${data.fecha_inicio}"><br>
              <label for="fecha_limite_entrega">Fecha Límite de Entrega:</label>
              <input type="date" id="fecha_limite_entrega" name="fecha_limite_entrega" value="${data.fecha_limite_entrega}"><br>
              <label for="descripcion">Descripción:</label>
              <textarea id="descripcion" name="descripcion">${data.descripcion}</textarea><br>
              <label for="requisitos">Requisitos:</label>
              <textarea id="requisitos" name="requisitos">${data.requisitos}</textarea><br>
              <label for="documentos_a_entregar">Documentos a Entregar:</label>
              <textarea id="documentos_a_entregar" name="documentos_a_entregar">${data.documentos_a_entregar}</textarea><br>
            </form>
          `,
          showCancelButton: true,
          confirmButtonText: 'Guardar',
          cancelButtonText: 'Cancelar',
          preConfirm: () => {
            const form = document.getElementById('editarConvocatoriaForm');
            const formData = new FormData(form);
            return fetch(`${editarConvocatoriaUrl}${convocatoriaId}/`, {
              method: 'POST',
              body: formData,
              headers: {
                'X-CSRFToken': csrfToken
              }
            })
            .then(response => {
              if (!response.ok) {
                throw new Error(response.statusText);
              }
              return response.json();
            })
            .catch(error => {
              Swal.showValidationMessage(`Request failed: ${error}`);
            });
          }
        }).then(result => {
          if (result.isConfirmed) {
            Swal.fire('¡Actualizado!', 'La convocatoria ha sido actualizada.', 'success')
            .then(() => location.reload());
          }
        });
      });
  }
  
  function eliminarConvocatoria(convocatoriaId) {
    Swal.fire({
      title: '¿Está seguro?',
      text: "¡No podrá revertir esto!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Sí, eliminarla',
      cancelButtonText: 'No, cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        fetch(`${eliminarConvocatoriaUrl}${convocatoriaId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken
          }
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          if (data.success) {
            Swal.fire('¡Eliminada!', 'La convocatoria ha sido eliminada.', 'success')
            .then(() => location.reload());
          } else {
            Swal.fire('Error', 'Hubo un problema al eliminar la convocatoria.', 'error');
          }
        })
        .catch(error => {
          Swal.fire('Error', `Hubo un problema al eliminar la convocatoria: ${error.message}`, 'error');
        });
      }
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
  
  // Paginación
  const filasPorPagina = 4;
  const table = document.getElementById("convocatoriasTabla");
  const cuerpoTabla = table.querySelector("tbody");
  const filas = cuerpoTabla.querySelectorAll("tr");
  const paginacion = document.getElementById("pagination");
  
  function initPagination() {
    const numPaginas = Math.ceil(filas.length / filasPorPagina);
    paginacion.innerHTML = '';
  
    for (let i = 1; i <= numPaginas; i++) {
      const boton = document.createElement('button');
      boton.innerText = i;
      boton.addEventListener('click', () => {
        mostrarPagina(i);
        actualizarBotones(i);
      });
      paginacion.appendChild(boton);
    }
  
    mostrarPagina(1);
    actualizarBotones(1);
  }
  
  function mostrarPagina(pagina) {
    const inicio = (pagina - 1) * filasPorPagina;
    const fin = inicio + filasPorPagina;
  
    filas.forEach((fila, indice) => {
      if (indice >= inicio && indice < fin) {
        fila.style.display = '';
      } else {
        fila.style.display = 'none';
      }
    });
  }
  
  function actualizarBotones(pagina) {
    const botones = paginacion.querySelectorAll('button');
    botones.forEach((boton, indice) => {
      if (indice === (pagina - 1)) {
        boton.classList.add('active');
      } else {
        boton.classList.remove('active');
      }
    });
  }
  
  // Inicializar la paginación al cargar la página
  document.addEventListener('DOMContentLoaded', initPagination);
  