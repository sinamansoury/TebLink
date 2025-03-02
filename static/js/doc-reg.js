function getCSRFToken() {
            let csrfToken = null;
            document.cookie.split(';').forEach(function (cookie) {
                if (cookie.trim().startsWith('csrftoken=')) {
                    csrfToken = cookie.trim().substring('csrftoken='.length);
                }
            });
            return csrfToken;
        }
        document.addEventListener("DOMContentLoaded", function () {
            fetch('/api/degree/')
                .then(response => response.json())
                .then(data => {
                    const degreeSelect = document.getElementById('degree');

                    // اضافه کردن گزینه‌های دریافت شده به dropdown
                    data.forEach(degree => {  // داده‌ها به صورت مستقیم لیست هستند
                        const option = document.createElement('option');
                        option.value = degree.id; // یا هر چیزی که برای value لازم دارید
                        option.textContent = degree.name;
                        degreeSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error("خطا در دریافت داده‌ها:", error);
                });
        });
        document.getElementById("degree").addEventListener("change", function () {
    const degreeId = this.value;

    if (degreeId) {
        fetch(`/api/specialty/${degreeId}/`)
            .then(response => response.json())
            .then(data => {
                const specialtySelect = document.getElementById("specialty");
                specialtySelect.innerHTML = '<option value="">انتخاب کنید</option>';  // پاک کردن تخصص‌های قبلی

                // اضافه کردن تخصص‌های جدید به dropdown
                data.forEach(specialty => {
                    const option = document.createElement('option');
                    option.value = specialty.id;
                    option.textContent = specialty.name;
                    specialtySelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error("خطا در دریافت تخصص‌ها:", error);
            });
    } else {
        // اگر مدرک انتخاب نشده بود، فیلد تخصص را خالی کنید
        document.getElementById("specialty").innerHTML = '<option value="">انتخاب کنید</option>';
    }
});


        document.addEventListener("DOMContentLoaded", function () {
            const otpInputs = document.querySelectorAll(".otp-box");

            otpInputs.forEach((input, index) => {
                input.addEventListener("input", (e) => {
                    if (e.target.value.length === 1 && index < otpInputs.length - 1) {
                        otpInputs[index + 1].focus(); // رفتن به فیلد بعدی
                    }
                });

                input.addEventListener("keydown", (e) => {
                    if (e.key === "Backspace" && input.value.length === 0 && index > 0) {
                        otpInputs[index - 1].focus(); // بازگشت به فیلد قبلی
                    }
                });
            });
        });
        document.addEventListener("DOMContentLoaded", function () {
            const phoneInput = document.getElementById("phone-number");
            const sendOtpBtn = document.getElementById("send-otp");
            const otpInputs = document.querySelectorAll(".otp-box");
            const otpForm = document.getElementById("otp-form");
            const doctorForm = document.getElementById("doctor-form");

            let phoneNumber = "";

            // 📌 ارسال شماره موبایل برای دریافت یا تأیید OTP
            sendOtpBtn.addEventListener("click", function () {
                phoneNumber = phoneInput.value.trim();

                if (!phoneNumber || phoneNumber.length !== 11 || !/^09\d{9}$/.test(phoneNumber)) {
                    alert("لطفاً یک شماره موبایل معتبر وارد کنید.");
                    return;
                }

                fetch("/api/doctor/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()},
                    body: JSON.stringify({ phone: phoneNumber, step: "send_otp" })  // ارسال درخواست OTP
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById("otp-section").classList.remove("hidden");
                            otpInputs[0].focus();
                        } else {
                            alert(data.message || "ارسال OTP ناموفق بود.");
                        }
                    })
                    .catch(error => console.error("خطا در ارسال OTP:", error));
            });

            // 📌 تأیید OTP
            otpForm.addEventListener("submit", function (event) {
                event.preventDefault();

                let otpCode = Array.from(otpInputs).map(input => input.value.trim()).join("");
                if (otpCode.length !== 5) {
                    alert("لطفاً کد تأیید ۵ رقمی را وارد کنید.");
                    return;
                }

                fetch("/api/doctor/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()},
                    body: JSON.stringify({ phone: phoneNumber, otp: otpCode, step: "verify_otp" })  // تأیید OTP
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById("otp-page").classList.add("hidden");
                            document.getElementById("register-page").classList.remove("hidden");
                        } else {
                            alert("کد تأیید اشتباه است. لطفاً مجدداً تلاش کنید.");
                            otpInputs.forEach(input => input.value = "");  // پاک کردن فیلدهای OTP

                        }
                    })
                    .catch(error => console.error("خطا در تایید OTP:", error));
            });

            // 📌 ارسال اطلاعات ثبت‌نام پزشک
            doctorForm.addEventListener("submit", function (event) {
                event.preventDefault();

                const formData = {
                    phone: phoneNumber,
                    first_name: document.getElementById("first-name").value.trim(),
                    last_name: document.getElementById("last-name").value.trim(),
                    national_id: document.getElementById("national-id").value.trim(),
                    birth_date: document.getElementById("birth-date").value.trim(),
                    medical_id: document.getElementById("medical-id").value.trim(),
                    gender: document.getElementById("gender").value,
                    degree: document.getElementById("degree").value,
                    specialty: document.getElementById("specialty").value,
                    step: "register"
                };

                fetch("/api/doctor/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()},
                    body: JSON.stringify(formData)
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("ثبت‌نام با موفقیت انجام شد!");
                            window.location.href = "/";
                        } else {
                            alert(data.message || "ثبت‌نام ناموفق بود.");
                        }
                    })
                    .catch(error => console.error("خطا در ثبت‌نام:", error));
            });
        });
