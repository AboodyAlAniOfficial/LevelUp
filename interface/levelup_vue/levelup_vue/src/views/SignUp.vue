<template>
    <div class="sign-up-page">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Sign Up</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="text" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="field">
                        <label>Confirm Password</label>
                        <div class="control">
                            <input type="text" class="input" v-model="password2">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Sign Up</button>
                        </div>
                    </div>

                    <hr>

                    Or <router-link to="/login">click here</router-link> to log in!
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'signUp',
    data() {
        return {
            username: '',
            password: '',
            password2: '',
            errors: []
        }
    },
    methods: {
        submitForm() {
            this.errors=[]

            if (this.username==='') {
                this.errors.push('Missing Username!')
            }

            if (this.password.length <= 8) {
                this.errors.push('Password is too short!')
            }

            if (this.password !== this.password2) {
                this.errors.push('Passwords doesn\'t match!')
            }

            if (!this.errors.length) {
                const formData ={
                    username: this.username,
                    password: this.password
                }

                axios
                    .post("api/v1/users/", formData)
                    .then(response => {
                        toast({
                            message: 'Account created, please log in!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })
                        this.$router.push('/login')
                    })
                    .catch(error => {
                        if(error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }

                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again.')
                            console.log(JSON.stringify(error))
                        }
                    })
            }
        }
    }
}
</script>