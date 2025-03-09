<template>
    <form id="login_form" action="http://localhost:8000/accounts/login/" method="POST">
	<label for="username">Username:</label>
	<input id="username" name="username" required>
	<br>
	<label for="password">Password:</label>
	<input id="password" name="password" type="password" required>
	<br>
        <input type="submit">
    </form>
</template>

<script>
export default {
  name: 'login',
  components: {}
}
</script>
