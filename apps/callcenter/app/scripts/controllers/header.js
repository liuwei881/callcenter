define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name rightApp.controller:HeaderCtrl
     * @description
     * # HeaderCtrl
     * Controller of the rightApp
     */
    angular.module('callcenterApp.controllers.HeaderCtrl', [])
        .controller('HeaderCtrl', function ($scope,$cookies,$state,$uibModal,$http,Async) {

            $scope.initPage = function(){
            Async.get('/api/v2/username/').
                success(function (data) {
                    $scope.username = data.username;
                    $scope.rows = data.rows;
                });
        };

            $scope.$on('$includeContentLoaded', function () {
                Layout.initHeader();
                $scope.initPage();
            });

            $scope.Logout = function() {
                $cookies.remove('user');
                $http.get('/api/v2/logout');
                $state.go('login');

            };

            $scope.edit = function () {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'edit.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[0];
                    },
                    title: function () {
                        return {'title':'修改密码'};
                    }
                }
            });
           modalInstance.userput = function (item) {
                Async.userput('/api/v2/changepasswd/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.person = function () {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'person.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[0];
                    },
                    title: function () {
                        return {'title':'修改个人资料'};
                    }
                }
            });
           modalInstance.userput = function (item) {
                Async.userput('/api/v2/username/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        });
});
