<template>
    <div class="page-artist">
        <div class="columns is-multiline">
            <div class="column is-9">
                <figure class="image mb-6">
                    <img v-bind:src="artist.get_image">
                </figure>

                <h1 class="title">{{ artist.name }}</h1>

                <p>{{ artist.description }}</p>
            </div>

            <div class="column is-3">
                <h2 class="subtitle">Information</h2>

                <p><strong>Spotify ID: </strong>{{ artist.sp_id}}</p>

            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default {
    name: 'Artist',
    data() {
        return {
            artist: {},
            quantity: 1
        }
    },
    mounted() {
        this.getArtist() 
    },
    methods: {
        async getArtist() {
            this.$store.commit('setIsLoading', true)
            const sp_id = this.$route.params.sp_id
            await axios
                .get(`/api/v1/artist/${sp_id}/`)
                .then(response => {
                    this.artist = response.data
                    document.title = this.artist.name + ' | Djackets'
                })
                .catch(error => {
                    console.log(error)
                })
            
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>