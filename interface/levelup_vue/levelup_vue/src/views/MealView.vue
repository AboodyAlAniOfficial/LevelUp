<template>
    <div class="column is-multiline">
        
    </div>
</template>

<script>
export default {
  name: 'meal',
  data() {
    return {
      meal: []
    }
  },
  components: {
    mounted() {
      this.getMealList()
    }
  },
  methods: {
    getMealList() { //STUB: Need to update to match component app in django. Fetches the entire list of food from database, need another method for fetching users'.
      axios
        .get('api/v1/meals') //Name of the django page storing these data
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