document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('speciality-name').textContent = consultant; // مقداردهی از متغیر گلوبال در HTML

    const API_URL = `/doctor/api/doctors/${consultant}/`;

    async function fetchDoctors() {
        try {
            const response = await fetch(API_URL);
            const data = await response.json();
            const doctorsListElement = document.getElementById('doctors-list');
            doctorsListElement.innerHTML = ""; // پاک کردن محتوای قبلی

            data.forEach(doctor => {
                const profileLink = `/doctor/${doctor.name}-${doctor.last_name}/profile`;

                const doctorCard = document.createElement('div');
                doctorCard.className = "bg-white rounded-xl shadow-md p-4 flex flex-col items-center h-80 space-y-10";
                doctorCard.innerHTML = `
                    <div class="relative">
                        <img src="${doctor.image || 'https://via.placeholder.com/100'}" class="rounded-full border-4 border-green-400 p-1">
                        <span class="absolute bottom-1 right-1 w-4 h-4 bg-green-500 rounded-full"></span>
                    </div>
                    <h2 class="font-bold text-lg text-gray-800">${doctor.name} ${doctor.last_name}</h2>
                    <p class="text-sm text-gray-600">${doctor.speciality_name}</p>
                    <div class="mt-auto space-y-2 w-full">
                        <input type="hidden" class="doctor-id" value="${doctor.id}">
                        <a href="#" 
                           class="profile-link w-full px-4 py-2 bg-red-400 text-white rounded-lg text-center block"
                           data-id="${doctor.id}" data-url="${profileLink}">
                            مشاهده پروفایل
                        </a>
                        
                        <a href="#" 
                           class="appointment-link w-full px-4 py-2 bg-blue-600 text-white rounded-lg text-center block"
                           data-id="${doctor.id}">
                            درخواست ویزیت
                        </a>
                    </div>
                `;
                doctorsListElement.prepend(doctorCard);

                // ذخیره doctor_id هنگام کلیک روی مشاهده پروفایل
                doctorCard.querySelector('.profile-link').addEventListener('click', function (e) {
                    e.preventDefault();
                    const doctorId = doctor.id;
                    localStorage.setItem("doctor_id", doctorId); // ذخیره ID در localStorage
                    window.location.href = profileLink; // هدایت به صفحه پروفایل
                });

                // ارسال ID دکتر هنگام کلیک روی درخواست ویزیت
                doctorCard.querySelector('.appointment-link').addEventListener('click', function(e) {
                    e.preventDefault();
                    console.log("🩺 درخواست ویزیت برای دکتر:", doctorId);
                    // اینجا می‌توان API برای ثبت نوبت را فراخوانی کرد
                });
            });
        } catch (error) {
            console.error("Error fetching doctors:", error);
        }
    }

    fetchDoctors();
});
