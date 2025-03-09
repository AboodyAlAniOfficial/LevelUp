<template>
    <div class="column is-multiline">
        
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProfileView',
  data() {
    return {
      userProfile: []
    }
  },
  components: {
    mounted() {
      this.getUserProfile() 
    }
  },
  methods: {
    getUserProfile() { //STUB: Need to update to match component app in django
      axios
        .get('api/v1/u/profile') //Name of the django page storing these data
        .then(response=>{
          this.profile = response.data
        })
        .catch(error=>{
          console.log(error)
        })
    }
  }
}
</script>