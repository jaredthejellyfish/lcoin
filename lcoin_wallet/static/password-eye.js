const togglePassword = document.querySelector("#togglePassword");
const password = document.querySelector("#password");
const confirm_password = document.querySelector("#confirm-password");

togglePassword.addEventListener("click", function () {
  // toggle the type attribute
  const type =
    password.getAttribute("type") === "password" ? "text" : "password";

  password.setAttribute("type", type);
  try {
    confirm_password.setAttribute("type", type);
  } catch (e) {
    //pass
  }
  // toggle the icon
  this.classList.toggle("fa-eye-slash");
});
