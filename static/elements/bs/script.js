
const scrollToTopBtn = document.getElementById('scrollToTop');

// adding event listener
window.addEventListener('scroll', function() {
    // checking current scroll position
    if (window.scrollY > window.innerHeight * 0.2) {
        // if scrolled beyond 90% viewport show the button
        scrollToTopBtn.classList.add('show');
    } else {
        // Otherwise, hide the button
        scrollToTopBtn.classList.remove('show');
    }
});

// event listener for the smooth scroll
scrollToTopBtn.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});




const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}

const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
  alertTrigger.addEventListener('click', () => {
    appendAlert('Nice, you triggered this alert message!', 'success')
  })
}


