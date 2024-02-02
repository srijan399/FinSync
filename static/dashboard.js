let finalDate;

async function updateDateSelected(selectedDate) {
    const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
    };

    let dateString;
    if (selectedDate) {
        // Format the selected date
        finalDate = new Date(selectedDate);
        dateString = new Date(selectedDate).toLocaleDateString(
            "en-US",
            options
        );
    } else {
        // Format the current date
        finalDate = new Date();
        dateString = new Date().toLocaleDateString("en-US", options);
    }

    // Insert a comma after the weekday
    dateString = dateString.replace(/^(\w+)\s/, "$1, ");

    // Update the currentDate div
    document.getElementById("currentDate").textContent = dateString;
    document.getElementById("date").value = dateString;

    const date = new FormData();
    date.append('date', dateString); //equivalent to <input name="date" value=dateString>

    data = await fetch("http://127.0.0.1:5000/get_logs", {
        method: 'POST',
        body: date
    }).then(response => response.json());

    const table = document.getElementById("tabil");
    table.innerHTML = "";
    for (let i = 0; i < data.length; i++) {
        table.innerHTML += `<tr>
          <td>${data[i].desc}</td>
          <td>${data[i].amount}</td>
          </tr>`;
    }
}

// Set the current date on page load
window.onload = function () {
    updateDateSelected();
};

// Update the date when a new date is selected
document
    .getElementById("calendarInput")
    .addEventListener("change", function () {
        updateDateSelected(this.value);
    });

document.addEventListener("DOMContentLoaded", function () {
    var addButton = document.getElementById("addButton");
    var inputFields = document.getElementById("inputFields");
    var amountInput = document.getElementById("amount-taker");
    var reasonInput = document.getElementById("reason");
    var logForm = document.getElementById("logForm");

    addButton.addEventListener("click", function (event) {
        // Toggle input fields visibility
        if (inputFields.style.display === "none") {
            inputFields.style.display = "block";
            event.preventDefault(); // Prevent form submission
        } else {
            // Check if both fields are filled and amount is valid
            if (
                amountInput.value && reasonInput.value && amountInput.value >= 1
            ) {
                logForm.submit(); // Submit the form
            } else {
                alert(
                    "Please fill in both fields and ensure amount is at least 1."
                );
                event.preventDefault(); // Prevent form submission
            }
        }
    });
});