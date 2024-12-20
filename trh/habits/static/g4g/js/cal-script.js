// script.js

// Function to generate a range of
// years for the year select input
function generate_year_range(start, end) {
	let years = "";
	for (let year = start; year <= end; year++) {
		years += "<option value='" +
			year + "'>" + year + "</option>";
	}
	return years;
}

// Initialize date-related letiables
today = new Date();
currentMonth = today.getMonth();
currentYear = today.getFullYear();

// Call the showCalendar function initially to display the calendar
window.addEventListener('DOMContentLoaded', function() {

	createYear = generate_year_range(1970, 2050);

	document.getElementById("year").innerHTML = createYear;

	$dataHead = "<tr>";
	for (dhead in days) {
		$dataHead += "<th data-days='" +
			days[dhead] + "'>" +
			days[dhead] + "</th>";
	}
	$dataHead += "</tr>";

	document.getElementById("thead-month").innerHTML = $dataHead;

	monthAndYear = document.getElementById("monthAndYear");
	showCalendar(currentMonth, currentYear);
});

let calendar = document.getElementById("calendar");

let months = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December"
];
let days = [
	"Sun", "Mon", "Tue", "Wed",
	"Thu", "Fri", "Sat"];


// Function to navigate to the next month
function next() {
	let selectYear = document.getElementById("year");
	let selectMonth = document.getElementById("month");
	let currentYear = parseInt(selectYear.value);
	let currentMonth = parseInt(selectMonth.value);
	currentYear = currentMonth === 11 ?
		currentYear + 1 : currentYear;
	currentMonth = (currentMonth + 1) % 12;
	showCalendar(currentMonth, currentYear);
}

// Function to navigate to the previous month
function previous() {
	let selectYear = document.getElementById("year");
	let selectMonth = document.getElementById("month");
	let currentYear = parseInt(selectYear.value);
	let currentMonth = parseInt(selectMonth.value);
	currentYear = currentMonth === 0 ?
		currentYear - 1 : currentYear;
	currentMonth = currentMonth === 0 ?
		11 : currentMonth - 1;
	showCalendar(currentMonth, currentYear);
}

// Function to jump to a specific month and year
function jump() {
	let selectYear = document.getElementById("year");
	let selectMonth = document.getElementById("month");
	let currentYear = parseInt(selectYear.value);
	let currentMonth = parseInt(selectMonth.value);
	showCalendar(currentMonth, currentYear);
}

// Function to display the calendar
function showCalendar(month, year) {
	let selectYear = document.getElementById("year");
	let selectMonth = document.getElementById("month");
	let firstDay = new Date(year, month, 1).getDay();
	let tbl = document.getElementById("calendar-body");
	tbl.innerHTML = "";
	monthAndYear.innerHTML = months[month] + " " + year;
	selectYear.value = year;
	selectMonth.value = month;

	let date = 1;
	for (let i = 0; i < 6; i++) {
		let row = document.createElement("tr");
		for (let j = 0; j < 7; j++) {
			if (i === 0 && j < firstDay) {
				cell = document.createElement("td");
				cellText = document.createTextNode("");
				cell.appendChild(cellText);
				row.appendChild(cell);
			} else if (date > daysInMonth(month, year)) {
				break;
			} else {
				cell = document.createElement("td");
				cell.setAttribute("data-date", date);
				cell.setAttribute("data-month", month + 1);
				cell.setAttribute("data-year", year);
				cell.setAttribute("data-month_name", months[month]);
				cell.className = "date-picker";
				cell.innerHTML = "<span>" + date + "</span";

				if (
					date === today.getDate() &&
					year === today.getFullYear() &&
					month === today.getMonth()
				) {
					cell.className = "date-picker selected";
				}

				// Check if there are events on this date
				// if (hasEventOnDate(date, month, year)) {
				// 	cell.classList.add("event-marker");
				// 	cell.appendChild(
				// 		createEventTooltip(date, month, year)
				// );
				// }

				row.appendChild(cell);
				date++;
			}
		}
		tbl.appendChild(row);
	}
}


// Function to get events on a specific date
function getEventsOnDate(date, month, year) {
	return events.filter(function (event) {
		let eventDate = new Date(event.date);
		return (
			eventDate.getDate() === date &&
			eventDate.getMonth() === month &&
			eventDate.getFullYear() === year
		);
	});
}

// Function to check if there are events on a specific date
function hasEventOnDate(date, month, year) {
	return getEventsOnDate(date, month, year).length > 0;
}

// Function to get the number of days in a month
function daysInMonth(iMonth, iYear) {
	return 32 - new Date(iYear, iMonth, 32).getDate();
}
