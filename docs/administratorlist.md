# Administrator List

This page displays the current list of MeshMapper administrators.


## Current Administrators

<div id="admin-table-container">
    <em>Loading data from server...</em>
</div>

---

### Legend
* **Master Administrator**: Full system access and server control.
* **Global Administrator**: Moderator access across all regions.
* **Region Administrator**: Access to specific geographic regions.

<style>
    #admin-table-container {
        overflow-x: auto;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .admin-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.8em;
    }
    .admin-table th {
        background-color: #003366;
        color: #ffffff;
        padding: 5px;
        text-align: left;
        border: 1px solid #ddd;
    }
    .admin-table td {
        padding: 5px;
        border: 1px solid #ddd;
    }
    .loading-msg {
        padding: 20px;
        text-align: center;
        color: #666;
        font-style: italic;
    }
</style>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        fetch('https://meshmapper.net/pull_users.php')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let html = '<table class="admin-table"><thead><tr><th>Zone</th><th>Name</th><th>Contact Info</th></tr></thead><tbody>';
                    data.data.forEach(user => {

                        const safeZone = String(user.zone).replace(/</g, "&lt;").replace(/>/g, "&gt;");
                        const safeName = String(user.name).replace(/</g, "&lt;").replace(/>/g, "&gt;");
                        const safeContact = String(user.contact_info || '').replace(/</g, "&lt;").replace(/>/g, "&gt;");
                        
                        html += `<tr>
                            <td>${safeZone}</td>
                            <td>${safeName}</td>
                            <td>${safeContact}</td>
                        </tr>`;
                    });
                    html += '</tbody></table>';
                    document.getElementById('admin-table-container').innerHTML = html;
                } else {
                    document.getElementById('admin-table-container').innerHTML = '<div class="loading-msg">Unable to load administrator list.</div>';
                }
            })
            .catch(err => {
                console.error('Error fetching admin list:', err);
                document.getElementById('admin-table-container').innerHTML = '<div class="loading-msg">Error connecting to server.</div>';
            });
    });
</script>