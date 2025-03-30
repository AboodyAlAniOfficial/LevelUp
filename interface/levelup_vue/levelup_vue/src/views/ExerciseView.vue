<template>
  <div class="meal-dashboard">
    <!-- Weight Goal Card -->
    <div class="dashboard-card">
      <h2 class="card-title">Weight Goal</h2>
      <p>
        Current Target Weight:
        <span>{{ weightGoal ? Math.round(weightGoal) + " " + unit : "Not Set" }}</span>
      </p>
      <input
        type="number"
        v-model="newWeight"
        placeholder="Enter new target weight"
        step="0.01"
        class="search-input"
      />
      <button class="submit-btn" @click="updateWeight">Update Weight Goal</button>
      <transition name="fade">
        <div v-if="weightMessage" class="success-message">
          <span class="success-icon">✓</span> {{ weightMessage }}
        </div>
      </transition>
    </div>

    <!-- Daily Steps Goal Card -->
    <div class="dashboard-card">
      <h2 class="card-title">Daily Steps</h2>
      <p>
        Current Daily Steps:
        <span>{{ stepsGoal ? stepsGoal : "Not Set" }}</span>
      </p>
      <input
        type="number"
        v-model="newSteps"
        placeholder="Enter daily steps"
        class="search-input"
      />
      <button class="submit-btn" @click="updateSteps">Update Steps</button>
      <transition name="fade">
        <div v-if="stepsMessage" class="success-message">
          <span class="success-icon">✓</span> {{ stepsMessage }}
        </div>
      </transition>
    </div>

    <!-- Daily Calorie Goal Card -->
    <div class="dashboard-card">
      <h2 class="card-title">Daily Calorie Goal</h2>
      <p>
        Current Daily Calorie Goal:
        <span>{{ calorieGoal ? calorieGoal : "Not Set" }}</span>
        <br>
        <label for="Not Active">
          Not Active:
        <input type="radio" name="selection" value="1.2" @change="updateCalories(1.2)">
        <br>
        </label>
        <label for="Moderately Active">
          Moderatly Active:
        <input type="radio" name="selection" value="1.55" @change="updateCalories(1.55)">
        <br>
        </label>
        <label for="Very Active">
          Very Active:
        <input type="radio" name="selection" value="1.725" @change="updateCalories(1.725)">
        </label>
      </p>
    </div>

    <!-- Calculate Daily Calories Card -->
    <div class="dashboard-card">
      <h2 class="card-title">Calculate Daily Calories</h2>
      <p>Search your meal names to calculate total calories for the day:</p>

      <!-- Searchable Input Fields -->
      <div v-for="(meal, key) in mealInputs" :key="key">
        <input
          type="text"
          v-model="meal.query"
          @input="debouncedSearch(key)"
          :placeholder="`${key.charAt(0).toUpperCase() + key.slice(1)} meal name`"
          class="search-input"
        />
        <ul v-if="meal.results.length" class="results-list">
          <li
            v-for="result in meal.results"
            :key="result.meal_name"
            class="result-item"
            @click="selectMeal(key, result)"
          >
            {{ result }}
          </li>
        </ul>
      </div>

      <button class="submit-btn" @click="calculateDailyCalories">
        Calculate Calories
      </button>

      <transition name="fade">
        <div v-if="calculationResult" class="success-message">
          <div>
            <strong>Total Calories: {{ calculationResult.totalCalories }}</strong>
          </div>
          <div class="meal-breakdown">
            <div v-if="calculationResult.meals.breakfast">
              <strong>Breakfast:</strong>
              {{ calculationResult.meals.breakfast.meal_name }} -
              {{ calculationResult.meals.breakfast.calories }} calories
            </div>
            <div v-if="calculationResult.meals.lunch">
              <strong>Lunch:</strong>
              {{ calculationResult.meals.lunch.meal_name }} -
              {{ calculationResult.meals.lunch.calories }} calories
            </div>
            <div v-if="calculationResult.meals.dinner">
              <strong>Dinner:</strong>
              {{ calculationResult.meals.dinner.meal_name }} -
              {{ calculationResult.meals.dinner.calories }} calories
            </div>
          </div>
          <p v-if="calculationMessage">{{ calculationMessage }}</p>
        </div>
      </transition>

      <transition name="fade">
        <div
          v-if="calculationError"
          class="success-message"
          style="background-color: #ffcccc; color: #b32d00;"
        >
          <span class="success-icon">✗</span> {{ calculationError }}
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from "axios";
function debounce(func, wait = 300) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

export default {
  name: "HealthGoals",
  data() {
    return {
      userId: null,
      weightGoal: null,
      stepsGoal: null,
      calorieGoal: null,
      mass: null,
      bmr: null,
      unit: null,
      newWeight: "",
      newSteps: "",
      weightMessage: "",
      stepsMessage: "",
      calculationResult: null,
      calculationMessage: "",
      calculationError: "",
      mealInputs: {
        breakfast: { query: "", results: [] },
        lunch: { query: "", results: [] },
        dinner: { query: "", results: [] },
      }
    };
  },
    async mounted() {
    await this.fetchUserId();
    await this.fetchUserPreference();
    await this.fetchUserData();
    

    await this.createDailyGoals();
    if(this.userId!=null){
    this.fetchWeightGoal();
    this.fetchStepsGoal();
    this.fetchCalorieGoal();
    this.fetchUserBMR();
    }
    },
    methods: {
    async fetchUserId() {
      const username = localStorage.getItem("active_username");
      const res = await axios.get(`/api/v1/daily_goals/getUserId/`, { params: { username } });
      if (res.data && res.data.data) this.userId = res.data.data.user_id;
    },
    debouncedSearch: debounce(function (key) {
      this.searchMeals(key);
    }, 300),
    async searchMeals(key) {
      const q = this.mealInputs[key].query;
      if (q.length < 2) return (this.mealInputs[key].results = []);
      try {
        const res = await axios.get(`/api/v1/daily_goals/searchMeals/`, {
          params: { username: localStorage.getItem("active_username"), q },
        });
        this.mealInputs[key].results = res.data;
      } catch (error) {
        console.error("Search error:", error);
      }
    },
    selectMeal(key, name) {
      this.mealInputs[key].query = name;
      this.mealInputs[key].results = [];
    },
    async calculateDailyCalories() {
      try {
        const res = await axios.post(`/api/v1/daily_goals/calculateCalories/${this.userId}`, {
          breakfast: this.mealInputs.breakfast.query,
          lunch: this.mealInputs.lunch.query,
          dinner: this.mealInputs.dinner.query,
        });
        if (res.data) {
          this.calculationResult = {
            totalCalories: res.data.dailyCalories,
            meals: res.data["meals data"],
          };
          this.calculationMessage = "Calorie calculation successful!";
        }
      } catch (error) {
        console.error("Error calculating calories:", error);
        this.calculationError =
          error.response?.data?.error || "Error calculating calories.";
      }
    },
  
  async fetchUserData(){
    try{
      const active_user = localStorage.getItem("active_username");
      const response = await axios .get(`/api/v1/accounts/healthdata/`, {params: {username: active_user, field: 'mass'}});

      if (response.data){
        this.mass = response.data;
        console.log("MASS:" + this.mass);
      }

    

    }catch (error){
      console.error("Error Fetching Data", error)
    }
  },
  async fetchUserPreference(){
    const active_user = localStorage.getItem("active_username");
    try{  
      const response = await axios .get(`/api/v1/accounts/unit/`, {params: {username: active_user, dimension: 'mass'}});

      if (response.data){
        this.unit = response.data;
        console.log("UNIT: " +this.unit);
      }
      }catch(error){
        console.error("Error Fetching Data", error)
      }
    },

  async createDailyGoals(){
    try {
      const response = await axios .post(`/api/v1/daily_goals/createDailyGoals/`, {user_id: this.userId});
      if (response.data){
        
      }

    }catch (error){

    }
  },

  async updateCalories(value){

    const updated_bmr = this.bmr/4184 * 86400;
    const today_calories =  value * updated_bmr;
    var updated_calories = today_calories;
    if(this.mass<this.weightGoal){

      updated_calories += 500;
      console.log("MASS IS LESS THAN TARGET");
      console.log("TARGET" + this.weightGoal);
    }else if(this.mass > this.weightGoal){
    updated_calories -= 500;

    }else{

    }

    console.log("BMR" + this.bmr);
    
    try {
      const response = await axios .post(`/api/v1/daily_goals/updateCalories/${this.userId}`,{calories: updated_calories});

      if (response.data){
        this.fetchCalorieGoal();
      }
    }catch (error){
      console.error("Error updating calories", error);
    }

  },

  async fetchUserBMR(){

    try{
      const active_user = localStorage.getItem("active_username");
      const response = await axios .get(`/api/v1/accounts/bmr/`, {params: {username: active_user}});

      if(response.data){
        this.bmr = response.data;
      }
    }catch (error){
      console.error("Error Fetching BMR", error);
    }

  },
  fetchWeightGoal() {
      axios
        .get(`/api/v1/daily_goals/weightGoal/${this.userId}`)
        .then((response) => {
          if (response.data && response.data.Target) {
            if(this.unit==='kg'){
            this.weightGoal = response.data.Target.target_weight;
            }else{
            const lbs = response.data.Target.target_weight * 2.205;
            console.log("lbs: " + lbs);
            this.weightGoal = lbs;
          }
          }
        })
        .catch((error) => {
          console.error("Error fetching weight goal:", error);
        });
    },
    updateWeight() {
      if (!this.newWeight) return;
      if(this.unit === 'kg'){

      }else{
        const tempWeight = this.newWeight/2.205;
        this.newWeight = tempWeight.toFixed(2);
      }
      axios
        .post(`/api/v1/daily_goals/weight/${this.userId}`, { weight: this.newWeight })
        .then(() => {
          this.weightMessage = "Weight goal updated successfully!";
          this.fetchWeightGoal();
          this.newWeight = "";
        })
        .catch((error) => {
          console.error("Error updating weight goal:", error);
          this.weightMessage = "Error updating weight goal.";
        });
    },
    fetchStepsGoal() {
      axios
        .get(`/api/v1/daily_goals/dailySteps/${this.userId}`)
        .then((response) => {
          if (response.data && response.data.steps) {
            this.stepsGoal = response.data.steps.daily_steps_goal;
          }
        })
        .catch((error) => {
          console.error("Error fetching steps goal:", error);
        });
    },
    updateSteps() {
      if (!this.newSteps) return;
      axios
        .post(`/api/v1/daily_goals/steps/${this.userId}`, { steps: this.newSteps })
        .then(() => {
          this.stepsMessage = "Steps updated successfully!";
          this.fetchStepsGoal();
          this.newSteps = "";
        })
        .catch((error) => {
          console.error("Error updating steps goal:", error);
          this.stepsMessage = "Error updating steps.";
        });
    },
    fetchCalorieGoal() {
      axios
        .get(`/api/v1/daily_goals/calories/${this.userId}`)
        .then((response) => {
          if (response.data && response.data.data) {
            this.calorieGoal = response.data.data.daily_calorie_goal;
          }
        })
        .catch((error) => {
          console.error("Error fetching calorie goal:", error);
        });
    },updateCalorieGoal(){
      const active_user = localStorage.getItem("active_username");
      const response = axios .post(`/api/v1/accounts/bmr/`, {})

    }
  
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

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.2s ease;
  margin-bottom: 10px;
}

.search-input:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.submit-btn {
  display: inline-flex;
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

/* Fade transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Optional meal breakdown styling */
.meal-breakdown > div {
  margin-top: 8px;
}
</style>
