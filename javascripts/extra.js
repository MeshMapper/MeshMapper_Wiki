document.addEventListener("DOMContentLoaded", function() {
    var headerInner = document.querySelector(".md-header__inner");
    if (headerInner) {
        var btn = document.createElement("a");
        btn.href = "https://meshmapper.net";
        btn.className = "nav-btn";
        btn.innerText = "Return to MeshMapper";
        headerInner.appendChild(btn);
    }
});