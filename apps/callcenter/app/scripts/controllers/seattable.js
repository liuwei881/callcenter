define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name rightApp.controller:callcenterApp
     * @description
     * # CompanyCtrl
     * Controller of the rightApp
     */
    angular.module('callcenterApp.controllers.SeatTableCtrl', [])
        .controller('SeatTableCtrl', function ($scope, $state, $uibModal, Async, Sync) {

        $scope.total = 0;
        $scope.pageSize = 15;
        $scope.page = 1;
        $scope.searchKey = '';
        $scope.initPage = function(searchKey){
            Async.get('/api/v2/oprno/', {page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
                success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };

        if ($state.current.needRequest) {
            $scope.initPage();
        }

        $scope.Create = function () {
            var oprnolist = JSON.parse(Sync.fetch('/api/v2/seatshow/'));
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'add.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return {};
                    },
                    title: function () {
                        return {'title':'新建坐席','oprnolist': oprnolist};
                    }
                }
            });
            modalInstance.save = function (item) {console.log(item);
                Async.save('/api/v2/oprno/', item).
                    success(function (data) {
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };


        $scope.editoprno = function (i) {
            var oprnolist = JSON.parse(Sync.fetch('/api/v2/seatshow/'));
            var statusshow = JSON.parse("[0,1]");
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'editoprno.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'编辑坐席','oprnolist': oprnolist,'status':statusshow};
                    }
                }
            });
           modalInstance.oprnoput = function (item) {
                Async.oprnoput('/api/v2/oprno/', item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.detailoprno = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'detailoprno.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return '查看';
                    }
                }
            });
        };

        $scope.Search = function (searchKey) {
            $scope.initPage(searchKey);
        };

        $scope.pageAction = function (page) {
            Async.get('/api/v2/oprno/',{page: page}).success(function (data) {
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };

        });
});
