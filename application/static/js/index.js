'use strict';

document.addEventListener('DOMContentLoaded', function () {
  const container = document.getElementById('list-container');
  const button = document.getElementById('list-btn');

  button.addEventListener('click', function () {
    $.ajax({
      type: 'get',
      url: URL.main_invites,
      contentType: 'application/json',
      }).done(function (data) {
        if (data.emails) {
          const ul = document.createElement('ul');

          data.emails.forEach(email => {
            const li = document.createElement('li');
            const liText = document.createTextNode(email);

            li.appendChild(liText);
            ul.appendChild(li);
          });

          container.innerHTML = ul.outerHTML;
        }
      }).fail(function (data) {
        container.innerHTML = 'Sorry, '
          + 'there is an issue communicating with our servers.';
      });
  });
});
