(function () {
  'use strict';
  var api = {
    get: function (action, params) {
      var api_ver = 3;
      var base_url = ckan.sandbox().client.endpoint;
      params = $.param(params);
      var url = base_url + '/api/' + api_ver + '/action/' + action + '?' + params;
      return $.getJSON(url);
    },
    post: function (action, data) {
      var api_ver = 3;
      var base_url = ckan.sandbox().client.endpoint;
      var url = base_url + '/api/' + api_ver + '/action/' + action;
      return $.post(url, JSON.stringify(data), "json");
    }
  };

  $(document).ready(function () {

    // Initiate display of empty block messages 
    _removeInitLiElement();

    function _removeInitLiElement() {
      $('.group-grid').each(function (el, source) {

        if ($(this).children().length == 0) {
          $(this).parent().children('.group-grid-empty').removeClass('hidden');
        } else {
          $(this).parent().children('.group-grid-empty').addClass('hidden');
        }

      });
    }

    dragula([document.getElementById('site-groups'), document.getElementById('dataguide-groups')])
      .on('dragend', function (el) {
        _removeInitLiElement();
      });

    $('#data-guide-submit-button').on('click', function (e) {
      e.preventDefault();
      var groupItems = $('#dataguide-groups').children();
      var dataGuideItems = [];

      $.each(groupItems, function (key, item) {
        var id = $(item).attr('data-droup-id');
        dataGuideItems.push(id);
      });

      var input = $('#data-guide-items');
      input.val(dataGuideItems.join());
      var form = $('#data-guide-config');
      form.submit();

    });

    $("#data-guide-submit-button").prop("disabled", false);

  });

})($);

