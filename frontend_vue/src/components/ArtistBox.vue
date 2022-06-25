<template>
    <div class="column is-3">
    <div class="box" @click="this.$store.commit(`setCurrentArtist`,artist.sp_id)">
        <h3 class="is-size-4">{{ artist.name }}</h3>
        <figure class="image m-1">
            <img v-bind:src="artist.image_url">
        </figure>
        <p class="is-size-6 has-text-grey">{{ artist.sp_id }}</p>
    </div></div>
</template>

<script>
export default {
    name: 'ArtistBox',
    props: {
        artist: Object
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
