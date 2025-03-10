<template>
  <div class="meal-creation">
    <h2>Log a Meal</h2>
    
    <form @submit.prevent="submitMeal">
      <div class="input-group">
        <label for="meal-name">Meal Name:</label>
        <input type="text" id="meal-name" v-model="meal.meal_name" required />
      </div>

      <div class="input-group">
        <label for="calories">Calories:</label>
        <input type="number" id="calories" v-model="meal.calories" required />
      </div>

      <div class="input-group">
        <label for="protein">Protein (g):</label>
        <input type="number" id="protein" v-model="meal.protein" required />
      </div>

      <div class="input-group">
        <label for="carbs">Carbs (g):</label>
        <input type="number" id="carbs" v-model="meal.carbs" required />
      </div>

      <div class="input-group">
        <label for="fats">Fats (g):</label>
        <input type="number" id="fats" v-model="meal.fats" required />
      </div>

      <div class="input-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="meal.description"></textarea>
      </div>

      <button type="submit" class="submit-btn">Log Meal</button>
    </form>

    <p v-if="message" class="success-message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      meal: {
        meal_name: '',
        calories: '',
        protein: '',
        carbs: '',
        fats: '',
        description: '',
      },
      message: '',
    };
  },
  methods: {
    async submitMeal() {
      try {
        const response = await axios.post('/api/meals/', this.meal, {
          headers: {
            Authorization: `Token ${localStorage.getItem('userToken')}`, // Assuming authentication
          },
        });

        this.message = 'Meal logged successfully!';
        this.resetForm();
      } catch (error) {
        console.error('Error logging meal:', error);
      }
    },
    resetForm() {
      this.meal = {
        meal_name: '',
        calories: '',
        protein: '',
        carbs: '',
        fats: '',
        description: '',
      };
    },
  },
};
</script>

<style scoped>
.meal-creation {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
}

.input-group {
  margin-bottom: 10px;
}

label {
  display: block;
  font-weight: bold;
}

input, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #0056b3;
}

.success-message {
  color: green;
  text-align: center;
  margin-top: 10px;
}
</style>
