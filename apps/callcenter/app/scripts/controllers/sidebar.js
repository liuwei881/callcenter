define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name callcenterApp.controller:SidebarCtrl
     * @description
     * # SidebarCtrl
     * Controller of the callcenterApp
     */
    angular.module('callcenterApp.controllers.SidebarCtrl', [])
        .controller('SidebarCtrl', function ($scope, $cookies, Async) {

            $scope.$on('$includeContentLoaded', function () {
                Layout.initSidebar();
            });

            $scope.pageSidebarClosed= false;
            $scope.initPage = function(){
                $scope.username = $cookies.get('user').substring(0,3);
        };
            $scope.initPage();
        });
});
