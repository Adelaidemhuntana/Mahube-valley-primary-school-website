document.getElementById("applicationForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const requestBody = {
        parent_name: document.getElementById("parentName").value,
        learner_name: document.getElementById("learnerName").value,
        grade: document.getElementById("grade").value,
        school_id: Number(document.getElementById("schoolId").value),
        home_distance_km: Number(document.getElementById("distance").value)
    };

    const result = document.getElementById("applicationResult");

    try {
        const response = await fetch("http://127.0.0.1:8000/applications", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(requestBody),
        });

        const data = await response.json();

        if (response.ok && data.offer) {
            result.innerHTML = `
                <div class="success-box">
                    <h2>Application Submitted</h2>
                    <p><strong>Application ID:</strong> ${data.application_id}</p>
                    <p><strong>Status:</strong> ${data.application_status}</p>
                    <p><strong>Offer ID:</strong> ${data.offer.offer_id}</p>
                    <p><strong>Offer Status:</strong> ${data.offer.status}</p>
                    <p><strong>Expires:</strong> ${new Date(data.offer.expires_at).toLocaleString()}</p>
                    <p>The learner is eligible and a school seat has been reserved for five days.</p>
                </div>
            `;
        } else if (response.ok) {
            result.innerHTML = `
                <div class="warning-box">
                    <h2>Application Submitted</h2>
                    <p><strong>Application ID:</strong> ${data.application_id}</p>
                    <p><strong>Status:</strong> ${data.application_status}</p>
                    <p>No offer was created yet. The learner may be outside the radius rule or waitlisted.</p>
                </div>
            `;
        } else {
            result.innerHTML = `<div class="warning-box"><p>${data.detail}</p></div>`;
        }
    } catch (error) {
        result.innerHTML = "<div class='warning-box'><p>The backend is not available.</p></div>";
    }
});
