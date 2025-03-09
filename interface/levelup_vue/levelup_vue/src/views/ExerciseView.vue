<template>
    <div class="column is-multiline">
        
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'exercise',
  data() {
    return {
      userExercise: []
    }
  },
  components: {
    mounted() {
      this.getUserExercise()
    }
  },
  methods: {
    getUserExercise() { //STUB: Need to update to match component app in django
      axios
        .get('api/v1/u/exercise') //Name of the django page storing these data
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
