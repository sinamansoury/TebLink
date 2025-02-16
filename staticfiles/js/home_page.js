document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('speciality-name').textContent = consultant; // مقداردهی از متغیر گلوبال در HTML

    const API_URL = `https://teblink.onrender.com/doctor/api/doctors/${consultant}/`;

    async function fetchDoctors() {
        try {
            const response = await fetch(API_URL);
            const data = await response.json();
            const doctorsListElement = document.getElementById('doctors-list');
            doctorsListElement.innerHTML = "";

            data.forEach(doctor => {
                const doctorCard = document.createElement('div');
                doctorCard.className = "bg-white rounded-xl shadow-md p-4 flex flex-col items-center h-80 space-y-10";
                doctorCard.innerHTML = `
                    <div class="relative">
                        <img src="${doctor.image || 'https://via.placeholder.com/100'}" class="rounded-full border-4 border-green-400 p-1">
                        <span class="absolute bottom-1 right-1 w-4 h-4 bg-green-500 rounded-full"></span>
                    </div>
                    <h2 class="font-bold text-lg text-gray-800">${doctor.name}</h2>
                    <p class="text-sm text-gray-600">${doctor.speciality_name}</p>
                    <div class="mt-auto space-y-2 w-full">
                        <button class="w-full px-4 py-2 bg-red-400 text-white rounded-lg">مشاهده پروفایل</button>
                        <button class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg">درخواست ویزیت</button>
                    </div>
                `;

                doctorsListElement.prepend(doctorCard);
            });
        } catch (error) {
            console.error("Error fetching doctors:", error);
        }
    }

    fetchDoctors();
});
