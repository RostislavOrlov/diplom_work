var peerConnection = null;

export function initPeerConnection(config) {
    if(peerConnection == null) {
        peerConnection = new RTCPeerConnection(config)
    } 
}

export function getPeerConnection() {
    return peerConnection;
}
