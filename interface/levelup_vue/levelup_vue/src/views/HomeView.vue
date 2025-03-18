<template>
  <div class="home-dashboard">
    <div class="dashboard-card welcome-card">
      <div class="welcome-content">
        <div class="app-logo">
          <span class="logo-icon">🥗</span>
          <h1 class="logo-text">LevelUp</h1>
        </div>
        
        <h2 class="welcome-title">Track, Achieve, and Share Your Health Journey</h2>
        
        <p class="welcome-description">
          A modern platform that allows you to track your caloric intake, set daily fitness goals, 
          and share your progress with others in a supportive community.
        </p>
        
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Meal Tracking</h3>
            <p class="feature-desc">Log your meals and monitor your nutrition with detailed breakdowns.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Goal Setting</h3>
            <p class="feature-desc">Create personalized daily fitness and nutrition targets.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h3 class="feature-title">Community</h3>
            <p class="feature-desc">Share achievements and connect with others on similar journeys.</p>
          </div>
        </div>
        
        <div class="action-buttons">
          <a class="action-btn primary-btn" href="/login">
            <span class="btn-icon">👤</span> Sign Up
          </a>
          <a class="action-btn secondary-btn" href="/about">
            <span class="btn-icon">ℹ️</span> Learn More
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  components: {}
}
</script>

<style scoped>
.home-dashboard {
  font-family: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
  max-width: 900px;
  margin: 2rem auto;
}

.dashboard-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  padding: 40px;
  margin-bottom: 20px;
}

.welcome-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.app-logo {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.logo-icon {
  font-size: 32px;
  margin-right: 12px;
}

.logo-text {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.welcome-title {
  color: #333;
  font-size: 2rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 20px;
  line-height: 1.3;
  max-width: 700px;
}

.welcome-description {
  color: #555;
  font-size: 1.125rem;
  line-height: 1.6;
  margin-bottom: 40px;
  max-width: 700px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  width: 100%;
  margin-bottom: 40px;
}

.feature-card {
  background-color: #f9f9f9;
  border-radius: 14px;
  padding: 24px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 28px;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  margin-top: 0;
  margin-bottom: 12px;
}

.feature-desc {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
}

.primary-btn {
  background-color: #a4e057;
  color: #333;
}

.primary-btn:hover {
  background-color: #93cc4a;
  transform: translateY(-2px);
}

.secondary-btn {
  background-color: #f5f5f5;
  color: #555;
}

.secondary-btn:hover {
  background-color: #e8e8e8;
  transform: translateY(-2px);
}

.btn-icon {
  font-size: 18px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .dashboard-card {
    padding: 24px;
  }
}

@media (min-width: 769px) and (max-width: 1023px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>