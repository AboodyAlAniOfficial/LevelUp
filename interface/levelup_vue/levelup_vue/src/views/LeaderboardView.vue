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
  <div class = "followresults">
      <p v-if= "followMessage">{{ followMessage }}</p>
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
            <tr v-for="(user, index) in users" :key="user.username">
              <td>{{ index + 1 }}</td>
              <td>{{ user.user }}</td>
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
            <tr v-for="(user, index) in fUsers" :key="user.user">
              <td>{{ index + 1 }}</td>
              <td>{{ user.user }}</td>
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

export default {
  name: "LeaderboardView",
  data() {
    return {
      users: [],
      fUsers: [],
      filteredResults: [],
      filteredFResults: [],
      search: "", // Search term for filtering
      followMessage: "",
    };
  },
  computed: {
  filteredUsers() {
        return this.search.trim()
      ? this.users.filter(user =>
          (user.username || "").toLowerCase().includes(this.search.toLowerCase())
        )
      : this.users;
      return this.filteredResults
    },

    filteredPUsers() {
      // Show all followers if search is empty
          this.filteredFResults = this.search.trim()
      ? this.users.filter(user =>
          (user.username || "").toLowerCase().includes(this.search.toLowerCase())
        )
      : this.fUsers;
      return this.filteredFResults
      },
  },
  mounted() {
    // Fetch leaderboard data when component mounts
    this.getLeaderboard();
    this.getPLeaderboard();
    this.searchUsers();
  },
  methods: {
    async getLeaderboard() {
      try {
        const response = await axios.get("/api/v1/leaderboard/global");
        this.users = response.data; // Populate users array
        console.log("Global leaderboard data fetched:", this.users);
      } catch (error) {
        console.error("Error fetching global leaderboard:", error);
      }
    },
    async getPLeaderboard() {
      try {
        const response = await axios.get("/api/v1/leaderboard/fleaderboard", {
          params: { username: localStorage.getItem('active_username') },
        });
        this.fUsers = response.data; // Populate fUsers array
        console.log("Follower leaderboard data fetched:", this.fUsers);
      } catch (error) {
        console.error("Error fetching follower leaderboard:", error);
      }
    },
    async searchUsers() {
      try {
        const response = await axios.get("/api/v1/leaderboard/search/", {
          params: { q: this.search.trim() },
        });
        this.filteredResults = response.data.users; // Update users array with search results
        console.log("Search results:", this.users);
        this.followMessage = "Search for a user to follow!";
      } catch (error) {
        console.error("Error searching users:", error);
      }
    },
    async followUser() {
      try {
        const username = localStorage.getItem("active_username"); // Active user
        const response = await axios.post("/api/v1/leaderboard/follow/", {
          follower_username: username,
          username_to_follow: this.search.trim(),
        });
        console.log("User followed successfully:", response.data);
        await this.getPLeaderboard(); 
        this.followMessage = 'Followed!';
      } catch (error) {
        console.error("Error following user:", error.response?.data || error.message);
        this.followMessage = 'Error!';
      }
    },
    async unfollowUser() {
      try {
        const username = localStorage.getItem("active_username"); // Active user
        const response = await axios.post("/api/v1/leaderboard/unfollow/", {
          follower_username: username,
          username_to_unfollow: this.search.trim(),
        });
        console.log("User unfollowed successfully:", response.data);
        await this.getPLeaderboard(); 
        this.followMessage = 'Unfollowed!';
      } catch (error) {
        console.error("Error unfollowing user:", error.response?.data || error.message);
        this.followMessage = 'Error!';
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
  height: auto;
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
.followresults{
  display: flex;
  justify-content: center;
  margin-top: -1rem;
  margin-bottom: 3rem;
  font-size: 14px;
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

.table th{
  color: #000000;
  font-size: 20px;
  font-weight: 525;
  margin-top: 0;
  margin-bottom: 30px;
  transition: all 0.2s ease;
}
.table td {
  color: #000000;
  font-size: 16px;
  font-weight: 400;
  margin-top: 0;
  margin-bottom: 20px;
  transition: all 0.2s ease;
}

th:not(:last-child),
td:not(:last-child) {
  border-right: 2px solid rgb(0, 0, 0);
  transition: all 0.2s ease;
}
</style>
