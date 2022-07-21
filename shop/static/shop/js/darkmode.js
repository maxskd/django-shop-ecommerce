var loader = document.getElementById("preloader")
window.addEventListener("load", function(){
    document.getElementsByTagName("html")[0].style.visibility = "visible";
})
/* Change dark mode on click the button, and save results in local storage */
let darkMode = localStorage.getItem('darkMode');

const darkModeToggle = document.querySelector('#dark-mode-toggle');

const enableDarkMode = () => {
    document.getElementsByTagName("html")[0].style.visibility = "hidden"
    document.body.classList.add('darkmode');
    localStorage.setItem('darkMode','enabled');
}

const disableDarkMode = () => {
    document.getElementsByTagName("html")[0].style.visibility = "hidden"
    document.body.classList.remove('darkmode');
    localStorage.setItem('darkMode',null);
}

if (darkMode === 'enabled' ) {
    enableDarkMode();
}

darkModeToggle.addEventListener('click', () => {
    darkMode = localStorage.getItem('darkMode');
    if(darkMode !== 'enabled'){
        enableDarkMode();
    }
    else {
        disableDarkMode();
    }
});