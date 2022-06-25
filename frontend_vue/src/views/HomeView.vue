<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
        <ArtistView
         v-bind:sp_id="this.$store.state.artist"
        />
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
          <h2 class="is-size-2 has-text-centered">Artists</h2>
      </div>

      <ArtistBox 
        v-for="artist in artists"
        v-bind:key="artist.id"
        v-bind:artist="artist"
         />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ArtistBox from '@/components/ArtistBox'
import ArtistView from '../components/ArtistView.vue'
export default {
  name: 'Home',
  data() {
    return {
      artists: [],
    }
  },
  components: {
    ArtistBox: ArtistBox,
    ArtistView: ArtistView
},
  mounted() {
    this.getArtists()
    document.title = 'Home | Spotify-Explorer'
  },
  methods: {
    async getArtists() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get('/api/v1/artists/')
        .then(response => {
          this.artists = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>