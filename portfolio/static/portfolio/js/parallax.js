(function () {
    var prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    var frame = document.querySelector(".hero-frame");
    if (!frame || prefersReducedMotion) {
        return;
    }

    var layers = frame.querySelectorAll("[data-parallax-speed]");
    if (!layers.length) {
        return;
    }

    var maxShiftPx = 26;
    var easing = 0.09;
    var target = { x: 0, y: 0 };
    var current = { x: 0, y: 0 };
    var raf = null;

    function setTargetFromEvent(event) {
        var rect = frame.getBoundingClientRect();
        target.x = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
        target.y = ((event.clientY - rect.top) / rect.height - 0.5) * 2;
        requestTick();
    }

    function resetTarget() {
        target.x = 0;
        target.y = 0;
        requestTick();
    }

    function requestTick() {
        if (!raf) {
            raf = window.requestAnimationFrame(update);
        }
    }

    function update() {
        current.x += (target.x - current.x) * easing;
        current.y += (target.y - current.y) * easing;

        layers.forEach(function (layer) {
            var speed = parseFloat(layer.dataset.parallaxSpeed) || 0;
            var x = current.x * maxShiftPx * speed;
            var y = current.y * maxShiftPx * speed;
            layer.style.transform = "translate(" + x.toFixed(2) + "px, " + y.toFixed(2) + "px)";
        });

        var settled =
            Math.abs(target.x - current.x) < 0.001 &&
            Math.abs(target.y - current.y) < 0.001;

        if (settled) {
            raf = null;
        } else {
            raf = window.requestAnimationFrame(update);
        }
    }

    frame.addEventListener("mousemove", setTargetFromEvent);
    frame.addEventListener("mouseleave", resetTarget);
})();
