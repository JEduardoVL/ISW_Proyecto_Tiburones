document.addEventListener('DOMContentLoaded', function () {
    const userTypeFields = document.querySelectorAll('input[name="user_type"]');
    
    userTypeFields.forEach(function(userTypeField) {
      userTypeField.addEventListener('change', function (e) {
        const selectedType = e.target.value;
        document.getElementById('alumnoFields').style.display = selectedType === 'is_alumno' ? 'block' : 'none';
        document.getElementById('docenteFields').style.display = selectedType === 'is_docente' ? 'block' : 'none';
        document.getElementById('administrativoFields').style.display = selectedType === 'is_administrador' ? 'block' : 'none';
      });
    });
  });


  document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch("{% url 'administracion:create_user' %}", { 
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            Swal.fire({
                title: 'Éxito!',
                text: data.message,
                icon: 'success',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    resetForm(); // Llamar a la función de limpieza de formulario
                }
            });
        } else {
            Swal.fire({
                title: 'Error!',
                text: data.message,
                icon: 'error',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    resetForm(); // Llamar a la función de limpieza de formulario
                }
            });
        }
    })
    .catch(error => console.error('Error:', error));
});

function resetForm() {
    document.getElementById('signupForm').reset(); // Resetea todos los campos del formulario a sus valores iniciales
    document.getElementById('alumnoFields').style.display = 'none';
    document.getElementById('docenteFields').style.display = 'none';
    document.getElementById('administrativoFields').style.display = 'none';
}

