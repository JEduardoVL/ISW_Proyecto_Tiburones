document.addEventListener('DOMContentLoaded', function () {
    // Asegurándonos de que el formulario y los campos existan antes de añadir listeners
    var signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData(this);
            fetch(signupForm.dataset.url, { 
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': signupForm.dataset.csrfToken
                },
            })
            .then(response => response.json())
            .then(handleResponse)
            .catch(handleError);
        });
    }

    const userTypeFields = document.querySelectorAll('input[name="user_type"]');
    userTypeFields.forEach(function(userTypeField) {
        userTypeField.addEventListener('change', function (e) {
            const selectedType = e.target.value;
            toggleUserFields(selectedType);
        });
    });

    function toggleUserFields(selectedType) {
        document.getElementById('alumnoFields').style.display = selectedType === 'is_alumno' ? 'block' : 'none';
        document.getElementById('docenteFields').style.display = selectedType === 'is_docente' ? 'block' : 'none';
        document.getElementById('administrativoFields').style.display = selectedType === 'is_administrador' ? 'block' : 'none';
    }

    function handleResponse(data) {
        if (data.status === 'success') {
            Swal.fire({
                title: 'Éxito!',
                text: data.message,
                icon: 'success',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    resetForm();
                }
            });
        } else {
            let errorMessage = "Error al crear la cuenta. Revise los detalles.";
            if (data.errors) {
                errorMessage += "\n" + JSON.stringify(data.errors);
            }
            Swal.fire({
                title: 'Error!',
                text: errorMessage,
                icon: 'error',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    resetForm();
                }
            });
        }
    }

    function handleError(error) {
        console.error('Error:', error);
    }

    function resetForm() {
        signupForm.reset(); // Resetea todos los campos del formulario a sus valores iniciales
        document.getElementById('alumnoFields').style.display = 'none';
        document.getElementById('docenteFields').style.display = 'none';
        document.getElementById('administrativoFields').style.display = 'none';
    }
});
