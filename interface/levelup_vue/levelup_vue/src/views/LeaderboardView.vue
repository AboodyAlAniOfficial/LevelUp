<template>
    <div class="leaderboard-dashboard">
      <div class="leaderboard">
        <h2 class="card-title">Global Leaderboard</h2>

        <div class="leaderboard-wrapper">
          <input 
          type="text" 
          v-model="search" 
          placeholder="Enter a Username"
          class="search">

          <table class="table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, index) in filteredUsers":key="user.score">
                <td>{{ index+1 }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.score }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="leaderboard">
        <h2 class="card-title">Private Leaderboard</h2>

        <div class="leaderboard-wrapper">
          <input 
          type="text" 
          v-model="search" 
          placeholder="Enter a Username"
          class="search">

          <table class="table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, index) in filteredPUsers" :key="user.score">
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

//Replace if your implementation is different/does not work with this
export default {
  name: 'LeaderboardView',
  data() {
    return {
      users: [],
      fUsers: [],
    }
  },
  computed: {//Search bar logic 
    filteredUsers() {
      return this.users.filter(users => {
        return users.toLowerCase().username.indexOf(this.search.toLowerCase) > -1
      })
    },
    filteredPUsers() {
      return this.fUsers.filter(fUsers => {
        return fUsers.username.toLowerCase().indexOf(this.search.toLowerCase) > -1
      })
    }
  },

  // Should be changed if your backend does not match
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

.leaderboard-wrapper {
  overflow-y: auto;
  max-height: 200px;
  overflow: hidden;
  position:relative;
  display: flex;
  flex-direction: column;
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
  padding: 8px;
  position: static;
  width: 100%;
  padding: 14px 16px;
  background: white;
  border: 2px solid black;
  border-collapse: collapse;
  z-index: 10;
}

.search {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.2s ease;
}

.search:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.table th, .table td {
  color:#000000;
  font-size: 1rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 20px;
}

th:not(:last-child), td:not(:last-child) {
  border-right: 2px solid rgb(0, 0, 0);
}
</style>
