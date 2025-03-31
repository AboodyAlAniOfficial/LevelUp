<template>
  <div class="searchContainer">
    <input
      type="text"
      v-model="search"
      placeholder="Enter a Username"
      class="search"
      @input="searchUsers"
    />
    <button @click="followUser" class="followButton">Follow</button>
    <button @click="unfollowUser" class="unfollowButton">Unfollow</button>
  </div>
  <div class="leaderboard-dashboard">
    <div class="leaderboard">
      <h2 class="card-title">Global Leaderboard</h2>

      <div class="leaderboard-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Username</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in filteredUsers" :key="user.score">
              <td>{{ index + 1 }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.score || '0'}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="leaderboard">
      <h2 class="card-title">Follower Leaderboard</h2>

      <div class="leaderboard-wrapper">
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
              <td>{{ index + 1 }}</td>
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
import axios from "axios";

//Replace if your implementation is different/does not work with this
export default {
  name: "LeaderboardView",
  data() {
    return {
      users: [],
      fUsers: [],
      search: "",
    };
  },
computed: {
  // Search bar logic for users
  filteredUsers() {
    return this.users.filter(user => user.username.toLowerCase().includes(this.search.toLowerCase()));
  },
  
  // Search bar logic for followers (filteredPUsers)
  filteredPUsers() {
    return this.fUsers.filter(user => user.username.toLowerCase().includes(this.search.toLowerCase()));
  }
},

  // Should be changed if your backend does not match
  components: {
    mounted() {
      this.getLeaderboard(), this.getPLeaderboard();
    },
  },
methods: {
  async searchUsers() {
    try {
      const response = await axios.get('/api/v1/leaderboard/search/', {
        params: { q: this.search }, // Pass the search query to the backend
      });
      this.users = response.data.users; // Update the users array with search results
    } catch (error) {
      console.error('Error searching users:', error);
    }
  },
  async followUser() {
    try {
      const username= localStorage.getItem('active_username');  ;  // Get the active user's username from localStorage
      const response = await axios.post("/api/v1/leaderboard/follow/", {
        follower_username: username,  // Pass the active user's username as the follower
        username_to_follow: this.search,  // The username to follow, taken from your search input
    });
      console.log("User followed successfully:", response.data);
  } catch (error) {
      console.error("Error following user:", error.response?.data || error.message);
  }
},
  async unfollowUser() {
    try {
      const username = localStorage.getItem('active_username'); // Get the active user's username from localStorage
      const response = await axios.post("/api/v1/leaderboard/unfollow/", {
        follower_username: username,  // Pass the active user's username as the follower
        username_to_unfollow: this.search,  // The username to unfollow, taken from your search input
    });
      console.log("User unfollowed successfully:", response.data);
  } catch (error) {
      console.error("Error unfollowing user:", error.response?.data || error.message);
  }
},

    async getLeaderboard() {
      try {
        axios.get("api/v1/leaderboard/global").then((response) => {
          this.users = response.data;
        });
      } catch (error) {
        console.error("Error loading global user rankings:", error);
      }
    },
    async getPLeaderboard() {
        try {
        axios.get("api/v1/leaderboard/fleaderboard").then((response) => {
          this.fUsers = response.data;
        });
      } catch (error) {
        console.error("Error loading global user rankings:", error);
      }
    },
  },
};
</script>

<style scoped>
.leaderboard-dashboard {
  font-family: "Segoe UI", Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
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
  position: relative;
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
.searchContainer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  height: 100px;
}
.search {
  width: 50%;
  padding: 12px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.2s ease;
}
.followButton {
  background-color: #a4e057;
  color: #333;
  padding: 12px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.2s ease;
}

.followButton:hover {
  background-color: #93cc4a;
  transform: translateY(-2px);
}

.unfollowButton {
  background-color: #f5f5f5;
  color: #555;
  padding: 12px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.2s ease;
}

.unfollowButton:hover {
  background-color: #e8e8e8;
  transform: translateY(-2px);
}
.search:focus {
  outline: none;
  border-color: #a4e057;
  box-shadow: 0 0 0 3px rgba(164, 224, 87, 0.2);
}

.table th,
.table td {
  color: #000000;
  font-size: 1rem;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 20px;
}

th:not(:last-child),
td:not(:last-child) {
  border-right: 2px solid rgb(0, 0, 0);
}
</style>
