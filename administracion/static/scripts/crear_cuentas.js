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

