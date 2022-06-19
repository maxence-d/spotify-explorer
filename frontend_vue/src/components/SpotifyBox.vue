<template>
      <div class="card">
        <div class="card-content">
          <p class="title">
            Spotify status:
          </p>
        </div>
        <footer class="card-footer">
          <template v-if=this.sp_is_auth>
            <p class="card-footer-item">
              <button class="button" @click="logOut()" >Signed In</button>
            </p>
          </template>
          <template v-else>
            <p class="card-footer-item">
              Not authenticated
            </p>
            <p class="card-footer-item">
              <button class="button" @click="sp_do_auth()">Log in</button>
            </p>
          </template>
        </footer>
      </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'SpotifyBox',
  data() {
    return {
      sp_is_auth : false
    }
  },
  components: {
  },
  mounted() {
    this.get_sp_auth()
  },
  methods: {
    async get_sp_auth() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get("/api/v1/sp_is_auth")
        .then(response => {
          localStorage.setItem("is_sp_authenticated", response.data.sp_is_auth) 
          this.sp_is_auth = response.data.sp_is_auth
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    },
  }
}
</script>