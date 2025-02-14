if (window.qrObserver) {
    window.qrObserver.disconnect();
    console.log('MutationObserver disconnected.');
} else {
    console.log('No MutationObserver to disconnect.');
}
