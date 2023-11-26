/**
 * accounts Settings - accounts
 */

'use strict';

document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    const deactivateAcc = document.querySelector('#formaccountsDeactivation');

    // Update/reset user image of accounts page
    let accountsUserImage = document.getElementById('uploadedAvatar');
    const fileInput = document.querySelector('.accounts-file-input'),
      resetFileInput = document.querySelector('.accounts-image-reset');

    if (accountsUserImage) {
      const resetImage = accountsUserImage.src;
      fileInput.onchange = () => {
        if (fileInput.files[0]) {
          accountsUserImage.src = window.URL.createObjectURL(fileInput.files[0]);
        }
      };
      resetFileInput.onclick = () => {
        fileInput.value = '';
        accountsUserImage.src = resetImage;
      };
    }
  })();
});
