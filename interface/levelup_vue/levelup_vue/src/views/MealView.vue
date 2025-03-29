<template>
  <div class="meal-dashboard">
    <div class="dashboard-card">
      <h2 class="card-title">Log a Meal with Multiple Items</h2>

      <!-- Meal Name Field -->
      <div class="input-group">
        <label for="meal_name">Meal Name</label>
        <input id="meal_name" type="text" v-model="mealName" placeholder="Enter meal name" class="input-field" />
      </div>

      <!-- Food Items Section -->
      <div v-for="(food, index) in foods" :key="index" class="food-section">
        <!-- Initial Search Bar -->
        <div v-if="!food.isExpanded" class="search-container">
          <input
            v-model="food.search"
            @input="debouncedSearch(index)"
            placeholder="Search food..."
            class="input-field"
          />
          <ul v-if="food.searchResults.length" class="results-list">
            <li
              v-for="item in food.searchResults"
              :key="item.food_id"
              @click="selectFood(index, item)"
              class="result-item"
            >
              {{ item.food }}
            </li>
          </ul>
          
          <!-- Manual Entry Button -->
          <button @click="enableManualEntry(index)" class="text-btn">
            Or enter manually
          </button>
        </div>

        <!-- Expanded Form after Selection -->
        <div v-if="food.isExpanded" class="expanded-form">
          <div class="form-header">
            <h3 class="food-title">{{ food.food_name || 'New Food Item' }}</h3>
            <button @click="removeFood(index)" class="delete-btn">
              <span class="delete-icon">×</span>
            </button>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>Food Name</label>
              <input type="text" v-model="food.food_name" placeholder="Food name" class="input-field" />
            </div>
            <div class="form-group">
              <label>Calories</label>
              <input type="number" v-model.number="food.calories" placeholder="0" class="input-field" />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>Protein (g)</label>
              <input type="number" v-model.number="food.protein" placeholder="0" class="input-field" />
            </div>
            <div class="form-group">
              <label>Carbs (g)</label>
              <input type="number" v-model.number="food.carbs" placeholder="0" class="input-field" />
            </div>
            <div class="form-group">
              <label>Fats (g)</label>
              <input type="number" v-model.number="food.fats" placeholder="0" class="input-field" />
            </div>
          </div>
        </div>
      </div>

      <!-- Only show Add Another Food button if at least one food item has been expanded -->
      <button 
        v-if="hasAtLeastOneExpandedFood" 
        @click="addFoodSection" 
        class="btn add-food-btn"
      >
        <span class="btn-icon">+</span> Add Another Food
      </button>

      <div class="input-group">
        <label for="description">Meal Notes</label>
        <textarea id="description" v-model="description" class="textarea-field"></textarea>
      </div>

      <button @click="logMeal" class="btn submit-btn">
        <span class="btn-icon">+</span> Log Meal
      </button>

      <div v-if="message" class="success-message">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      mealName: '',
      foods: [this.getEmptyFoodItem()],
      description: '',
      message: '',
    };
  },
  computed: {
    hasAtLeastOneExpandedFood() {
      // Returns true if at least one food item has been expanded
      return this.foods.some(food => food.isExpanded);
    }
  },
  methods: {
    getEmptyFoodItem() {
      return {
        food_name: '',
        calories: 0,
        protein: 0,
        carbs: 0,
        fats: 0,
        search: '',
        searchResults: [],
        isExpanded: false,
      };
    },
    async searchMeals(index) {
      const query = this.foods[index].search;
      if (query.length < 2) {
        this.foods[index].searchResults = [];
        return;
      }
      try {
        const response = await axios.get('/api/v1/meals/search/', {
          params: { q: query },
        });
        this.foods[index].searchResults = response.data;
      } catch (error) {
        console.error('Error searching meals:', error);
      }
    },
    debouncedSearch: debounce(function (index) {
      this.searchMeals(index);
    }, 300),
    selectFood(index, item) {
      this.foods[index] = {
        ...this.foods[index],
        food_name: item.food,
        calories: item.calories || 0,
        protein: item.proteins || 0,
        carbs: item.carbs || 0,
        fats: item.fats || 0,
        search: item.food,
        searchResults: [],
        isExpanded: true,
      };
    },
    enableManualEntry(index) {
      this.foods[index].isExpanded = true;
      this.foods[index].searchResults = [];
    },
    addFoodSection() {
      this.foods.push(this.getEmptyFoodItem());
    },
    removeFood(index) {
      if (this.foods.length > 1) {
        this.foods.splice(index, 1);
      } else {
        // If it's the last item, just reset it
        this.foods = [this.getEmptyFoodItem()];
      }
    },
    async logMeal() {
      // Filter out any empty or incomplete entries
      const validFoods = this.foods.filter(f => f.food_name.trim() !== '');
      
      if (validFoods.length === 0) {
        this.message = 'Please add at least one food item';
        setTimeout(() => (this.message = ''), 3000);
        return;
      }
      
      const payload = {
        username: localStorage.getItem('active_username'),
        meal_name: this.mealName || `Meal on ${new Date().toLocaleString()}`,
        description: this.description,
        foods: validFoods.map(f => ({
          food_name: f.food_name,
          calories: f.calories,
          protein: f.protein,
          carbs: f.carbs,
          fats: f.fats,
        })),
      };
      
      try {
        const res = await axios.post('/api/v1/meals/log/', payload);
        if (res.data.success) {
          this.message = res.data.message;
          this.mealName = '';
          this.foods = [this.getEmptyFoodItem()];
          this.description = '';
          setTimeout(() => (this.message = ''), 3000);
        }
      } catch (error) {
        console.error('Error logging meal:', error);
        this.message = 'Error saving meal. Please try again.';
        setTimeout(() => (this.message = ''), 3000);
      }
    },
  },
};

function debounce(func, wait = 300) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}
</script>

<style scoped>
.meal-dashboard {
  font-family: 'Segoe UI', sans-serif;
  max-width: 700px;
  margin: 3rem auto;
}

.dashboard-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  padding: 40px;
  transition: all 0.3s ease;
}

.card-title {
  font-size: 1.8rem;
  margin-bottom: 28px;
  color: #333;
  font-weight: 600;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.input-field {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  background-color: #fafafa;
  font-size: 14px;
  transition: all 0.2s ease;
  margin-bottom: 12px;
}

.input-field:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.textarea-field {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  background-color: #fafafa;
  min-height: 80px;
  font-size: 14px;
  transition: all 0.2s ease;
  resize: vertical;
}

.textarea-field:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.results-list {
  background: white;
  border-radius: 12px;
  border: 1px solid #eee;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  max-height: 150px;
  overflow-y: auto;
  margin: 0 0 16px 0;
  padding: 0;
  list-style: none;
  z-index: 10;
  position: relative;
}

.result-item {
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
  transition: background-color 0.2s ease;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover {
  background-color: #f8f8f8;
}

.form-row {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 80px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
  font-size: 14px;
}

.food-section {
  background-color: #fafafa;
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 20px;
  border: 1px solid #f0f0f0;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #a4e057;
  border: none;
  color: #333;
  font-weight: 600;
  padding: 14px 24px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 15px;
  box-shadow: 0 4px 10px rgba(164, 224, 87, 0.2);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(164, 224, 87, 0.25);
}

.btn:active {
  transform: translateY(1px);
}

.add-food-btn {
  background-color: white;
  border: 2px solid #a4e057;
  margin-bottom: 24px;
  animation: fadeIn 0.3s ease;
}

.btn-icon {
  margin-right: 8px;
  font-weight: bold;
}

.text-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 14px;
  text-decoration: underline;
  cursor: pointer;
  padding: 8px 0;
  display: block;
  text-align: left;
}

.text-btn:hover {
  color: #a4e057;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.food-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.delete-btn {
  background: none;
  border: none;
  color: #ff6b6b;
  cursor: pointer;
  font-size: 20px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.delete-btn:hover {
  background-color: #fff0f0;
}

.delete-icon {
  line-height: 1;
}

.expanded-form {
  animation: fadeIn 0.3s ease;
}

.success-message {
  margin-top: 20px;
  background: #f0fce9;
  padding: 16px;
  border-radius: 12px;
  color: #2e7d32;
  font-weight: 500;
  animation: fadeIn 0.3s ease;
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>