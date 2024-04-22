//Funcion para que al hacer clic en buscar muestre la tabla
function showTable() {
    var tableContainer = document.querySelector('.contenedor_tabla');
    tableContainer.style.display = 'block';
}


// Funcion para que al hacer clic en 'Busqueda avanzada' se despliegue
document.addEventListener('DOMContentLoaded', function () {
    const searchLink = document.querySelector('.search-2');
    const advancedSearchContainer = document.querySelector('.Avanzada');

    searchLink.addEventListener('click', function () {
        // Esto alterna la visibilidad del formulario
        if (advancedSearchContainer.style.display === 'block') {
            advancedSearchContainer.style.display = 'none';
        } else {
            advancedSearchContainer.style.display = 'block';
        }
    });
});