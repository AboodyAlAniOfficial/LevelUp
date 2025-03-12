<template>
  <div class="about-container">
    <div class="feature-card">
      <h1 class="card-title">Features</h1>
      
      <div class="feature-section">
        <div class="feature-icon">👤</div>
        <div class="feature-content">
          <h2 class="feature-title">User Profile</h2>
          <p class="feature-description">
            The user can manage their account as well as see information related to keep track of your fitness progress here.
          </p>
          <div class="feature-details">
            <p>These includes:</p>
            <ul class="feature-list">
              <li>User's weight, height, and gender</li>
              <li>Their BMI score and BMR score (using Mifflin-St Jeor Equation)</li>
              <li>Their exercise frequency:
                <ul>
                  <li>Sedentary</li>
                  <li>1-3 times a week</li>
                  <li>4-5 times a week</li>
                  <li>Daily or intense exercise 3-4 times a week</li>
                  <li>Daily intense exercise</li>
                  <li>Very intense daily exercise</li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="feature-divider"></div>
      
      <div class="feature-section">
        <div class="feature-icon">📊</div>
        <div class="feature-content">
          <h2 class="feature-title">Daily Tracker</h2>
          <p class="feature-description">
            Where you can track your daily calorie intake and exercises done based on BMI and BMR calculations.
          </p>
        </div>
      </div>
      
      <div class="feature-divider"></div>
      
      <div class="feature-section">
        <div class="feature-icon">🏆</div>
        <div class="feature-content">
          <h2 class="feature-title">Leaderboard</h2>
          <p class="feature-description">
            This is where you can compare your fitness progress with others with a score based on how committed you are to your fitness goal.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-container {
  font-family: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
  max-width: 800px;
  margin: 2rem auto;
}

.feature-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  padding: 32px;
}

.card-title {
  color: #333;
  font-size: 1.8rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 32px;
  text-align: center;
}

.feature-section {
  display: flex;
  margin-bottom: 24px;
}

.feature-icon {
  font-size: 28px;
  margin-right: 16px;
  background-color: #f5fbf0;
  height: 56px;
  width: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-content {
  flex: 1;
}

.feature-title {
  color: #333;
  font-size: 1.4rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 12px;
}

.feature-description {
  color: #555;
  margin-bottom: 16px;
  line-height: 1.5;
}

.feature-details {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.feature-details p {
  margin-top: 0;
  margin-bottom: 12px;
  font-weight: 500;
}

.feature-list {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.feature-list li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.feature-list li:last-child {
  border-bottom: none;
}

.feature-list ul {
  list-style-type: none;
  padding-left: 20px;
  margin: 8px 0;
}

.feature-list ul li {
  padding: 4px 0;
  border-bottom: none;
  position: relative;
}

.feature-list ul li:before {
  content: "•";
  position: absolute;
  left: -15px;
  color: #a4e057;
}

.feature-divider {
  height: 1px;
  background-color: #eee;
  margin: 24px 0;
}

@media (max-width: 768px) {
  .about-container {
    padding: 0 16px;
  }
  
  .feature-section {
    flex-direction: column;
  }
  
  .feature-icon {
    margin-bottom: 16px;
  }
}
</style>