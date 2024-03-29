// eye button func
const showPassword = document.querySelector("#show-password");
const passwordField = document.querySelector("#password");

showPassword.addEventListener("click", function () {
    this.classList.toggle("fa-eye-slash");
    const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
    passwordField.setAttribute("type", type);
})

function checkPasswordMatch() {
    const password = document.getElementById("password").value;
    const cnfrmpassword = document.getElementById("cnfrmpw").value;

    const message = document.getElementById("message");
    const signupbtn = document.getElementById("signup-button");

    if (password !== '' && cnfrmpassword != '') {
        if (password === cnfrmpassword) {
            message.textContent = ' ';
            signupbtn.removeAttribute('disabled');
            signupbtn.style.cursor = "pointer";
        }

        else {
            message.textContent = 'Passwords do not match';
            signupbtn.style.cursor = "not-allowed";
            signupbtn.setAttribute('disabled', 'true');
        }
    }
}