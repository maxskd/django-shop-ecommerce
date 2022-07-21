/* Use observer to show block when user scroll down */
window.onload = () => {
    function entries(entry) {
        entry.forEach(change => {
            if (change.isIntersecting) {
                change.target.style.opacity = 1;
                change.target.classList.add('element-show')
            }
        })
    }

    let options = {
        threshold: [0.5]
    };
    let observer = new IntersectionObserver(entries, options);
    let elements = document.querySelectorAll('.animation-block');

    for (let e of elements) {
        observer.observe(e)
    }
}