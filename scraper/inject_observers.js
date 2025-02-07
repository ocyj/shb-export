console.log("Injecting JS code");

const QR_CODE_SELECTOR = '[data-test-id="QrCode__image"]';

const COOKIE_MODAL_SELECTOR = '[data-test-id="CookieConsent_modal"]';
const COOKIE_CLOSE_BUTTON_SELECTOR = '[data-test-id="CookieConsent__declineButton"]';

// Immediately check for the cookie modal on page load
const modal = document.querySelector(COOKIE_MODAL_SELECTOR);
if (modal) {
  console.log("Cookie modal already exists.");
  const closeBtn = modal.querySelector(COOKIE_CLOSE_BUTTON_SELECTOR);
  if (closeBtn) {
    closeBtn.click();
    console.log('Cookie modal closed by clicking the button.');
  } else {
    modal.remove();
    console.log('Cookie modal removed from the DOM.');
  }
} else {
  console.log("No existing cookie modal found.");
}

function handleQrCodeMutations(mutationsList, observer) {
  mutationsList.forEach((mutation) => {
    console.log('Element with class updated:', mutation);
    // Notify Python without any data
    window.notifyPython();
  });
}

function closeCookieModal(mutationsList, observer) {
  for (const mutation of mutationsList) {
    if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
      mutation.addedNodes.forEach((node) => {
        // Check if the node is an element node
        if (node.nodeType === Node.ELEMENT_NODE) {
          const modal = node.matches(COOKIE_MODAL_SELECTOR)
            ? node
            : node.querySelector(COOKIE_MODAL_SELECTOR);
          if (modal) {
            console.log("Found modal")
            // Option 1: Click the close button if it exists
            const closeBtn = modal.querySelector(COOKIE_CLOSE_BUTTON_SELECTOR);
            if (closeBtn) {
              closeBtn.click();
              console.log('Cookie modal closed by clicking the button.');
            } else {
              // Option 2: Remove the modal from the DOM
              modal.remove();
              console.log('Cookie modal removed from the DOM.');
            }
          }
        }
        else{
          console.log("Found NO modal")
        }
      });
    }
  }
}

window.initQrObserver = () => 
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
      window.notifyPython();
    }
}

const cookieModalObserver = new MutationObserver(closeCookieModal);
cookieModalObserver.observe(document.body, { childList: true, subtree: true });

// window.initQrObserver()

// window.stopCookieModalObserver = () => cookieModalObserver.disconnect();

// window.stopQrObserver = () => window.qrObserver.disconnect();
