<template>
    <form action="login">
	<label for="username">Username:</label>
	<input id="username">
	<br>
	<label for="password">Password:</label>
	<input id="password" type="password">
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
