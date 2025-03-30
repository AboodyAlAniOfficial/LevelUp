<template>
  <div class="meal-dashboard">
    <div class="dashboard-card">
      <!-- View All Meals Button -->
      <button @click="showMealModal = true" class="btn view-meals-btn">
        View All Meals
      </button>

      <h2 class="card-title">Meal Logger</h2>

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
        <span class="btn-icon">+</span> {{ isEditing ? 'Update Meal' : 'Log Meal' }}
      </button>

      <div v-if="message" class="success-message">
        {{ message }}
      </div>
    </div>

    <!-- Modal: View Logged Meals (UPDATED) -->
    <div v-if="showMealModal" class="modal-overlay">
      <div class="modal-content">
        <h3 class="modal-title">Your Logged Meals</h3>
        <button class="close-btn" @click="showMealModal = false">×</button>

        <div v-if="allMeals.length === 0" class="empty-state">
          No meals logged yet.
        </div>

        <div v-for="meal in allMeals" :key="meal.id" class="meal-item">
          <div class="meal-header" @click="toggleExpand(meal.id)">
            <h4>{{ meal.meal_name }}</h4>
            <span>{{ meal.date }}</span>
          </div>

          <div v-if="expandedMeals.includes(meal.id)" class="meal-details">
            <ul>
              <li v-for="(item, index) in meal.foods" :key="index">
                {{ item.food_name }} - {{ item.calories }} cal | {{ item.protein }}g P | {{ item.carbs }}g C | {{ item.fats }}g F
              </li>
            </ul>
            <p v-if="meal.description"><strong>Notes:</strong> {{ meal.description }}</p>

            <div class="action-buttons">
              <button class="action-btn edit-btn" @click="editMeal(meal)">Edit</button>
              <button class="action-btn delete-btn" @click="confirmDeleteMeal(meal.id, meal.meal_name)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirmModal" class="modal-overlay">
      <div class="modal-content delete-confirm-modal">
        <h3 class="modal-title">Confirm Delete</h3>
        <p class="confirm-message">Are you sure you want to delete <strong>"{{ mealToDelete.name }}"</strong>?</p>
        <p class="confirm-warning">This action cannot be undone.</p>
        
        <div class="confirm-actions">
          <button @click="cancelDelete" class="btn cancel-btn">Cancel</button>
          <button @click="confirmDelete" class="btn confirm-delete-btn">Delete</button>
        </div>
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
      showMealModal: false,
      allMeals: [],
      expandedMeals: [],
      isEditing: false,
      editingMealId: null,
      // New properties for delete confirmation
      showDeleteConfirmModal: false,
      mealToDelete: {
        id: null,
        name: ''
      }
    };
  },
  computed: {
    hasAtLeastOneExpandedFood() {
      return this.foods.some(food => food.isExpanded);
    }
  },
  mounted() {
    this.fetchAllMeals();
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
        this.foods = [this.getEmptyFoodItem()];
      }
    },
    async logMeal() {
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
        const url = this.isEditing 
          ? `/api/v1/meals/${this.editingMealId}/update/` 
          : '/api/v1/meals/log/';

        const method = this.isEditing ? 'put' : 'post';
        const res = await axios[method](url, payload);

        if (res.data.success) {
          // Set appropriate message based on number of food items
          if (validFoods.length === 1) {
            this.message = this.isEditing ? 'Meal updated successfully' : 'Single item meal logged successfully';
          } else {
            this.message = this.isEditing ? 'Meal updated successfully' : 'Meal logged with multiple items';
          }
          
          this.mealName = '';
          this.foods = [this.getEmptyFoodItem()];
          this.description = '';
          this.fetchAllMeals();
          this.isEditing = false;
          this.editingMealId = null;
          setTimeout(() => (this.message = ''), 3000);
        }
      } catch (error) {
        console.error('Error saving meal:', error);
        this.message = 'Error saving meal. Please try again.';
        setTimeout(() => (this.message = ''), 3000);
      }
    },
    async fetchAllMeals() {
      try {
        const res = await axios.get('/api/v1/meals/user/', {
          params: { username: localStorage.getItem('active_username') },
        });
        this.allMeals = res.data.meals || [];
      } catch (err) {
        console.error('Failed to fetch meals:', err);
      }
    },
    toggleExpand(mealId) {
      if (this.expandedMeals.includes(mealId)) {
        this.expandedMeals = this.expandedMeals.filter(id => id !== mealId);
      } else {
        this.expandedMeals.push(mealId);
      }
    },
    // New methods for delete confirmation
    confirmDeleteMeal(mealId, mealName) {
      this.mealToDelete = {
        id: mealId,
        name: mealName
      };
      this.showDeleteConfirmModal = true;
    },
    async confirmDelete() {
      try {
        await axios.delete(`/api/v1/meals/${this.mealToDelete.id}/delete/`);
        this.fetchAllMeals();
        this.showDeleteConfirmModal = false;
        this.message = 'Meal deleted successfully';
        setTimeout(() => (this.message = ''), 3000);
      } catch (err) {
        console.error('Failed to delete meal:', err);
        this.message = 'Error deleting meal. Please try again.';
        setTimeout(() => (this.message = ''), 3000);
      }
    },
    cancelDelete() {
      this.showDeleteConfirmModal = false;
      this.mealToDelete = {
        id: null,
        name: ''
      };
    },
    editMeal(meal) {
      this.isEditing = true;
      this.editingMealId = meal.id;
      this.mealName = meal.meal_name;
      this.description = meal.description;
      this.foods = meal.foods.map(f => ({
        ...this.getEmptyFoodItem(),
        ...f,
        isExpanded: true,
      }));
      this.showMealModal = false;
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
/* Main container styling */
.meal-dashboard {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  min-height: calc(100vh - 60px);
}

.dashboard-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
  padding: 36px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

/* Card title and section headers */
.card-title {
  font-size: 1.75rem;
  color: #333;
  margin-bottom: 24px;
  font-weight: 600;
}

/* View All Meals button */
.view-meals-btn {
  background: transparent;
  border: 2px solid #a4e057;
  color: #a4e057;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 24px;
  float: right;
}

.view-meals-btn:hover {
  background-color: #f5fbe7;
}

/* Form inputs styling */
.input-group {
  margin-bottom: 24px;
}

.input-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: #444;
  font-size: 16px;
}

.input-field {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  font-size: 16px;
  background: #ffffff;
  transition: border-color 0.2s ease;
}

.input-field:focus {
  border-color: #a4e057;
  outline: none;
}

.textarea-field {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  font-size: 16px;
  min-height: 100px;
  resize: vertical;
}

.textarea-field:focus {
  border-color: #a4e057;
  outline: none;
}

/* Food sections styling */
.food-section {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
}

.search-container {
  position: relative;
}

.results-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  margin-top: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.result-item {
  padding: 10px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}

.result-item:hover {
  background: #f5fbe7;
}

.expanded-form {
  animation: fadeIn 0.3s ease;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.food-title {
  font-size: 1.2rem;
  font-weight: 500;
  color: #444;
  margin: 0;
}

.delete-btn {
  background: none;
  border: none;
  color: #ff6b6b;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
}

.delete-icon {
  font-size: 24px;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: #555;
  font-size: 14px;
}

/* Action buttons */
.btn {
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.add-food-btn {
  background: transparent;
  border: 2px solid #a4e057;
  color: #a4e057;
  margin-bottom: 24px;
}

.add-food-btn:hover {
  background-color: #f5fbe7;
}

.submit-btn {
  background: #a4e057;
  color: white;
  font-size: 16px;
  width: 100%;
}

.submit-btn:hover {
  background: #93cc4a;
}

.btn-icon {
  margin-right: 8px;
}

.text-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 14px;
  text-decoration: underline;
  cursor: pointer;
  padding: 6px 0;
  display: inline-block;
}

.text-btn:hover {
  color: #a4e057;
}

/* Success message */
.success-message {
  background-color: #f0fdf0;
  color: #2e7d32;
  padding: 12px;
  border-radius: 8px;
  margin-top: 16px;
  text-align: center;
  animation: fadeIn 0.3s ease;
}

/* UPDATED MODAL STYLES */
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

/* Modal Content */
.modal-content {
  background: white;
  padding: 30px;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.3s ease;
}

/* Modal Title */
.modal-title {
  font-size: 1.75rem;
  margin-bottom: 28px;
  font-weight: 600;
  color: #333;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

/* Close Button */
.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  transition: all 0.2s ease;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background-color: #f5f5f5;
  color: #666;
}

/* Meal Item */
.meal-item {
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  border: 1px solid #f0f0f0;
  transition: box-shadow 0.2s ease;
}

.meal-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Meal Header */
.meal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: 600;
  font-size: 18px;
  color: #444;
  padding: 6px 4px;
}

/* Date display */
.meal-header span {
  font-size: 14px;
  color: #777;
  font-weight: normal;
}

/* Meal Details */
.meal-details {
  margin-top: 12px;
  font-size: 14px;
  color: #555;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
}

/* Food items list */
.meal-details ul {
  padding-left: 20px;
  list-style: none;
  margin: 0 0 12px 0;
}

.meal-details li {
  padding: 6px 0;
  position: relative;
}

.meal-details li:before {
  content: "•";
  color: #a4e057;
  font-weight: bold;
  display: inline-block;
  width: 1em;
  margin-left: -1em;
}

/* Notes section */
.meal-details p {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #e0e0e0;
}

/* Action buttons container */
.action-buttons {
  margin-top: 12px;
  display: flex;
  gap: 10px;
}

/* Edit and Delete buttons */
.action-btn {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-btn {
  background: transparent;
  border: 1px solid #a4e057;
  color: #a4e057;
}

.edit-btn:hover {
  background-color: #f5fbe7;
}

.delete-btn {
  background: transparent;
  border: 1px solid #ff6b6b;
  color: #ff6b6b;
}

.delete-btn:hover {
  background-color: #fff0f0;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 30px 20px;
  color: #777;
  font-size: 16px;
}

/* Delete Confirmation Modal Styles */
.delete-confirm-modal {
  max-width: 450px;
  text-align: center;
}

.confirm-message {
  font-size: 18px;
  margin-bottom: 12px;
  color: #444;
}

.confirm-warning {
  color: #ff6b6b;
  font-size: 14px;
  margin-bottom: 24px;
}

.confirm-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.cancel-btn {
  background: transparent;
  border: 2px solid #ccc;
  color: #666;
}

.cancel-btn:hover {
  background: #f5f5f5;
}

.confirm-delete-btn {
  background: #ff6b6b;
  color: white;
}

.confirm-delete-btn:hover {
  background: #ff5252;
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

/* Mobile responsiveness */
@media (max-width: 768px) {
  .dashboard-card {
    padding: 20px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 12px;
  }
  
  .modal-content {
    padding: 20px;
    width: 95%;
  }
  
  .modal-title {
    font-size: 1.5rem;
    margin-bottom: 20px;
  }
}
</style>