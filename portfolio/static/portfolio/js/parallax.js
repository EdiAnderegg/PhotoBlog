(function () {
    var prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReducedMotion) {
        return;
    }

    var layers = document.querySelectorAll("[data-parallax-speed]");
    if (!layers.length) {
        return;
    }

    var ticking = false;

    function update() {
        var scrollY = window.scrollY;
        layers.forEach(function (layer) {
            var speed = parseFloat(layer.dataset.parallaxSpeed) || 0;
            layer.style.transform = "translateY(" + scrollY * speed + "px)";
        });
        ticking = false;
    }

    window.addEventListener("scroll", function () {
        if (!ticking) {
            window.requestAnimationFrame(update);
            ticking = true;
        }
    });
})();
