function getTeamsForUser() {
    console.log("STORE USER ID ", localStorage.getItem('userId'))
    var curr = localStorage.getItem('userId')
    // fetch(`http://192.168.1.123:8000/teams/${curr}`, {
        fetch(`http://localhost:8000/teams/${curr}`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const dataJson = JSON.parse(data['result'])
        this.teams = dataJson['teams']
    })
}

export default getTeamsForUser