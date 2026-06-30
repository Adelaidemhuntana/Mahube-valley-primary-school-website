async function loadDashboard() {
  try {
    const summaryResponse = await fetch("/analytics/capacity-summary");
    const summary = await summaryResponse.json();

    document.getElementById("totalApplications").textContent = formatNumber(
      summary.total_applications,
    );
    document.getElementById("totalSchools").textContent = formatNumber(
      summary.total_schools,
    );
    document.getElementById("gradeCapacity").textContent = formatNumber(
      summary.grade_1_capacity,
    );
    document.getElementById("availableSeats").textContent = formatNumber(
      summary.available_seats,
    );
    document.getElementById("underOffer").textContent = formatNumber(
      summary.under_offer_seats,
    );
    document.getElementById("takenSeats").textContent = formatNumber(
      summary.taken_seats,
    );
    document.getElementById("unplacedLearners").textContent = formatNumber(
      summary.unplaced_learners,
    );

    const schoolsResponse = await fetch("/schools");
    const schools = await schoolsResponse.json();
    const mainSchool = schools.find((school) => school.school_id === 1);

    if (mainSchool) {
      document.getElementById("seatAvailable").textContent =
        mainSchool.available_seats;
      document.getElementById("seatOffer").textContent =
        mainSchool.under_offer_seats;
      document.getElementById("seatTaken").textContent = mainSchool.taken_seats;
    }
  } catch (error) {
    console.log("Dashboard fallback mode.");
  }
}

function formatNumber(value) {
  return Number(value || 0).toLocaleString();
}

function createClassSeatMap(
  elementId,
  className,
  available,
  reserved,
  taken,
  blocked,
) {
  const element = document.getElementById(elementId);
  const seats = [];

  for (let i = 0; i < available; i++) seats.push("available");
  for (let i = 0; i < reserved; i++) seats.push("reserved");
  for (let i = 0; i < taken; i++) seats.push("taken");
  for (let i = 0; i < blocked; i++) seats.push("blocked");

  element.innerHTML = `
        <h4>${className}</h4>
        <small>30 desks</small>
        <div class="desk-grid">
            ${seats.map((status) => `<span class="desk ${status}"></span>`).join("")}
        </div>
        <p>Available ${available}. Under Offer ${reserved}. Taken ${taken}</p>
    `;
}

async function acceptOffer() {
  const response = await fetch("/offers/1/accept", { method: "POST" });

  if (response.ok) {
    alert("Offer accepted. Seat secured.");
    await loadDashboard();
  } else {
    alert(
      "This offer may already be accepted. Reset the database if you want to test again.",
    );
  }
}

createClassSeatMap("classA", "Grade 1A", 6, 2, 7, 15);
createClassSeatMap("classB", "Grade 1B", 5, 3, 7, 15);
createClassSeatMap("classC", "Grade 1C", 4, 2, 8, 16);
createClassSeatMap("classD", "Grade 1D", 3, 5, 7, 15);

loadDashboard();

async function loadDataQualityReport() {
  try {
    const response = await fetch("/analytics/data-quality");
    const data = await response.json();

    document.getElementById("dataQualityStatus").textContent = data.status;
    document.getElementById("dataQualitySchools").textContent =
      data.total_schools;
    document.getElementById("dataQualityApplications").textContent =
      data.total_applications;

    document.getElementById("missingSchoolNames").textContent =
      data.checks.missing_school_names;
    document.getElementById("invalidSeatValues").textContent =
      data.checks.invalid_seat_values;
    document.getElementById("capacityMismatch").textContent =
      data.checks.capacity_mismatch;
    document.getElementById("missingParentNames").textContent =
      data.checks.missing_parent_names;

    document.getElementById("dataQualityMessage").textContent = data.message;
  } catch (error) {
    document.getElementById("dataQualityStatus").textContent = "ERROR";
    document.getElementById("dataQualityMessage").textContent =
      "Could not load data quality report.";
  }
}

loadDataQualityReport();