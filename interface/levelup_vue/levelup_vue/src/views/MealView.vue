<template>
  <div class="meal-dashboard">
    <div class="dashboard-card search-card">
      <h2 class="card-title">Search and Log a Meal</h2>
      
      <div class="search-container">
        <div class="search-input-wrapper">
          <input 
            type="text" 
            v-model="searchQuery" 
            @input="searchMeals" 
            placeholder="Search for a meal..."
            class="search-input"
          />
          <span class="search-icon">🔍</span>
        </div>
        
        <transition name="fade">
          <ul v-if="searchResults.length" class="results-list">
            <li 
              v-for="meal in searchResults" 
              :key="meal.foodid" 
              @click="selectMeal(meal)"
              class="result-item"
            >
              {{ meal.fooddescription }}
            </li>
          </ul>
        </transition>
      </div>

      <!-- Selected meal details -->
      <transition name="fade">
        <div v-if="selectedMeal" class="meal-form-container">
          <div class="selected-meal">
            <div class="meal-icon">🍽️</div>
            <div class="meal-info">
              <h3>{{ selectedMeal.fooddescription }}</h3>
            </div>
          </div>

          <!-- Form to log the meal -->
          <form @submit.prevent="submitMeal" class="meal-form">
            <div class="form-row">
              <div class="input-group">
                <label for="meal-type">Meal Type</label>
                <div class="custom-select">
                  <select v-model="meal.meal_type" id="meal-type" required>
                    <option value="breakfast">Breakfast</option>
                    <option value="lunch">Lunch</option>
                    <option value="dinner">Dinner</option>
                    <option value="snack">Snack</option>
                  </select>
                </div>
              </div>
            </div>
            
            <div class="input-group">
              <label for="notes">Notes (optional)</label>
              <textarea 
                id="notes" 
                v-model="meal.notes" 
                placeholder="Add any details about your meal..."
                class="notes-textarea"
              ></textarea>
            </div>

            <button type="submit" class="submit-btn">
              <span class="btn-icon">+</span> Log Meal
            </button>
          </form>
        </div>
      </transition>

      <transition name="fade">
        <div v-if="message" class="success-message">
          <span class="success-icon">✓</span> {{ message }}
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
// A simple debounce function to limit API calls
function debounce(func, wait = 300) {
  let timeout;
  return function(...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), wait);
  };
}

import axios from 'axios';

export default {
  name: 'MealView',
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedMeal: null,
      
      meal: {
        predefined_meal: '',  // We'll set this to the selected meal's foodid
        meal_type: 'breakfast',
        notes: '',
      },
      message: '',
    };
  },
  created() {
    this.searchMeals = debounce(this.searchMeals, 300);
  },
  methods: {
    async searchMeals() {
      if (this.searchQuery.length < 2) {
        this.searchResults = [];
        return;
      }
      try {
        const response = await axios.get('/api/v1/meals/search/', {
          params: { q: this.searchQuery },
        });
        this.searchResults = response.data;
      } catch (error) {
        console.error('Error searching meals:', error);
      }
    },
    selectMeal(meal) {
      this.selectedMeal = meal;
      this.meal.predefined_meal = meal.foodid;
      // Set the search query to the selected meal description and clear the results.
      this.searchQuery = meal.fooddescription;
      this.searchResults = [];
    },
    async submitMeal() {
      try {
        const response = await axios.post('/api/v1/meals/create/', this.meal, {
          headers: {
            Authorization: `Token ${localStorage.getItem('userToken')}`,
          },
        });
        this.message = 'Meal logged successfully!';
        // Clear the message after a few seconds
        setTimeout(() => {
          this.message = '';
        }, 3000);
        this.resetForm();
      } catch (error) {
        console.error('Error logging meal:', error);
      }
    },
    resetForm() {
      this.selectedMeal = null;
      this.meal = {
        predefined_meal: '',
        meal_type: 'breakfast',
        notes: '',
      };
      this.searchQuery = '';
      this.searchResults = [];
    },
  },
};
</script>

<style scoped>
.meal-dashboard {
  font-family: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
  max-width: 600px;
  margin: 2rem auto;
}

.dashboard-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  padding: 24px;
  margin-bottom: 20px;
}

.card-title {
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 20px;
}

.search-container {
  position: relative;
  margin-bottom: 16px;
}

.search-input-wrapper {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.search-icon {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.results-list {
  list-style: none;
  margin: 4px 0 0;
  padding: 0;
  position: absolute;
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.result-item {
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.15s ease;
  border-bottom: 1px solid #f2f2f2;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover {
  background-color: #f9f9f9;
}

.meal-form-container {
  margin-top: 24px;
}

.selected-meal {
  display: flex;
  align-items: center;
  background-color: #f5fbf0;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.meal-icon {
  font-size: 24px;
  margin-right: 12px;
}

.meal-info h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

.meal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  gap: 16px;
}

.input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

label {
  font-size: 14px;
  font-weight: 500;
  color: #555;
  margin-bottom: 8px;
}

.custom-select {
  position: relative;
}

select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  appearance: none;
  background: url("data:image/svg+xml;utf8,<svg fill='%23888' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/></svg>") no-repeat;
  background-position: right 10px center;
  background-color: white;
}

select:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.notes-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  min-height: 80px;
  resize: vertical;
  font-family: inherit;
}

.notes-textarea:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  background-color: #a4e057;
  color: #333;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
  margin-top: 8px;
}

.submit-btn:hover {
  background-color: #93cc4a;
  transform: translateY(-2px);
}

.btn-icon {
  font-size: 20px;
  font-weight: bold;
}

.success-message {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 20px;
  padding: 12px 16px;
  background-color: #f0fce9;
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
