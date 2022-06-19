<template>
    <div class="page-my-account">
        <div class="column is-12">
            <h1 class="title">My account</h1>
        </div>
        <div class="columns">
            <div class="column">
                <div class="box">
                <table class="table">
                    <tbody>
                    <tr>
                        <td>Name</td>
                        <td>{{me.username}}</td>
                    </tr>
                    </tbody>
                </table>
                </div>
            </div>
            <div class="column">
                <SpotifyBox />
            </div>
        </div>
        <div class="column">
            <button @click="logout()" class="button is-danger">Log out</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import SpotifyBox from '@/components/SpotifyBox'

export default {
    name: 'MyAccount',
  components: {
    SpotifyBox: SpotifyBox
  },
    data() {
        return {
            me:{}
        }
    },
    mounted() {
        document.title = 'My account | Spotify-Explorer'
        this.getMe()
    },
    methods: {
        logout() {
            axios.defaults.headers.common["Authorization"] = ""
            this.$store.commit('removeToken')
            this.$router.push('/')
        },
        async getMe() {
            this.$store.commit('setIsLoading', true)

            await axios
                .get('/api/v1/users/me')
                .then(response => {
                    this.me = response.data
                })
                .catch(error => {
                    if (error.response) {
                        console.log(JSON.stringify(error))
                    } else {
                        this.errors.push('Something went wrong. Please try again')
                        console.log(JSON.stringify(error))
                    }
                })

            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>