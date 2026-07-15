/* =================================================================
   MAIN JAVASCRIPT - Ishan Careers Redesign
   =================================================================
   This file handles all client-side interactivity, including the
   navigation bar, modals, and form submissions.
*/

document.addEventListener('DOMContentLoaded', () => {
  // --- Cache DOM elements for performance ---
  const header = document.getElementById('main-header');
  const modalOverlay = document.getElementById('modal-overlay');

  // --- 1. HEADER SCROLL BEHAVIOR ---
  // This function adds a 'scrolled' class to the header when the user
  // scrolls down, allowing for a style change (e.g., background color).
  const handleScroll = () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  // Attach the scroll event listener
  window.addEventListener('scroll', handleScroll);

  // --- 2. MODAL EVENT LISTENERS ---
  // These listeners handle closing the modal.

  // Close modal when clicking on the overlay background
  modalOverlay.addEventListener('click', (event) => {
    if (event.target === modalOverlay) {
      closeModal();
    }
  });

  // Close modal when the 'Escape' key is pressed
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modalOverlay.classList.contains('active')) {
      closeModal();
    }
  });
});

// --- 3. MODAL CONTROL FUNCTIONS ---
// These functions are globally scoped so they can be called from inline HTML `onclick` attributes.

/**
 * Opens a specific modal by its ID.
 * It ensures any other open modal is closed first.
 * @param {string} modalId - The ID of the modal container to open (e.g., 'login-modal').
 * @param {Event} [event] - Optional event object to prevent default link behavior.
 */
function openModal(modalId, event) {
  if (event) event.preventDefault();

  const modalOverlay = document.getElementById('modal-overlay');
  const modals = modalOverlay.querySelectorAll('.modal-container');
  const targetModal = document.getElementById(modalId);

  // Hide any currently visible modals first
  modals.forEach(modal => modal.style.display = 'none');

  // Show the target modal and the overlay
  if (targetModal) {
    targetModal.style.display = 'block';
    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
  }
}

/**
 * Closes the currently active modal.
 */
function closeModal() {
  const modalOverlay = document.getElementById('modal-overlay');
  modalOverlay.classList.remove('active');
  document.body.style.overflow = ''; // Restore background scrolling
}

// --- 4. FORM HANDLER PLACEHOLDERS ---
// These functions simulate form submission. They prevent the default
// browser action and log the form data.
// LATER, you will replace console.log with a `fetch` call to your Flask API.

/**
 * Handles the signup form submission.
 * @param {Event} event - The form submission event.
 */
function handleSignup(event) {
  event.preventDefault();
  const form = event.target;

  fetch('/signup', { method: 'POST', body: new FormData(form) })
    .then(res => res.json())
    .then(result => {
      if (result.error) {
        alert(result.error);
        return;
      }
      form.innerHTML = '<p style="text-align:center; color: var(--accent-primary); font-weight:600;">✓ Account created! Logging you in...</p>';
      setTimeout(() => {
        closeModal();
        window.location.reload();
      }, 1200);
    })
    .catch(err => console.error('Signup failed:', err));
}
/**
 * Handles the login form submission.
 * @param {Event} event - The form submission event.
 */
function handleLogin(event) {
  event.preventDefault();
  const form = event.target;

  fetch('/signup', { method: 'POST', body: new FormData(form) })
    .then(res => res.json())
    .then(result => {
      if (result.error) { alert(result.error); return; }
      window.location.reload();
    })
    .catch(err => {
      console.error('Signup failed:', err);
      alert('Something went wrong. Check the console.');
    });
}