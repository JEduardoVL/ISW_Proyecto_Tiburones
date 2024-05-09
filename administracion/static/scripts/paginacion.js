document.addEventListener('DOMContentLoaded', function () {
  const rowsPerPage = 5;
  const userRows = Array.from(document.querySelectorAll("#userTable tbody tr"));
  const totalPages = Math.ceil(userRows.length / rowsPerPage);
  const paginationContainer = document.getElementById("pagination");
  const tableBody = document.getElementById("tableBody");

  function displayPage(page) {
    const start = (page - 1) * rowsPerPage;
    const end = page * rowsPerPage;
    tableBody.innerHTML = ''; // Limpia el contenido actual del cuerpo de la tabla
    userRows.slice(start, end).forEach(row => tableBody.appendChild(row.cloneNode(true))); // Clona cada fila y la agrega
    updatePaginationButtons(page);
  }

  function updatePaginationButtons(currentPage) {
    paginationContainer.innerHTML = ''; // Limpia los botones actuales
    for (let i = 1; i <= totalPages; i++) {
      const pageButton = document.createElement('button');
      pageButton.textContent = i;
      pageButton.className = (i === currentPage) ? 'active' : '';
      pageButton.addEventListener('click', function() { displayPage(i); }); // Asegúrate de que el manejador de eventos esté correctamente asignado
      paginationContainer.appendChild(pageButton);
    }
  }

  if (userRows.length > 0) {
    displayPage(1); // Muestra la primera página al cargar
  }
});
