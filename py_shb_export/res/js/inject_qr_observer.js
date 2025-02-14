const QR_CODE_SELECTOR = '____PH_qrsel____';

function handleQrCodeMutations(mutationsList, observer) {
    mutationsList.forEach((mutation) => {
      console.log('Element with class updated:', mutation);
      window.____PH_pycallback____();
    });
}

window.____PH_initqrobs____ = () => 
{
    console.log("init QR observer")
    const targetNode = document.querySelector(QR_CODE_SELECTOR);
    if (targetNode) {
        console.log('MutationObserver initialized for QrCode__image.');
        const config = { attributes: true, childList: true, subtree: true };
        window.qrObserver = new MutationObserver(handleQrCodeMutations);
        window.qrObserver.observe(targetNode, config);
    } else {
        console.log('QR code element not found.');
        // Notify Python that the element was not found
        //window.notifyPython();
    }
}
