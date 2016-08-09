define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name callcenterApp.controller:MainCtrl
   * @description
   * # MainCtrl
   * Controller of the callcenterApp
   */
  angular.module('callcenterApp.controllers.MainCtrl', [])
    .controller('MainCtrl', function () {
      this._AuthorCompany_ = 'Ciprun';
    });
});
