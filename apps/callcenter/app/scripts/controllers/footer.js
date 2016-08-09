define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name callcenterApp.controller:FooterCtrl
     * @description
     * # FooterCtrl
     * Controller of the callcenterApp
     */
    angular.module('callcenterApp.controllers.FooterCtrl', [])
        .controller('FooterCtrl', function ($scope) {

            $scope.$on('$includeContentLoaded', function () {
                Layout.initFooter(); // init footer
            });
        });
});
