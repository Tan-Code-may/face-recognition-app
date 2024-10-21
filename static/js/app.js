document.addEventListener('DOMContentLoaded', function () {
    const roleSelect = document.querySelector('select[name="role"]');
    const studentUpload = document.getElementById('student-upload');

    if (roleSelect) {
        roleSelect.addEventListener('change', function () {
            if (roleSelect.value === 'student') {
                studentUpload.style.display = 'block';
            } else {
                studentUpload.style.display = 'none';
            }
        });
    }
});