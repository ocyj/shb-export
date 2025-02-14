const QR_CODE_SELECTOR = '[data-test-id="QrCode__image"]';

const targetNode = document.querySelector(QR_CODE_SELECTOR);
if (targetNode) {
    console.log('MutationObserver initialized for QrCode__image.');
    const config = { attributes: true, childList: true, subtree: true };
    const callback = function(mutationsList, observer) {
        for(const mutation of mutationsList) {
            console.log('Element with class updated:', mutation);
            // Notify Python without any data
            window.notifyPython();
        }
    };
    // Assign the observer to a global variable
    window.qrObserver = new MutationObserver(callback);
    window.qrObserver.observe(targetNode, config);
} else {
    console.log('QR code element not found.');
    // Notify Python that the element was not found
    window.notifyPython();
}

// Add a function to quit observer
window.stopQrObserver = () => window.qrObserver.disconnect();
