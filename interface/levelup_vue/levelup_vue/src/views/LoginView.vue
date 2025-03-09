<template>
    <p id="loginerr" class="error hidden"><em>Login failed.</em></p>
    <p id="registererr" class="error hidden"><em>An account with this username already exists.</em></p>
    <label for="username">Username:</label>
    <input id="username" name="username" required>
    <br>
    <label for="password">Password:</label>
    <input id="password" name="password" type="password" required>
    <br>
    <button @click="login" class="button is-dark">Login</button>
    <button @click="register" class="button is-dark">Sign Up</button>
</template>

<script>
 export default {
   name: 'login',
   components: {},
   methods: {
     login() {
       const xhr = new XMLHttpRequest();
       const url = "http://localhost:8000/accounts/login/"
       xhr.addEventListener("load", function(evt) {
         const response = JSON.parse(xhr.response);
         if (response["success"]) {
           localStorage.setItem("active_username", response["username"]);
           window.location.href = "/";
         } else {
           document.getElementById("loginerr").classList.remove("hidden");
           document.getElementById("registererr").classList.add("hidden");
         }
       });
       xhr.open("POST", url, false);

       const form_data = new FormData();
       form_data.append('username', document.getElementById("username").value);
       form_data.append('password', document.getElementById("password").value);
       xhr.send(form_data);
     },
     register() {
       const xhr = new XMLHttpRequest();
       const url = "http://localhost:8000/accounts/register/"
       xhr.addEventListener("load", function(evt) {
         const response = JSON.parse(xhr.response);
         if (response["success"]) {
           localStorage.setItem(
             "active_username", document.getElementById("username").value);
           window.location.href = "/";
         } else {
           document.getElementById("loginerr").classList.add("hidden");
           document.getElementById("registererr").classList.remove("hidden");
         }
       });
       xhr.open("POST", url, false);

       const form_data = new FormData();
       form_data.append('username', document.getElementById("username").value);
       form_data.append('password', document.getElementById("password").value);
       xhr.send(form_data);
    }
  }
}
</script>

<style>
.error {
    color: #ff0000;
 }

.hidden {
    display: none;
 }
</style>
