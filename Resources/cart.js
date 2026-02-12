const COURSE_CONFIG = {
  "fundamentals-of-facebook-ads": {
    name: "Fundamentals of Facebook Ads",
    amount: 999,
    thankYouPage: "/fundamentals-of-facebook-ads/thankyou",
  },
  "business-growth-plan": {
    name: "Business Growth Plan",
    amount: 49991,
    thankYouPage: "/psychology-driven-advanced-meta-ad-course/business-growth-plan/thankyou",
  },
  "value-plan": {
    name: "Value Plan",
    amount: 14991,
    thankYouPage: "/psychology-driven-advanced-meta-ad-course/value-plan/thankyou",
  },
  "meta-andromeda-base": {
    name: "Meta Andromeda Base",
    amount: 1491,
    thankYouPage: "/master-creative-targeting/base-plan/thankyou",
  },
  "meta-andromeda-mentorship": {
    name: "Meta Andromeda Mentorship",
    amount: 4991,
    thankYouPage: "/master-creative-targeting/mentorship-plan/thankyou",
  },
};

async function initializeRazorpayPayment(courseId) {
  const fullName = document.querySelector('.form-input[type="text"]').value.trim();
  const countryCode = document.getElementById("country-code").value;
  const phoneNumber = document.querySelector(".phone-input").value.trim();
  const email = document.querySelector('.form-input[type="email"]').value.trim();

  if (!fullName || !phoneNumber || !email) {
    alert("Please fill in all required fields.");
    return;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address.");
    return;
  }

  const phone = countryCode + phoneNumber;
  const course = COURSE_CONFIG[courseId];

  if (!course) {
    alert("Invalid course selection.");
    return;
  }

  try {
    const response = await fetch("/api/create-order", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        course_id: courseId,
        name: fullName,
        email: email,
        phone: phone,
      }),
    });

    const data = await response.json();

    if (!data.success) {
      alert("Failed to create order. Please try again.");
      return;
    }

    const options = {
      key: data.key_id,
      amount: data.amount,
      currency: data.currency,
      name: "ROAS School of Marketing",
      description: data.course_name,
      order_id: data.order_id,
      handler: async function (response) {
        const verifyResponse = await fetch("/api/verify-payment", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
            course_id: courseId,
            name: fullName,
            email: email,
            phone: phone,
          }),
        });

        const verifyData = await verifyResponse.json();

        if (verifyData.success) {
          window.location.href = course.thankYouPage;
        } else {
          alert("Payment verification failed. Please contact support.");
        }
      },
      prefill: {
        name: data.prefill.name,
        email: data.prefill.email,
        contact: data.prefill.contact,
      },
      theme: {
        color: "#6366f1",
      },
      modal: {
        ondismiss: function () {
          console.log("Payment modal closed");
        },
      },
    };

    const rzp = new Razorpay(options);
    rzp.on("payment.failed", function (response) {
      alert("Payment failed. Please try again.");
      console.error(response.error);
    });
    rzp.open();
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
}
