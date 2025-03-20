<template>
    <div class="leaderboard-dashboard">
      <div class="leaderboard">
        <h2 class="card-title">Global Leaderboard</h2>

        <div class="leaderboard-wrapper">
          <table>
            <thead>
              <tr class="table">
                <th class="table-item">Rank</th>
                <th class="table-item">Username</th>
                <th class="table-item">Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, index) in users" :key="user.score">
                <td>{{ index+1 }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.score }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="leaderboard">
        <h2 class="card-title" href="#">Private Leaderboard</h2>

        <div class="leaderboard-wrapper">
          <table>
            <thead>
              <tr class="table">
                <th>Rank</th>
                <th>Username</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, index) in fUsers" :key="user.score">
                <td>{{ index+1 }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.score }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios'

//Replace if your implementation is different
export default {
  name: 'LeaderboardView',
  data() {
    return {
      users: [],
      fUsers: [],
    }
  },
  components: {
    mounted() {
      this.getLeaderboard(),
      this.getPLeaderboard() 
    }
  },
  methods: {
    async getLeaderboard() { //TODO: Fetch all user and their score/rankings.
      try {
        axios.get('api/v1/leaderboard').then(response=>{
            this.users = response.data
          })
      } catch (error) {
        console.error('Error loading global user rankings:', error)
      }
    },
    async getPLeaderboard() { //TODO: Fetches all user and their score/rankings that are 'friend' with current user
    }, 
  }
}
</script>

<style scoped>
.leaderboard-dashboard {
  font-family: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
  max-width: 1500px;
  margin: 2rem auto;
  display: flex; 
  justify-content: space-between; 
  gap: 10px; 
}

.leaderboard {
  flex: 1;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  padding: 20px;
  margin-bottom: 20px;
}

.card-title {
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 20px;
}

.table {
  margin: 4px 0 0;
  padding: 0;
  position: static;
  width: 35%;
  background: white;
  border-radius: 20px;
  border-collapse: collapse;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

th, td {
  color:#333;
  font-size: 1rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 20px;
}

th:not(:last-child), td:not(:last-child) {
  border-right: 1px solid rgb(0, 0, 0);
}
</style>
