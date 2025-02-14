const COOKIE_MODAL_SELECTOR = '____PH_cookiemodal____';
const COOKIE_CLOSE_BUTTON_SELECTOR = '____PH_cookiedecline____';

// Immediately check for the cookie modal on page load
// window.____P___H____cookieclose____ = ()=>
// {
//   const modal = document.querySelector(COOKIE_MODAL_SELECTOR);
//   if (modal) {
//     console.log("Cookie modal already exists.");
//     const closeBtn = modal.querySelector(COOKIE_CLOSE_BUTTON_SELECTOR);
//     if (closeBtn) {
//       closeBtn.click();
//       console.log('Cookie modal closed by clicking the button.');
//     } else {
//       modal.remove();
//       console.log('Cookie modal removed from the DOM.');
//     }
//   } else {
//     console.log("No existing cookie modal found.");
//   }
// }


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

window.____PH_initcookieobsfn____ = () =>
{
  const cookieModalObserver = new MutationObserver(closeCookieModal);
  cookieModalObserver.observe(document.body, { childList: true, subtree: true });
}
// window.stopCookieModalObserver = () => cookieModalObserver.disconnect();

// window.stopQrObserver = () => window.qrObserver.disconnect();
