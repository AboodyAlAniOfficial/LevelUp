<template>
    <label for="username">Username:</label>
    <input id="username" name="username" required>
    <br>
    <label for="password">Password:</label>
    <input id="password" name="password" type="password" required>
    <br>
    <button @click="login">Login</button>
</template>

<script>
 export default {
   name: 'login',
   components: {},
   methods: {
     login() {
       console.log("Logging in...");
       const xhr = new XMLHttpRequest();
       const url = "http://localhost:8000/accounts/login/"
       xhr.addEventListener("load", function(evt) {
         console.log(xhr.response);
         const response = JSON.parse(xhr.response);
         if (response["success"]) {
           console.log("success");
           localStorage.setItem("active_username", response["username"]);
           window.location.href = "/";
         } else {
           console.log("failure");
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
