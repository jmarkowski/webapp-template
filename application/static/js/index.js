$(document).ready(function () {
  $container = $('#js-container');

  $container.html(HTML.contents);

  $('#js-btn').on('click', function () {
    $.ajax({
      type: 'get',
      url: URL.main_invites,
      contentType: 'application/json',
      }).done(function (data) {
        if (data.emails) {
          $container.find('div').html('<ul></ul>');
          data.emails.forEach(email => {
            $container.find('ul').append('<li>' + email + '</li>');
          });
        }
      }).fail(function (data) {
        $container.find('div').html('Sorry, '
          + 'there is an issue communicating with our servers.');
      });
  });
});
