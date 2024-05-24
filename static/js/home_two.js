document.addEventListener('DOMContentLoaded', function () {
    const contentArea = document.getElementById('content-area');

    document.querySelectorAll('.sidebar .item a').forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default link behavior
            const contentId = this.getAttribute('data-content-id'); // Get the identifier for content

            switch (contentId) {
                case 'dashboard':
                    contentArea.innerHTML = '<h1>Dashboard Content</h1>';
                    break;
                case 'application-form':
                    loadContent(applicationFormUrl, contentArea);
                    break;
                case 'approved-loans':
                    loadContent(approvedLoansURL, contentArea);
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

function loadContent(url, container) {
    console.log(url);
    fetch(url)
        .then(response => response.text())
        .then(html => container.innerHTML = html)
        .catch(error => console.log('Failed to load page:', error));
}
