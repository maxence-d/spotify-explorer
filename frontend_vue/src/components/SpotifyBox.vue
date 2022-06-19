<template>
      <div class="card">
        <div class="card-content">
          <p class="title">
            Spotify status:
          </p>
        </div>
        <footer class="card-footer">
          <p class="card-footer-item">
            <router-link to="/log-in" @click="logOut()" class="button is-light">Log-out</router-link>
          </p>
          <p class="card-footer-item">
            <router-link to="/log-in" @click="logOut()" class="button is-light">Log-out</router-link>
          </p>
        </footer>
      </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'SpotifyBox',
  data() {
    return {
      artists: []
    }
  },
  components: {
  },
  mounted() {
  },
  methods: {
  }
}
</script>