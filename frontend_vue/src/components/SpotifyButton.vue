<template>
    <template v-if="$store.state.is_sp_authenticated">
        <p class="button is-success" @click="sp_logout()">
            Signed In
        </p>
    </template>
    <template v-else>
        <button class="button is-warning" @click="sp_do_auth()">Sign in</button>
    </template>
</template>

<script>
import axios from 'axios'
export default {
    name: 'SpotifyButton',
    data() {
        return {
        }
    },
    components: {

    },
    mounted() {
        this.get_sp_auth()
    },
    methods: {
        async sp_logout() {
            await axios
                .get("/api/v1/sp/logout")
                .then(response => {
                    this.$store.state.is_sp_authenticated = response.data.sp_is_auth
                })
                .catch(error => {
                    console.log(error)
                })
        },
        async get_sp_auth() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get("/api/v1/sp_is_auth")
                .then(response => {
                    this.$store.state.is_sp_authenticated = response.data.sp_is_auth
                    if(this.$store.state.is_sp_authenticated){
                        this.refresh_following()
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },
        async refresh_following() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get("/api/v1/sp/me/following")
                .then(response => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },
        async sp_do_auth() {
            this.$store.commit('setIsLoading', true)
            axios.get("/api/v1/sp_get_auth_url")
                .then((response) => {
                    console.log(response.data.url)
                    window.location.replace(response.data.url);
                }).catch(error => {
                    console.log(error)
                });
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>