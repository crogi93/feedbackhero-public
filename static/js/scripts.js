document.addEventListener('DOMContentLoaded', function () {
  const notification = document.getElementById('notification');
  const deleteButton = notification.querySelector('.delete');

  function closeNotification() {
    notification.classList.add('fade-out');
    setTimeout(() =>{
      notification.classList.add('is-hidden');
      notification.classList.remove('fade-out');
    }, 500);
  }

  deleteButton.addEventListener('click', function () {
    closeNotification();
  });

  setTimeout(closeNotification, 3000);
});

document.addEventListener('DOMContentLoaded', function () {
  (document.querySelectorAll('.file-input') || []).forEach(fileInput => {
    fileInput.onchange = () => {
      if (fileInput.files.length > 0) {
        const fileName = document.querySelector('.file-name');
        fileName.textContent = fileInput.files[0].name;
      }
    };
  });
});
