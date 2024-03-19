//notification fade out
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

// file input name
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
// modal
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
//dropdown dashboard
// document.addEventListener('DOMContentLoaded', () => {
//     const dropdownButton = document.getElementById('dropdown-button');
//     const dropdownDashboard = document.getElementById('dropdown-dashboard');

//     dropdownButton.addEventListener('click', () => {
//       console.log(dropdownDashboard)
//       dropdownDashboard.classList.toggle('is-active');
//     });

//     document.addEventListener('click', function (event) {
//       if (!dropdownDashboard.contains(event.target)) {
//         dropdownDashboard.classList.remove('is-active');
//       }
//     });
//   });
//dropdown-createboard-socialmedia
document.addEventListener('DOMContentLoaded', function () {
  const dropdown = document.getElementById('dropdown-create-contact');
  const trigger = dropdown.querySelector('.dropdown-trigger');
  const menu = dropdown.querySelector('.dropdown-menu');
  const selectedOptionsContainer = document.getElementById('selectedOptions');

  trigger.addEventListener('click', function (event) {
    event.stopPropagation();
    dropdown.classList.toggle('is-active');
  });

  document.addEventListener('click', function (event) {
    if (!dropdown.contains(event.target)) {
      dropdown.classList.remove('is-active');
    }
  });



  const dropdownItems = document.querySelectorAll('.dropdown-item');
  dropdownItems.forEach(function (item) {
    item.addEventListener('click', function () {
      if (!item.classList.contains('disabled')) {
        const selectedOption = item.dataset.option;
        const selectedInput = item.dataset.input;
        const selectedIcon = item.dataset.icon;
        const newOption = document.createElement('div');
        newOption.classList.add('buttons', 'has-addons', 'mt-1');
        newOption.innerHTML = `
          <a class="button is-static">
            <span class="icon is-small">
              <i class="${selectedIcon}"></i>
            </span>
            <span>${selectedOption}</span>
          </a>
          <a class="button is-danger remove-button">
            <span class="icon is-small">
              <i class="fas fa-times"></i>
            </span>
          </a>
          <input type="text" name="${item.dataset.input}" class="input is-small" placeholder="Enter link">
        `;
        selectedOptionsContainer.appendChild(newOption);
        item.classList.add('disabled');
      }
    });
  });

  selectedOptionsContainer.addEventListener('click', function (event) {
    const target = event.target.closest('.remove-button');
    if (target) {
      const parentDiv = target.closest('.buttons');
      parentDiv.remove();
      const optionText = parentDiv.querySelector('span:last-child').innerText;
      dropdownItems.forEach(function (item) {
        if (item.dataset.option === optionText) {
          item.classList.remove('disabled');
        }
      });
    }
  });
});

//navbar-dashboard-active
document.addEventListener('DOMContentLoaded', function () {
    const currentUrl = window.location.href;
    const dashboardLink = document.getElementById('dashboard-link');
    const links = document.querySelectorAll('.menu-list a');

    links.forEach(link => {
      if (link.href === currentUrl) {
        link.classList.add('is-active');
      }
    });
  });

//select icon picker
document.addEventListener("DOMContentLoaded", function () {
var selectElements = document.querySelectorAll(".select-icon-picker select");

    selectElements.forEach(function(selectElement) {
        var hiddenInput = selectElement.parentElement.querySelector(".select-hidden-input");

        selectElement.addEventListener("change", function () {
            hiddenInput.value = selectElement.value;

        });
    });
});
