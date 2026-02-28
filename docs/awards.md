# Profiles & Awards

MeshMapper recognizes community contributors through a **Profiles & Awards** system. Every companion device/user that participates in wardriving gets a profile, and awards are granted automatically for milestones or manually by administrators for special contributions.

### Viewing Profiles

You can view any users profile by clicking their name on a regional or [global leaderboard](https://meshmapper.net/global_leaderboard.php). Leaderboards also have a "Profiles" search button in the header, which allows you to search for any companion by name or ID.

### Users

When a single person operates multiple companion devices in a region, that regions administrators can combine them into a **user group**. All devices in the group aggregate their points under a single primary companion. The group appears as one entry on the leaderboards, and the profile displays the combined statistics.  

### Roadmap

Eventually, profiles will expand to allow users to log in and manage their avatar, bio, social media links, and view and manage the data they have contributed.

## Awards

Awards are visual badges displayed on a companion's profile. They come in two types:

### Automatic Awards

These are granted automatically by the system based on wardriving milestones:

| Award | Criteria |
| --- | --- |
| **Wardriver** | Any wardriving contribution (at least 1 data point) |
| **1,000 Data Points** | Accumulate 1,000 or more all-time points |
| **5,000 Data Points** | Accumulate 5,000 or more all-time points |
| **10,000 Data Points** | Accumulate 10,000 or more all-time points |
| **50,000 Data Points** | Accumulate 50,000 or more all-time points |
| **Ping Leader** | Rank #1 on a regional leaderboard |
| **Explorer 1** | Map 1,000 or more unique grid squares |
| **Explorer 2** | Map 5,000 or more unique grid squares |
| **Explorer 3** | Map 10,000 or more unique grid squares |
| **Global Leader** | Rank in the top 10 on the global leaderboard (all-time, weekly, or top explorers) |

!!! info "Assignment Interval"
    MeshMapper processes the auto assignment of awards once every 24-hours.  Check back later if you've earned an award but don't yet see it.

### Manual Awards

Administrators can grant custom awards for special achievements, events, contest wins, donating to MeshMapper, or community contributions.

## Available Awards

The table below is a list of currently available awards to be earned:

<div id="awards-table-container">
  <p><em>Loading awards...</em></p>
</div>

<div id="award-img-modal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:9999;cursor:pointer;justify-content:center;align-items:center;" onclick="this.style.display='none'">
  <div style="position:relative;max-width:90vw;max-height:90vh;text-align:center;">
    <img id="award-img-modal-src" src="" alt="" style="max-width:400px;max-height:80vh;object-fit:contain;border-radius:8px;">
    <div id="award-img-modal-name" style="color:#fff;font-size:1.2rem;font-weight:600;margin-top:0.75rem;"></div>
  </div>
</div>

<script>
function openAwardImage(src, name) {
    var modal = document.getElementById('award-img-modal');
    document.getElementById('award-img-modal-src').src = src;
    document.getElementById('award-img-modal-src').alt = name;
    document.getElementById('award-img-modal-name').textContent = name;
    modal.style.display = 'flex';
}

(function() {
    var container = document.getElementById('awards-table-container');
    fetch('https://meshmapper.net/profile_api.php?action=awards')
        .then(function(r) { return r.json(); })
        .then(function(awards) {
            if (!awards || awards.length === 0) {
                container.innerHTML = '<p><em>No awards have been created yet.</em></p>';
                return;
            }
            var html = '<table>';
            html += '<thead><tr><th style="width:64px;">Icon</th><th>Award</th><th>Description</th><th>Awarded</th></tr></thead>';
            html += '<tbody>';
            awards.forEach(function(a) {
                var imgSrc = a.image_path
                    ? 'https://meshmapper.net/' + a.image_path
                    : 'https://meshmapper.net/img/default-award.svg';
                var escapedName = a.name.replace(/'/g, "\\'").replace(/"/g, '&quot;');
                var icon = '<img src="' + imgSrc + '" alt="' + a.name + '" style="width:128px;height:128px;object-fit:contain;cursor:pointer;" onclick="openAwardImage(\'' + imgSrc.replace(/'/g, "\\'") + '\', \'' + escapedName + '\')">';
                var desc = a.description || '—';
                var count = a.grant_count || 0;
                html += '<tr><td style="text-align:center;vertical-align:middle;">' + icon + '</td><td style="vertical-align:middle;"><strong>' + a.name + '</strong></td><td style="vertical-align:middle;">' + desc + '</td><td style="text-align:center;vertical-align:middle;">' + count + '</td></tr>';
            });
            html += '</tbody></table>';
            container.innerHTML = html;
        })
        .catch(function() {
            container.innerHTML = '<p><em>Unable to load awards. Please try again later.</em></p>';
        });
})();
</script>

## Request an Award or Suggest a New One

Use the form below to request a missing award or suggest a new award type for the community.

<div id="award-request-form" style="max-width:560px;">
  <div style="margin-bottom:1rem;">
    <label style="font-weight:600;">Request Type</label><br>
    <label style="cursor:pointer;margin-right:1rem;">
      <input type="radio" name="award_type" value="request" checked onchange="toggleCompanionField()"> Request Award
    </label>
    <label style="cursor:pointer;">
      <input type="radio" name="award_type" value="suggestion" onchange="toggleCompanionField()"> Award Suggestion
    </label>
  </div>

  <div style="margin-bottom:1rem;">
    <label for="award_name" style="font-weight:600;">Your Name</label><br>
    <input type="text" id="award_name" placeholder="Your name" style="width:100%;padding:8px;border:1px solid #555;border-radius:4px;background:#2b2b2b;color:#fff;box-sizing:border-box;">
  </div>

  <div id="companion-id-field" style="margin-bottom:1rem;">
    <label for="award_companion_id" style="font-weight:600;">Companion ID</label><br>
    <input type="text" id="award_companion_id" placeholder="Public ID of the companion" style="width:100%;padding:8px;border:1px solid #555;border-radius:4px;background:#2b2b2b;color:#fff;box-sizing:border-box;">
  </div>

  <div style="margin-bottom:1rem;">
    <label for="award_details" style="font-weight:600;">Details</label><br>
    <textarea id="award_details" rows="4" style="width:100%;padding:8px;border:1px solid #555;border-radius:4px;background:#2b2b2b;color:#fff;box-sizing:border-box;resize:vertical;"></textarea>
  </div>

  <button onclick="submitAwardRequest()" id="award-submit-btn" style="background:#00d2ff;color:#111;border:none;padding:10px 24px;border-radius:6px;font-weight:600;cursor:pointer;font-size:14px;">Submit</button>
  <div id="award-form-status" style="margin-top:0.75rem;"></div>
</div>

<script>
function toggleCompanionField() {
    var type = document.querySelector('input[name="award_type"]:checked').value;
    document.getElementById('companion-id-field').style.display = type === 'request' ? 'block' : 'none';
}

function submitAwardRequest() {
    var type = document.querySelector('input[name="award_type"]:checked').value;
    var name = document.getElementById('award_name').value.trim();
    var companionId = document.getElementById('award_companion_id').value.trim();
    var details = document.getElementById('award_details').value.trim();
    var status = document.getElementById('award-form-status');
    var btn = document.getElementById('award-submit-btn');

    if (!name) { status.innerHTML = '<span style="color:#dc3545;">Please enter your name.</span>'; return; }
    if (type === 'request' && !companionId) { status.innerHTML = '<span style="color:#dc3545;">Please enter a Companion ID.</span>'; return; }
    if (!details) { status.innerHTML = '<span style="color:#dc3545;">Please provide details.</span>'; return; }

    btn.disabled = true;
    btn.textContent = 'Submitting...';
    status.innerHTML = '';

    fetch('https://meshmapper.net/award_request.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            type: type,
            name: name,
            companion_id: companionId,
            details: details
        })
    })
    .then(function(r) { return r.json().then(function(d) { return { ok: r.ok, data: d }; }); })
    .then(function(res) {
        btn.disabled = false;
        btn.textContent = 'Submit';
        if (res.ok) {
            status.innerHTML = '<span style="color:#28a745;">' + res.data.message + '</span>';
            document.getElementById('award_name').value = '';
            document.getElementById('award_companion_id').value = '';
            document.getElementById('award_details').value = '';
        } else {
            status.innerHTML = '<span style="color:#dc3545;">' + (res.data.error || 'Something went wrong.') + '</span>';
        }
    })
    .catch(function() {
        btn.disabled = false;
        btn.textContent = 'Submit';
        status.innerHTML = '<span style="color:#dc3545;">Network error. Please try again.</span>';
    });
}
</script>
