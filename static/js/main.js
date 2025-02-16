 const API_BASE_URL = "https://teblink.onrender.com/api/consultant/";

async function fetchSpecialities() {
    try {
        const response = await fetch(API_BASE_URL);
        const data = await response.json(); // دریافت داده‌ها از API
        $('#specialities').empty(); // پاک کردن اطلاعات قبلی

        data.forEach(consultant => {
            // لینک به صفحه دکترهای مربوط به تخصص
            const specialityLink = `/doctor/${consultant.consultant}`;
            $('#specialities').append(`
                <a href="${specialityLink}" class="block speciality-link" data-link="${specialityLink}">
                    <div class="bg-white p-5 rounded-xl shadow-md border border-gray-200 hover:shadow-lg transition duration-300 transform hover:-translate-y-1">
                        <p class="text-blue-600 text-lg font-semibold text-center">🔬 ${consultant.consultant}</p>
                        <p class="text-gray-500 text-sm text-center mt-1">👨‍⚕️ تعداد پزشکان: <span class="font-bold">${consultant.count}</span></p>
                    </div>
                </a>
            `);
        });
        // اضافه کردن رویداد کلیک به هر لینک
        $('.speciality-link').on('click', function () {
            const specialityName = $(this).data('link').split('/').pop();  // استخراج نام تخصص از لینک
            fetchDoctorsBySpeciality(specialityName); // فراخوانی تابع برای دریافت دکترها
        });

    } catch (error) {
        console.error("Error fetching specialities:", error);
    }
}

$(document).ready(fetchSpecialities);