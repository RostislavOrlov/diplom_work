let teamPageWebsocket = null;

export function initTeamPageWebsocket() {
    teamPageWebsocket = new WebSocket(`ws://localhost:8000/ws/teams/${localStorage.getItem('userId')}`)
    teamPageWebsocket.onopen = () => {
        console.log("Соединение установлено")
    }
}

export function getTeamPageWebsocket() {
    return teamPageWebsocket;
}

let joinTeamWebsocket = null;
let preferredTeam = null;

export function initJoinTeamWebsocket() {
    joinTeamWebsocket = new WebSocket(`ws://localhost:8000/ws/teams/${localStorage.getItem('userId')}`)
    joinTeamWebsocket.onopen = () => {
        console.log("Соединение установлено2")
    }
    joinTeamWebsocket.onmessage = (event) => {
        console.log(event.data)
        const obj = JSON.parse(event.data)
        console.log(obj.params)
        preferredTeam = obj.params
    }
}

export function getJoinTeamWebsocket() {
    return joinTeamWebsocket;
}

export function getPreferredTeam() {
    return preferredTeam
}


let webSocket = null;

export function getWebsocket() {
    if(webSocket == null) {
        initWebsocket()
    }

    return webSocket
}

export function initWebsocket() {
    webSocket = new WebSocket(`ws://localhost:8000/ws/teams/${localStorage.getItem('userId')}`)
    webSocket.onopen = () => {
        console.log("Соединение установлено (общий вебсокет)")
    }
    webSocket.onmessage = (event) => {
        console.log(event.data)
    }
}


let createPostWebsocket = null;

export function initCreatePostWebsocket() {
    createPostWebsocket = new WebSocket(`ws://localhost:8000/ws/teams/${localStorage.getItem('userId')}`)
    createPostWebsocket.onopen = () => {
        console.log("Соединение установлено (общий вебсокет)")
    }
    
}

export function getCreatePostWebsocket() {
    if(createPostWebsocket == null) {
        initCreatePostWebsocket()
    }

    return createPostWebsocket
}


let postWebsocket = null;

export function initPostWebsocket() {
    postWebsocket = new WebSocket(`ws://localhost:8000/ws/teams/${localStorage.getItem('userId')}`)
    postWebsocket.onopen = () => {
        console.log("Соединение установлено (общий вебсокет)")
    }
    
}

export function getPostWebsocket() {
    if(postWebsocket == null) {
        initPostWebsocket()
    }

    return postWebsocket
}


let editPostWebsocket = null;

export function initEditPostWebsocket() {
    editPostWebsocket = new WebSocket(`ws://localhost:8000/ws/teams/${localStorage.getItem('userId')}`)
    editPostWebsocket.onopen = () => {
        console.log("Соединение установлено (общий вебсокет)")
    }
    
}

export function getEditPostWebsocket() {
    if(editPostWebsocket == null) {
        initEditPostWebsocket()
    }

    return editPostWebsocket
}


let pendReqWebsocket = null;

export function initPendReqWebsocket() {
    pendReqWebsocket = new WebSocket(`ws://localhost:8000/ws/teams/${localStorage.getItem('userId')}`)
    pendReqWebsocket.onopen = () => {
        console.log("Соединение установлено (общий вебсокет)")
    }
    
}

export function getPendReqWebsocket() {
    if(pendReqWebsocket == null) {
        initPendReqWebsocket()
    }

    return pendReqWebsocket
}


let confWebsocket = null;

export function initConfWebsocket() {
    confWebsocket = new WebSocket(`ws://localhost:8086/ws/conf/`)
    confWebsocket.onopen = () => {
        console.log("Соединение установлено (вебсокет конференций)")
    }
    
}

export function getConfWebsocket() {
    if(confWebsocket == null) {
        initConfWebsocket()
    }

    return confWebsocket
}


let manageTeamWebsocket = null;

export function initManageTeamWebsocket() {
    manageTeamWebsocket = new WebSocket(`ws://localhost:8000/ws/teams/${localStorage.getItem('userId')}`)
    manageTeamWebsocket.onopen = () => {
        console.log("Соединение установлено (общий вебсокет)")
    }
    
}

export function getManageTeamWebsocket() {
    if(manageTeamWebsocket == null) {
        initManageTeamWebsocket()
    }

    return manageTeamWebsocket
}


let chatWebsocket = null;

export function initChatWebsocket() {
    chatWebsocket = new WebSocket(`ws://localhost:8084/ws/${localStorage.getItem('userId')}`)
    chatWebsocket.onopen = () => {
        console.log("Соединение установлено (вебсокет чатов)")
    }
    
}

export function getChatWebsocket() {
    if(chatWebsocket == null) {
        initChatWebsocket()
    }

    return chatWebsocket
}


let messagesWebsocket = null;

export function initMessagesWebsocket() {
    messagesWebsocket = new WebSocket(`ws://localhost:8085/ws/${localStorage.getItem('userId')}`)
    messagesWebsocket.onopen = () => {
        console.log("Соединение установлено (вебсокет сообщений)")
    }
    
}

export function getMessagesWebsocket() {
    if(messagesWebsocket == null) {
        initMessagesWebsocket()
    }

    return messagesWebsocket
}


let confContainerWebsocket = null;

export function initConfContainerWebsocket() {
    confContainerWebsocket = new WebSocket(`ws://localhost:8086/ws/conf}`)
    confContainerWebsocket.onopen = () => {
        console.log("Соединение установлено (вебсокет конференций (контейнер конференций))")
    }
    
}

export function getConfContainerWebsocket() {
    if(confContainerWebsocket == null) {
        initConfContainerWebsocket()
    }

    return confContainerWebsocket
}


let ownerWebsocket = null;

export function initOwnerWebsocket(username) {
    console.log(username)
    ownerWebsocket = new WebSocket(`ws://localhost:8086/ws/conf`)
    ownerWebsocket.onopen = () => {
        console.log("Соединение установлено (вебсокет конференций с залом ожидания)")
    }
    
}

export function getOwnerWebsocket(username) {
    if(ownerWebsocket == null) {
        initOwnerWebsocket(username)
    }

    return ownerWebsocket
}
