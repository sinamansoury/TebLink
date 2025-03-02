 const API_BASE_URL = "api/consultant/";

async function fetchSpecialities() {
    try {
        const response = await fetch(API_BASE_URL);
        const data = await response.json();
        $('#specialities').empty();

        data.forEach(consultant => {
            // لینک به صفحه دکترهای مربوط به تخصص
            const specialityLink = `/doctor/${consultant.name}`;
            $('#specialities').append(`
                <a href="${specialityLink}" class="block speciality-link" data-link="${specialityLink}">
                    <div class="bg-white p-5 rounded-xl shadow-md border border-gray-200 hover:shadow-lg transition duration-300 transform hover:-translate-y-1">
                        <p class="text-blue-600 text-lg font-semibold text-center">🔬 ${consultant.name}</p>
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

 window.onload = function () {
        document.body.style.opacity = "1"; // بعد از لود کامل نمایش بده
    };

    function openAuthModal() {
        document.getElementById("auth-modal").classList.remove("hidden");
    }

    function closeAuthModal() {
        document.getElementById("auth-modal").classList.add("hidden");
    }

    function openOtpModal() {
        document.getElementById("auth-modal").classList.add("hidden"); // مخفی کردن فرم ورود
        document.getElementById("otp-modal").classList.remove("hidden"); // نمایش فرم OTP
        startTimer(); // شروع تایمر
    }

    function closeOtpModal() {
        document.getElementById("otp-modal").classList.add("hidden");
    }

    // تایمر معکوس 2 دقیقه‌ای
    let timer;
    let timeLeft = 120; // 2 دقیقه (120 ثانیه)

    function startTimer() {
        timer = setInterval(function() {
            if (timeLeft <= 0) {
                clearInterval(timer);
                document.getElementById("otp-expired").classList.remove("hidden");
                document.getElementById("otp-time").classList.add("hidden");
            } else {
                document.getElementById("otp-time").textContent = `${Math.floor(timeLeft / 60)}:${timeLeft % 60 < 10 ? '0' + (timeLeft % 60) : timeLeft % 60}`;
                timeLeft--;
            }
        }, 1000);
    }

    function moveFocus(current, nextFieldId) {
        // اگر ورودی فعلی پر شد به فیلد بعدی منتقل شو
        if (current.value.length == current.maxLength) {
            document.getElementById(nextFieldId).focus();
        }
    }

    function handleEnterKey(event) {
        // اگر Enter فشرده شود، به فیلد بعدی منتقل شو
        if (event.key === "Enter") {
            let nextField = event.target.nextElementSibling;
            if (nextField) {
                nextField.focus();
            }
        }
    }

    function closeMenu() {
        document.getElementById("mobile-menu").classList.add("translate-x-full");
    }

    function openMenu() {
        document.getElementById("mobile-menu").classList.remove("translate-x-full");
    }

    function checkWindowSize() {
        if (window.innerWidth >= 768) {
            closeMenu();
        }
    }

    window.addEventListener("resize", checkWindowSize);
    checkWindowSize();