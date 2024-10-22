document.addEventListener('DOMContentLoaded', function () {
    // Role-based file upload visibility
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

    // Loop through each attendance record and create a pie chart for it
    if (typeof attendanceData !== 'undefined') {
        attendanceData.forEach(record => {
            var ctx = document.getElementById('attendance-chart-' + record.course.id).getContext('2d');
            var attendanceChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Attended', 'Missed'],
                    datasets: [{
                        data: [record.attended, record.missed],  // Use dynamic data from attendanceData
                        backgroundColor: ['#4caf50', '#f44336'],  // Colors for 'Attended' and 'Missed'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'bottom',
                        }
                    }
                }
            });
        });
    }
});
