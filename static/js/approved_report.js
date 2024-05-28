function toggleDetails(id) {
	var details = document.getElementById(id);
	if (details.style.display === "none" || details.style.display === "")
	{
		details.style.display = "table-row";
	} else {
		details.style.display = "none";
	}
}
