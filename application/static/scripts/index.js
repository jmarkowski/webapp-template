import { Popover as Popover } from 'bootstrap';

var popoverEl = document.getElementById('popover')
var popover = new Popover(popoverEl)

document.addEventListener('DOMContentLoaded', function () {
  const container = document.getElementById('list-container');
  const button = document.getElementById('list-btn');

  button.addEventListener('click', function () {
    fetch(URL.main_invites, {
      method: 'GET',
    }).then(function (response) {
      if (response.status >= 200 && response.status <= 299) {
        return response.json();
      } else {
        throw Error(response.statusText);
      }
    }).then(function (jsonResponse) {
      if (jsonResponse.emails) {
        const ul = document.createElement('ul');

        jsonResponse.emails.forEach(email => {
          const li = document.createElement('li');
          const liText = document.createTextNode(email);

          li.appendChild(liText);
          ul.appendChild(li);
        });

        container.innerHTML = ul.outerHTML;
      } else {
        container.innerHTML = 'No invitations found!';
      }
    }).catch(function (error) {
      console.log('Request failed: ', error);
      container.innerHTML = 'Sorry, '
        + 'there is an issue communicating with our servers.';
    });
  });
});
