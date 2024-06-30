<script setup>
    // function changeProfileImg() {
        
    // }
    // function uploadProfileImage(event) {
        // const file = event.target.files[0]
        // const formData = new FormData()
        // formData.append('file', file)
        // fetch(`http://localhost:8087/upload/`, {
        //             method: 'POST',
        //             body: formData
        //         })
        //         .then(response => response.json())
        //         .then(data => {
        //             console.log(data);
        //         })
    // }

    let username = localStorage.getItem('userName')
    let email = localStorage.getItem('userEmail')
</script>

<template>
    <div class="profile">
        <div class="profile-img">
            <!-- <img src="" alt="testImage" @click="changeProfileImg"> -->
        </div>
        <div class="profile-details">
            <div class="profile-name">{{ username }}</div>
            <div class="profile-email">{{ email }}</div>
        </div>
    </div>
    <!-- <form action="" method="post" enctype="multipart/form-data">
    <input type="file" name="file_upload">
    <button type="submit" @change="uploadProfileImage()">Отправить</button> -->
<!-- </form> -->
</template>

<style scoped>
    .profile {
        display: flex;
        padding: 1%;
    }
    .profile-details {
        display: flex;
        flex-direction: column;
    }
    .profile-email {
        color: lightgray;
    }
</style>