/*
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

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

