// Data for the doughnut chart
const data = {
	labels: ['Approved Loans', 'Rejected Loans', 'Pending Loans'],
	datasets: [{
		data: [5, 3, 1],
		backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56'],
		hoverBackgroundColor: ['#36A2EB', '#FF6384', '#FFCE56']
	}]
};

// config for the doughnut chart
const config = {
	type: 'doughnut',
	data: data,
	options: {
		responsive: true,
		maintainAspectRatio: false,
	}
};

// create the chart
const doughnutChartCtx = document.getElementById('doughnutChart').getContext('2d');
new Chart(doughnutChartCtx, config);
