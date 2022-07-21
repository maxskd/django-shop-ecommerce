/* Simple validation on JS */
let form = document.querySelector('.register-form')
    formInputs = document.querySelectorAll('.form-control')
    inputEmail = document.querySelector('.email-input')
    inputPassword = document.querySelector('.password1').innerHTML
    inputPassword2 = document.querySelector('.password2').innerHTML

function emailValidate(email) {
    let emailRE = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return emailRE.test(String(email).toLowerCase());
}

form.onsubmit = function () {
    let emailValue = inputEmail.value
        emptyInputs = Array.from(formInputs).filter(input => input.value === '');

    if(inputPassword != inputPassword2){
        inputPassword.classList.add('input-error');
        inputPassword2.classList.add('input-error');
        console.log(document.querySelector('.password1'))
        console.log(document.querySelector('.password2'))
        return false
    }

    formInputs.forEach(function (input) {
        if (input.value == ''){
            input.classList.add('input-error');
        }
        else {
            input.classList.remove('input-error');
        }
    })

    if (emptyInputs.length !== 0){
        return false;
    }

    if(!validateEmail(emailValue)) {
        input.classList.add('input-error');
        return false;
    }
    else {
        input.classList.remove('input-error');
    }

}