// approved_report JS
function toggleDetails(id) {
	var details = document.getElementById(id);
	if (details.style.display === "none" || details.style.display === "") {
		details.style.display = "table-row";
	} else {
		details.style.display = "none";
	}
}


// HOME_TWO JS
document.addEventListener('DOMContentLoaded', function () {
    const contentArea = document.getElementById('content-area');

    document.querySelectorAll('.sidebar .item a').forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default link behavior
            const contentId = this.getAttribute('data-content-id'); // Get the identifier for content

            switch (contentId) {
                case 'dashboard':
                    loadContent(dashboardUrl, contentArea, true); // flag to load dashboard js
                    break;
                case 'application-form':
                    loadContent(applicationFormUrl, contentArea);
                    break;
                case 'approved-loans':
                    loadContent(approvedLoansUrl, contentArea);
                    break;
                case 'rejected-loans':
                    loadContent(rejectedLoansUrl, contentArea);
                    break;
                case 'all-loans':
                    loadContent(allLoansUrl, contentArea);
                    break;
                case 'settings':
                    loadContent(settingsUrl, contentArea);
                    break;
                default:
                    contentArea.innerHTML = '<p>Select a menu item to see its content.</p>';
            }
        });
    });
});

function loadContent(url, container, loadDashboardJS = false) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
		container.innerHTML = html;
		reinitializeEventListeners(); // reattach listeners
		if (loadDashboardJS) {
			loadChartJs(function () {
				loadDashboardScript(); // load dashboard JS if required
			});
		}
	})
        .catch(error => console.log('Failed to load page:', error));
}

function loadDashboardScript() {
	const existingScript = document.querySelector('script[src="${dashboardScriptUrl}"]');
	if (existingScript) {
		existingScript.remove(); // Remove existing script if any to reload it
	}

	const script = document.createElement('script');
	script.src = dashboardScriptUrl;
	script.onload = function () {
		console.log('Dashboard JS loaded successfully');
	}
	document.body.appendChild(script);
}

// Function to dynamically load Chart.js if not already loaded
function loadChartJs(callback) {
	    if (typeof Chart !== 'undefined') {
		    // Chart.js is already loaded
		    if (callback) callback();
		    return;
	    }

	const script = document.createElement('script');
	script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
	script.onload = callback;
	document.head.appendChild(script);
}

// reinitialize approved loans JS listeners
function reinitializeEventListeners() {
	document.querySelectorAll('.details-toggle').forEach(item => {
		item.addEventListener('click', function (event) {
			const id = this.getAttribute('data-details-id');
			toggleDetails(id);
		});
	});
}
