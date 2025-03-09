<template>
    <div class="column is-multiline">
        
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LeaderboardView',
  data() {
    return {
      leaderboard: [],
      privateLeaderboard: []
    }
  },
  components: {
    mounted() {
      this.getLeaderboard(),
      this.getPLeaderboard() 
    }
  },
  methods: {
    getLeaderboard() { //STUB: Need to update to match component app in django. Fetches all user and their score/rankings.
      axios
        .get('api/v1/leaderboard') //Name of the django page storing these data (most likely to fetch all users)
        .then(response=>{
          this.profile = response.data
        })
        .catch(error=>{
          console.log(error)
        })
    },
    getPLeaderboard() { //STUB: Need to update to match component app in django. Fetches all user and their score/rankings that are 'friend' with current user
      axios
        .get('api/v1/leaderboard') //Name of the django page storing these data (most likely to fetch all users)
        .then(response=>{
          this.profile = response.data
        })
        .catch(error=>{
          console.log(error)
        })
    }, 
  }
}
</script>