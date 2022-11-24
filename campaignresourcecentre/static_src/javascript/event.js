/* eslint-disable */

(function () {
    function recordEvent(group, name, href) {
      if (!window.CRC_SETTINGS.CAMPAIGNS_EVENT_API_ENDPOINT) {
        window.location.href = href;
        return;
      }

      // Send the API request.
      var body = { key: group + ':' + name, date: new Date().toISOString().split('T')[0] };
      var xhr = new XMLHttpRequest();
      xhr.open('POST', window.CRC_SETTINGS.CAMPAIGNS_EVENT_API_ENDPOINT, true),
      xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8'),
      xhr.timeout = 500,
      (xhr.onreadystatechange = function () {
        // Navigate to the href when readyState is DONE (response is received or after 500 milliseconds)
        if (4 === xhr.readyState) {
          window.location.href = href
        }
      }),
      xhr.send(JSON.stringify(body));
    }

    function getEventName(elem) {
      // Use data attribute if supplied.
      var eventName = elem.getAttribute('data-event');
      if (eventName) return eventName;

      // Check if there are child nodes.
      if (elem.hasChildNodes()) {
        // Look for alt on enclosed img tag.
        var image = elem.querySelector('img');
        if (image) {
          eventName = image.getAttribute('alt');
          if (eventName) return eventName;
        }

        // Look for h3 or h4 text.
        var heading = elem.querySelector('h3');
        if (!heading) heading = elem.querySelector('h4');
        if (heading) {
          eventName = heading.innerText;
          if (eventName) return eventName;
        }
      }

      return elem.innerText;
    }

    function addListeners() {
      var main = document.getElementById('main-content');
      var elems = main.querySelectorAll('a');

      // Attach click handlers to each <a> tag in the main content.
      for (let i=0; i<elems.length; i++) {
        elems[i].addEventListener('click', function(e) {
          e.preventDefault();
          recordEvent('crc', getEventName(elems[i]), elems[i].href);
        });
      }
    }

    document.addEventListener("DOMContentLoaded", function () {
      addListeners();
    });
  })();
