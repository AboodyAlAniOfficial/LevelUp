<template>
  <div class="login-dashboard">
    <div v-if="!isLoggedIn" class="dashboard-card login-card">
      <h2 class="card-title">Welcome Back</h2>
      
      <transition name="fade">
        <div v-if="loginError" class="error-message">
          <span class="error-icon">!</span> Login failed. Please check your credentials.
        </div>
      </transition>
      
      <transition name="fade">
        <div v-if="registerError" class="error-message">
          <span class="error-icon">!</span> {{ registerErrorMessage }}
        </div>
      </transition>

      <form class="login-form">
        <div class="input-group">
          <label for="username">Username</label>
          <div class="input-wrapper">
            <input 
              id="username" 
              name="username" 
              v-model="loginForm.username" 
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
              v-model="loginForm.password" 
              required
              class="form-input"
            />
            <span class="input-icon">🔒</span>
          </div>
        </div>

        <div v-if="showConfirmPassword" class="input-group">
          <label for="confirmPassword">Confirm Password</label>
          <div class="input-wrapper">
            <input 
              id="confirmPassword" 
              name="confirmPassword" 
              type="password" 
              v-model="registerForm.confirmPassword" 
              required
              class="form-input"
            />
            <span class="input-icon">🔒</span>
          </div>
        </div>

        <div class="buttons-container">
          <button @click.prevent="handleLogin" class="submit-btn login-btn">
            <span class="btn-icon">→</span> Login
          </button>
          <button @click.prevent="handleRegister" class="submit-btn register-btn">
            <span class="btn-icon">+</span> Sign Up
          </button>
        </div>
      </form>
    </div>

    <!-- Unit Preferences Section -->
    <div v-if="isLoggedIn" class="dashboard-card preferences-card">
      <div class="card-header">
        <h2 class="card-title">Unit Preferences</h2>
        <button @click="logout" class="logout-btn">
          <span class="btn-icon">←</span> Logout
        </button>
      </div>
      
      <p class="welcome-message">Welcome, <strong>{{ username }}</strong></p>

      <div class="preferences-section">
        <!-- Length Unit Preference -->
        <div class="preference-group">
          <h3 class="preference-title">Length Unit</h3>
          <div class="preference-controls">
            <div class="select-wrapper">
              <select v-model="units.length" class="preference-select">
                <option value="meters">Meters</option>
                <option value="feet">Feet</option>
                <option value="inches">Inches</option>
                <option value="kilometers">Kilometers</option>
                <option value="miles">Miles</option>
              </select>
              <span class="select-icon">▼</span>
            </div>
            <button @click="saveUnit('length')" class="save-btn">
              <span class="btn-icon">💾</span> Save
            </button>
          </div>
        </div>

        <!-- Mass Unit Preference -->
        <div class="preference-group">
          <h3 class="preference-title">Mass Unit</h3>
          <div class="preference-controls">
            <div class="select-wrapper">
              <select v-model="units.mass" class="preference-select">
                <option value="kilograms">Kilograms</option>
                <option value="pounds">Pounds</option>
                <option value="grams">Grams</option>
                <option value="ounces">Ounces</option>
              </select>
              <span class="select-icon">▼</span>
            </div>
            <button @click="saveUnit('mass')" class="save-btn">
              <span class="btn-icon">💾</span> Save
            </button>
          </div>
        </div>

        <!-- Energy Unit Preference -->
        <div class="preference-group">
          <h3 class="preference-title">Energy Unit</h3>
          <div class="preference-controls">
            <div class="select-wrapper">
              <select v-model="units.energy" class="preference-select">
                <option value="joules">Joules</option>
                <option value="calories">Calories</option>
                <option value="kilowatt-hours">Kilowatt-hours</option>
                <option value="btu">BTU</option>
              </select>
              <span class="select-icon">▼</span>
            </div>
            <button @click="saveUnit('energy')" class="save-btn">
              <span class="btn-icon">💾</span> Save
            </button>
          </div>
        </div>
      </div>
      
      <transition name="fade">
        <div v-if="saveSuccess" class="success-message">
          <span class="success-icon">✓</span> Unit preference saved successfully!
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AccountsApp',
  data() {
    return {
      isLoggedIn: false,
      username: '',
      showConfirmPassword: false,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        confirmPassword: ''
      },
      units: {
        length: '',
        mass: '',
        energy: ''
      },
      loginError: false,
      registerError: false,
      registerErrorMessage: 'An account with this username already exists.',
      saveSuccess: false,
      saveTimeout: null
    };
  },
  methods: {
    async handleLogin() {
      try {
        this.loginError = false;
        this.registerError = false;
        
        const formData = new FormData();
        formData.append('username', this.loginForm.username);
        formData.append('password', this.loginForm.password);
        
        const response = await axios.post('/accounts/login/', formData);
        
        if (response.data.success) {
          this.isLoggedIn = true;
          this.username = response.data.username;
          this.fetchAllUnits();
          this.resetForms();
        } else {
          this.loginError = true;
        }
      } catch (error) {
        console.error('Login error:', error);
        this.loginError = true;
      }
    },
    
    async handleRegister() {
      if (!this.showConfirmPassword) {
        this.showConfirmPassword = true;
        this.registerForm.username = this.loginForm.username;
        this.registerForm.password = this.loginForm.password;
        return;
      }
      
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        this.registerError = true;
        this.registerErrorMessage = 'Passwords do not match.';
        return;
      }
      
      try {
        this.loginError = false;
        this.registerError = false;
        
        const formData = new FormData();
        formData.append('username', this.registerForm.username);
        formData.append('password', this.registerForm.password);
        
        const response = await axios.post('/accounts/register/', formData);
        
        if (response.data.success) {
          // Auto login after successful registration
          this.loginForm.username = this.registerForm.username;
          this.loginForm.password = this.registerForm.password;
          this.showConfirmPassword = false;
          this.handleLogin();
        } else {
          this.registerError = true;
          this.registerErrorMessage = 'An account with this username already exists.';
        }
      } catch (error) {
        console.error('Registration error:', error);
        this.registerError = true;
        this.registerErrorMessage = 'An error occurred during registration.';
      }
    },
    
    logout() {
      this.isLoggedIn = false;
      this.username = '';
      this.units = {
        length: '',
        mass: '',
        energy: ''
      };
      this.resetForms();
    },
    
    resetForms() {
      this.loginForm = {
        username: '',
        password: ''
      };
      this.registerForm = {
        username: '',
        password: '',
        confirmPassword: ''
      };
      this.showConfirmPassword = false;
    },
    
    async fetchUnit(dimension) {
      try {
        const response = await axios.get(`/accounts/unit/?username=${this.username}&dimension=${dimension}`);
        if (response.data && response.data !== "No units set for this user.") {
          this.units[dimension] = response.data;
        }
      } catch (error) {
        console.error(`Error fetching ${dimension} unit:`, error);
      }
    },
    
    fetchAllUnits() {
      this.fetchUnit('length');
      this.fetchUnit('mass');
      this.fetchUnit('energy');
    },
    
    async saveUnit(dimension) {
      try {
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('dimension', dimension);
        formData.append('unitname', this.units[dimension]);
        
        await axios.post('/accounts/unit/', formData);
        
        // Show success message and hide after 3 seconds
        this.saveSuccess = true;
        if (this.saveTimeout) {
          clearTimeout(this.saveTimeout);
        }
        this.saveTimeout = setTimeout(() => {
          this.saveSuccess = false;
        }, 3000);
      } catch (error) {
        console.error(`Error saving ${dimension} unit:`, error);
      }
    }
  }
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

.success-message {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 20px;
  padding: 12px 16px;
  background-color: #f0fff0;
  border-radius: 12px;
  color: #2e7d32;
  font-weight: 500;
}

.success-icon {
  background-color: #2e7d32;
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

/* Preferences Card Styles */
.preferences-card {
  margin-top: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.welcome-message {
  font-size: 16px;
  color: #555;
  margin-bottom: 24px;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background-color: #f5f5f5;
  border: none;
  border-radius: 12px;
  color: #555;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background-color: #e8e8e8;
  transform: translateY(-2px);
}

.preferences-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.preference-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preference-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.preference-controls {
  display: flex;
  gap: 12px;
}

.select-wrapper {
  position: relative;
  flex: 1;
}

.preference-select {
  width: 100%;
  padding: 12px 16px;
  padding-right: 36px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  appearance: none;
  background-color: white;
  cursor: pointer;
}

.preference-select:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.select-icon {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  pointer-events: none;
}

.save-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background-color: #a4e057;
  border: none;
  border-radius: 12px;
  color: #333;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-btn:hover {
  background-color: #93cc4a;
  transform: translateY(-2px);
}

@media (max-width: 480px) {
  .login-dashboard {
    margin: 2rem 1rem;
  }
  
  .dashboard-card {
    padding: 24px;
  }
  
  .buttons-container {
    flex-direction: column;
  }
  
  .preference-controls {
    flex-direction: column;
  }
}
</style>