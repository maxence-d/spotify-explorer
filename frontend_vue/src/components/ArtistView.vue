<template>
    <div class="page-artist">
        <div class="columns" v-if="this.artist">
            <div class="column is-3">
                <figure class="image is-640x640">
                    <img v-bind:src="artist.image_url">
                </figure>
            </div>

            <div class="column is-3">
                <h1 class="title">{{ artist.name }}</h1>
                <p class="has-text-grey-light">{{ artist.sp_id }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Artist',
    props: ['sp_id'],
    data() {
        return {
            artist: null
        }
    },
    mounted() {
    },
    methods: {
        async getArtist() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get(`/api/v1/artist/${this.sp_id}/`)
                .then(response => {
                    this.artist = response.data
                    document.title = this.artist.name + ' | Djackets'
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        }
    },
    watch: {
        sp_id: function(newVal){
            this.getArtist()   // or this.openPopup(newVal) is this suits
        }
    }
}
</script>