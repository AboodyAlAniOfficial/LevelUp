<template>
  <div class="about-container">
    <div class="feature-card">
      <h1 class="card-title">Features</h1>
      
      <div class="feature-section">
        <div class="feature-icon">👤</div>
        <div class="feature-content">
          <h2 class="feature-title">User Profile</h2>
          <p class="feature-description">
            Manage your account settings and track your fitness progress with personalized information.
          </p>
          <div class="feature-details">
            <p>Information includes:</p>
            <ul class="feature-list">
              <li>Personal metrics: weight, height, age, and sex</li>
              <li>BMI and BMR calculations using the Mifflin-St Jeor Equation</li>
              <li>Activity level selection:
                <ul>
                  <li>Not Active</li>
                  <li>Moderately Active</li>
                  <li>Very Active</li>
                </ul>
              </li>
              <li>Measurement unit preferences (metric/imperial)</li>
              <li>Privacy settings for tracker and leaderboard data</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="feature-divider"></div>
      
      <div class="feature-section">
        <div class="feature-icon">📊</div>
        <div class="feature-content">
          <h2 class="feature-title">Daily Trackers</h2>
          <p class="feature-description">
            Monitor and log all aspects of your fitness journey with comprehensive tracking tools.
          </p>
          <div class="feature-details">
            <ul class="feature-list">
              <li>Meal Logger - track what you eat with food search and manual entry options</li>
              <li>Weight Goal - set and update your target weight</li>
              <li>Daily Steps - monitor your physical activity</li>
              <li>Daily Calorie Goal - based on your activity level</li>
              <li>Calorie Calculator - track meals throughout the day (breakfast, lunch, dinner)</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="feature-divider"></div>
      
      <div class="feature-section">
        <div class="feature-icon">🏆</div>
        <div class="feature-content">
          <h2 class="feature-title">Leaderboards</h2>
          <p class="feature-description">
            Compare your fitness progress with others in the community, with privacy options to control what information is shared.
          </p>
          <p class="feature-sub-description">
            Your score is calculated based on your consistency and progress toward your fitness goals.
          </p>
        </div>
      </div>

      <div class="feature-divider"></div>
      
      <div class="feature-section">
        <div class="feature-icon">⚙️</div>
        <div class="feature-content">
          <h2 class="feature-title">Preferences</h2>
          <p class="feature-description">
            Customize your experience with personalized settings.
          </p>
          <div class="feature-details">
            <ul class="feature-list">
              <li>Measurement Units:
                <ul>
                  <li>Length Unit (meter/inch)</li>
                  <li>Mass Unit (kilogram/pound)</li>
                  <li>Energy Unit (kilojoule/calorie)</li>
                </ul>
              </li>
              <li>Privacy Settings - control who can see your tracker and leaderboard data</li>
              <li>Health Data - input personal information used to calculate BMR</li>
            </ul>
          </div>
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

.feature-sub-description {
  color: #666;
  font-style: italic;
  margin-bottom: 0;
  line-height: 1.4;
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