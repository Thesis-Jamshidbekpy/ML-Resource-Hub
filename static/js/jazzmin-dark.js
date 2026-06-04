/**
 * Force SOSbot-style dark admin (Jazzmin 3 / AdminLTE 4).
 * Runs before paint when placed in head via inline would be ideal;
 * custom_js loads at end of body — still sets mode for next navigation.
 */
(function () {
    var root = document.documentElement;
    root.setAttribute("data-bs-theme", "dark");
    try {
        localStorage.setItem("jazzmin-theme-mode", "dark");
    } catch (e) { /* private browsing */ }
})();
