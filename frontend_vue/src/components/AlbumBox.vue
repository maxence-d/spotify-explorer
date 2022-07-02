<template>
    <div class="column m-2" :class="cardColor">
        <div class="card m-3 is-radiusless is-shadowless">
            <div class="card-image">
                <figure class="image">
                   
                </figure>
            </div>
            <div class="media">
                <div class="media-left">
                    <figure class="image is-128x128 m-3">
                         <img v-bind:src="album.images[1].url">
                    </figure>
                </div>
                <div class="media-content">
                    <p class="title is-4">{{ album.name }}</p>
                    <p class="subtitle is-6">{{ album.sp_id }}</p>
                </div>
            </div>
            <div class="content">
                hello
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AlbumBox',
    props: {
        album: Object
    },
    computed: {
        cardColor() {
            /*
            var following = this.$store.state.user.following;
            if(following && following.includes(this.artist.sp_id)){
                return "has-background-danger-light";
            }
            else{
                return "";
            }
            */
        }
    }
}
</script>

<style scoped>
.image {
    margin-top: -1.25rem;
    margin-left: -1.25rem;
    margin-right: -1.25rem;
}
</style>
