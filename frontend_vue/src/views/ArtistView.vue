<template>
    <div class="page-artist">
        <div class="columns">
            <div class="column is-3">
                <figure class="image is-640x640" >
                    <img v-bind:src="artist.image_url">
                </figure>


            </div>

            <div class="column is-3">                
                <h1 class="title">{{ artist.name }}</h1>
                <p class="has-text-grey-light">{{ artist.sp_id}}</p>

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