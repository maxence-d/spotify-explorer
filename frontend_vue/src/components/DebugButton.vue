<template>
    <div class="column">
        <button class="button is-warning" @click="debug()">debug</button>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'DebugButton',
    data() {
        return {
        }
    },
    components: {

    },
    mounted() {
    },
    methods: {
        async debug() {
            console.log("debug start")
            await axios
                .get('/api/v1/sp/artist/2ITljoufW3HYgBnHFsCAIh/albums')
                .then(response => {
                    console.log("debug response")
                    console.log(response.data)
                })
                .catch(error => {
                    console.log("debug error")
                    console.log(error)
                })
            console.log("debug end")
        }
    }
}
</script>