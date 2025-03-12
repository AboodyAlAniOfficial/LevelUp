<template>
  <div class="login-dashboard">
    <div class="dashboard-card login-card">
      <h2 class="card-title">Welcome Back</h2>
      
      <transition name="fade">
        <div v-if="loginError" class="error-message">
          <span class="error-icon">!</span> Login failed. Please check your credentials.
        </div>
      </transition>
      
      <transition name="fade">
        <div v-if="registerError" class="error-message">
          <span class="error-icon">!</span> An account with this username already exists.
        </div>
      </transition>

      <form class="login-form">
        <div class="input-group">
          <label for="username">Username</label>
          <div class="input-wrapper">
            <input 
              id="username" 
              name="username" 
              v-model="username" 
              required
              class="form-input"
            />
            <span class="input-icon">👤</span>
          </div>
        </div>
        
        <div class="input-group">
          <label for="password">Password</label>
          <div class="input-wrapper">
            <input 
              id="password" 
              name="password" 
              type="password" 
              v-model="password" 
              required
              class="form-input"
            />
            <span class="input-icon">🔒</span>
          </div>
        </div>

        <div class="buttons-container">
          <button @click.prevent="login" class="submit-btn login-btn">
            <span class="btn-icon">→</span> Login
          </button>
          <button @click.prevent="register" class="submit-btn register-btn">
            <span class="btn-icon">+</span> Sign Up
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      loginError: false,
      registerError: false,
    };
  },
  methods: {
    async login() {
      try {
        this.loginError = false;
        this.registerError = false;
        // Note the updated URL for token login (no "auth/" in the path)
        const response = await axios.post('http://localhost:8000/api/v1/token/login/', {
          username: this.username,
          password: this.password,
        });
        if (response.data.auth_token) {
          localStorage.setItem('userToken', response.data.auth_token);
          localStorage.setItem('active_username', this.username);
          window.location.href = "/";
        } else {
          this.loginError = true;
        }
      } catch (error) {
        console.error('Error logging in:', error);
        this.loginError = true;
      }
    },
    async register() {
      try {
        this.loginError = false;
        this.registerError = false;
        // Using the custom registration endpoint from accounts app
        const response = await axios.post('http://localhost:8000/api/v1/accounts/register/', {
          username: this.username,
          password: this.password,
        });
        if (response.data.success) {
          // Automatically log in after successful registration
          await this.login();
        } else {
          this.registerError = true;
        }
      } catch (error) {
        console.error('Error registering:', error);
        this.registerError = true;
      }
    },
  },
};
</script>

<style scoped>
.login-dashboard {
  font-family: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
  max-width: 450px;
  margin: 4rem auto;
}

.dashboard-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  padding: 32px;
}

.card-title {
  color: #333;
  font-size: 1.75rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 28px;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

label {
  font-size: 14px;
  font-weight: 500;
  color: #555;
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  padding-right: 40px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.input-icon {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.buttons-container {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}

.submit-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 20px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
}

.login-btn {
  background-color: #a4e057;
  color: #333;
}

.login-btn:hover {
  background-color: #93cc4a;
  transform: translateY(-2px);
}

.register-btn {
  background-color: #f5f5f5;
  color: #555;
}

.register-btn:hover {
  background-color: #e8e8e8;
  transform: translateY(-2px);
}

.btn-icon {
  font-size: 18px;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding: 12px 16px;
  background-color: #fff0f0;
  border-radius: 12px;
  color: #d32f2f;
  font-weight: 500;
}

.error-icon {
  background-color: #d32f2f;
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
