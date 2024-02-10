document.addEventListener('DOMContentLoaded', () => {
  const notification = document.getElementById('notification');
  if (notification) {
    const deleteButton = notification.querySelector('.delete');

    function closeNotification() {
      notification.classList.add('fade-out');
      setTimeout(() =>{
        notification.classList.add('is-hidden');
        notification.classList.remove('fade-out');
      }, 500);
    }

    deleteButton.addEventListener('click', () => {
      closeNotification();
    });

    setTimeout(closeNotification, 3000);
  }
});

document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.file-input') || []).forEach(fileInput => {
    fileInput.onchange = () => {
      if (fileInput.files.length > 0) {
        const fileName = document.querySelector('.file-name');
        fileName.textContent = fileInput.files[0].name;
      }
    };
  });
});

document.addEventListener('DOMContentLoaded', () => {
    function openModal($el) {
      $el.classList.add('is-active');
    }

    function closeModal($el) {
      $el.classList.remove('is-active');
    }

    function closeAllModals() {
      (document.querySelectorAll('.modal') || []).forEach(($modal) => {
        closeModal($modal);
      });
    }

    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
      const modal = $trigger.dataset.target;
      const $target = document.getElementById(modal);

      $trigger.addEventListener('click', () => {
        openModal($target);
      });
    });

    (document.querySelectorAll('.modal-background, .close-modal') || []).forEach(($close) => {
      $close.addEventListener('click', (event) => {
        event.preventDefault();
        const $target = $close.closest('.modal');
        closeModal($target);
      });
    });

    document.addEventListener('keydown', (event) => {
      if(event.key === "Escape") {
        closeAllModals();
      }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const dropdownButton = document.getElementById('dropdown-button');
    const dropdownDashboard = document.getElementById('dropdown-dashboard');

    dropdownButton.addEventListener('click', () => {
      console.log(dropdownDashboard)
      dropdownDashboard.classList.toggle('is-active');
    });

    document.addEventListener('click', function (event) {
      if (!dropdownDashboard.contains(event.target)) {
        dropdownDashboard.classList.remove('is-active');
      }
    });
  });
