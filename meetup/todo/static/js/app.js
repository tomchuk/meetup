/*global $, Backbone */
/*jshint unused:false */
var app = app || {};
var ENTER_KEY = 13;
var ESC_KEY = 27;

$(function () {
  'use strict';

  var token = $("meta[name='csrf-token']").attr('content') || '',
    _sync = Backbone.sync;
	Backbone.sync = function(method, model, options) {
    var _url = _.isFunction(model.url) ?  model.url() : model.url;
    _url += _url.charAt(_url.length - 1) == '/' ? '' : '/';
    options = _.extend(options, {
      url: _url
    });

		if (method !== 'fetch') {
			options.beforeSend = function(xhr) {
				xhr.setRequestHeader('X-CSRFToken', token);
			};
		}
		return _sync(method, model, options);
  };

  new app.AppView();
});
