define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name callcenterApp.controller:RoleCtrl
     * @description
     * # RoleCtrl
     * Controller of the callcenterApp
     */
    angular.module('callcenterApp.controllers.RoleCtrl', [])
        .controller('RoleCtrl', function ($scope, $state, $uibModal, Async, Sync) {

        $scope.total = 0;
        $scope.pageSize = 15;
        $scope.page = 1;
        $scope.searchKey = '';
        $scope.initPage = function(searchKey){
            Async.get('/api/v2/roles/', {page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
                success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                    $scope.success = data.success;
                    $scope.username = data.username;
                });
        };

        if ($state.current.needRequest) {
            $scope.initPage();
        }

        $scope.Create = function () {
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
                        return {'title':'新建角色'};
                    }
                }
            });
            modalInstance.save = function (item) {console.log(item);
                Async.save('/api/v2/roles/',item).
                    success(function (data) {
                        modalInstance.close();
                        $scope.initPage();
                    }).error(function (data){
                        $scope.initPage();
                    });
            };
        };

        $scope.editrole = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'editrole.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'编辑角色'};
                    }
                }
            });
           modalInstance.roleput = function (item) {
                Async.roleput('/api/v2/roles/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    }).error(function (data){
                        $scope.initPage();
                    });
            };
        };

        $scope.detailrole = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'detailrole.html',
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

        $scope.deleterole = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'deleterole.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'删除角色'};
                    }
                }
            });
           modalInstance.roledel = function (item) {
                Async.roledel('/api/v2/roles/',item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    }).error(function (data){
                        $scope.initPage();
                    });
            };
        };

        $scope.roleright = function (RoleId) {
            var allmenu = JSON.parse(Sync.fetch('/api/v2/menu/'));
            console.log(allmenu);
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'roleright.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return Sync.showroleright('/api/v2/role/member/', RoleId).then(function(succ){
                            return succ.data.rows;
                            });
                    },
                    title: function () {
                        return {'title':'角色权限分配','allmenu':allmenu};
                    }
                }
            });
           modalInstance.saveroleright = function (item) {
                Async.saveroleright('/api/v2/role/member/', item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.userrole = function (RoleId) {
            var companylist = JSON.parse(Sync.fetch('/api/v2/departfunc/'));
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'userright.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return Sync.showuserrole('/api/v2/user/role/', RoleId).then(function(succ){
                            return succ.data.rows;
                            });
                    },
                    title: function () {
                        return {'title':'用户分配','companylist': companylist};
                    }
                }
            });
           modalInstance.saveuserrole = function (item) {
                Async.saveuserrole('/api/v2/user/role/', item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Search = function (searchKey) {
            $scope.initPage(searchKey);
        };

        $scope.pageAction = function (page) {
            Async.get({page: page}).success(function (data) {
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };



        });
});
