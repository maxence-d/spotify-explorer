<template>
    <div class="page-artist">
        <div class="columns" v-if="this.artist">
            <div class="column is-3">
                <figure class="image is-640x640 m-3">
                    <img v-bind:src="artist.image_url">
                </figure>
                <h1 class="title m-3 ">{{ artist.name }}</h1>
                <p class="has-text-grey-light m-3">{{ artist.sp_id }}</p>
            </div>
            <div class="columns is-multiline">
                <AlbumBox v-for="album in albums.items" :album="album" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import AlbumBox from '@/components/AlbumBox'
export default {
    name: 'Artist',
    props: ['sp_id'],
    data() {
        return {
            artist: null,
            albums: {}
        }
    },
    mounted() {
        this.getArtist()
        this.getAlbums()
    },
    components: {
        AlbumBox: AlbumBox
    },
    methods: {
        async getArtist() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get(`/api/v1/artist/${this.sp_id}/`)
                .then(response => {
                    this.artist = response.data
                    document.title = this.artist.name + ' | SpotifyExplorer'
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },
        async getAlbums() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get(`/api/v1/sp/artist/${this.sp_id}/albums`)
                .then(response => {
                    this.albums = response.data.sp_albums;
                    console.log(this.albums);
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },

    },
    watch: {
        sp_id: function (newVal) {
            this.getArtist()   // or this.openPopup(newVal) is this suits
            this.getAlbums()
        }
    }
}
</script>