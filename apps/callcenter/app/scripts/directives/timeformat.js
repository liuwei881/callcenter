define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc directive
   * @name CallcenterApp.directive:datepicker
   * @description
   * # callcenter
   */
  angular.module('callcenterApp.directives.TimeFormat', [])
    .directive("datepicker",function(){
         return {
    restrict: "E",
    scope:{
      ngModel: "=",
      dateOptions: "=",
      opened: "=",
    },
    link: function($scope, element, attrs) {
      $scope.open = function(event){
        console.log("open");
        event.preventDefault();
        event.stopPropagation();
        $scope.opened = true;
      };

      $scope.clear = function () {
        $scope.ngModel = null;
      };
    },
    templateUrl: 'views/datepicker.html'
  }
})
});
