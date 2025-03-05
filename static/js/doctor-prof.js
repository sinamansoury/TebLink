document.addEventListener("DOMContentLoaded", async function () {
    try {
        const doctorId = localStorage.getItem("doctor_id");
        if (!doctorId) {
            console.error("❌ doctor_id در localStorage پیدا نشد!");
            return;
        }

        const doctorProfileUrl = window.location.pathname;
        const pathParts = doctorProfileUrl.split("/").filter(part => part.trim() !== ""); // حذف بخش‌های خالی
        let doctorNameLastName = pathParts.slice(-2).join("-"); // استخراج نام و نام خانوادگی
        doctorNameLastName = doctorNameLastName.replace(/-profile$/, "");

        const response = await fetch(`/doctor/api/profile/${doctorNameLastName}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ doctor_id: doctorId })
        });

        if (!response.ok) {
            throw new Error("خطا در دریافت اطلاعات دکتر");
        }

        const doctor = await response.json();

        // بررسی مقدار doctor قبل از نمایش در صفحه
        if (!doctor || Object.keys(doctor).length === 0) {
            console.error("❌ داده‌های دکتر خالی یا نامعتبر است!");
            return;
        }

        // تغییر عنوان صفحه به نام دکتر
        document.title = doctor.name + " " + doctor.last_name;

        // نمایش اطلاعات در صفحه
        document.getElementById("doctor-name").textContent = doctor.name + " " + doctor.last_name;
        document.getElementById("doctor-bio").textContent = doctor.bio || "اطلاعاتی وارد نشده است";
        document.getElementById("doctor-address").textContent = doctor.address || "اطلاعاتی وارد نشده است";
        document.getElementById("doctor-phone").textContent = doctor.main_phone || "اطلاعاتی وارد نشده است";
        document.getElementById("doctor-degree").textContent = `${doctor.degree_name} - ${doctor.speciality_name}` || "اطلاعاتی وارد نشده است";
        document.getElementById("doctor-id-code").textContent = "کد نظام پزشکی: " + (doctor.number || "اطلاعاتی وارد نشده است");
        document.getElementById("doctor-image").src = doctor.image || "https://via.placeholder.com/100";

        // نمایش لیست خدمات
        const servicesList = document.getElementById("services-list");
servicesList.innerHTML = "";
if (doctor.services && doctor.services.length > 0) {
    doctor.services.forEach(service => {
        const serviceElement = document.createElement("div");
        serviceElement.className = "bg-white p-8 rounded-lg shadow-lg border-2 border-gray-300 w-full md:w-3/4 lg:w-2/3 xl:w-1/2 mx-auto my-6";  // افزایش padding و تنظیم عرض بزرگتر

        // اسم سرویس بالای هزینه
        if (service.name) {
            const serviceName = document.createElement("p");
            serviceName.className = "text-lg font-bold mb-3";  // فاصله از پایین برای نام
            serviceName.textContent = service.name;
            serviceElement.appendChild(serviceName);
        } else {
            const noName = document.createElement("p");
            noName.className = "text-gray-500";
            noName.textContent = "نام سرویس یافت نشد"; // اگر نام سرویس موجود نبود
            serviceElement.appendChild(noName);
        }

        // نمایش بازه قیمت و دکمه درخواست ویزیت در کنار هم
        const priceAndButtonWrapper = document.createElement("div");
        priceAndButtonWrapper.className = "flex justify-between items-center mt-4";  // افزایش فاصله برای جلوه بهتر

        // نمایش بازه قیمت
        if (service.min_price && service.max_price) {
            const priceRange = document.createElement("p");
            priceRange.className = "text-sm text-gray-600 mt-2 w-2/3";  // عرض 2/3 برای قیمت
            priceRange.textContent = `هزینه: ${service.min_price.toLocaleString()} - ${service.max_price.toLocaleString()} تومان`;
            priceAndButtonWrapper.appendChild(priceRange);
        }

        // دکمه درخواست ویزیت
        const requestButton = document.createElement("button");
        requestButton.className = "bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition w-1/3 border-2 border-blue-600 hover:border-blue-700";  // مستطیلی کردن دکمه و افزایش اندازه
        requestButton.textContent = "درخواست ویزیت";
        requestButton.onclick = function () {
            alert(`درخواست ویزیت برای سرویس ${service.name} ارسال شد.`);
        };

        // اضافه کردن دکمه به کنار هزینه
        priceAndButtonWrapper.appendChild(requestButton);

        // اضافه کردن بخش قیمت و دکمه به باکس سرویس
        serviceElement.appendChild(priceAndButtonWrapper);

        servicesList.appendChild(serviceElement);
    });
} else {
    servicesList.innerHTML = "<p class='text-gray-500'>خدماتی ثبت نشده است</p>";
}


    } catch (error) {
        console.error("مشکل در دریافت اطلاعات دکتر:", error);
    }
});
