<template>
    <router-link v-bind:to="artist.get_absolute_url" class="column is-2">
        <div class="box">
            <h3 class="is-size-4">{{ artist.name }}</h3>
            <figure class="image m-1">
                <img v-bind:src="artist.image_url">
            </figure>
            <p class="is-size-6 has-text-grey">{{ artist.sp_id }}</p>
        </div>
    </router-link>
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
