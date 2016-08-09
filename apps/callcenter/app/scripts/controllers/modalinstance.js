define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name rightApp.controller:ModalInstanceCtrlCtrl
     * @description
     * # ModalInstanceCtrlCtrl
     * Controller of the rightApp
     */
    angular.module('callcenterApp.controllers.ModalInstanceCtrl', ['ui.bootstrap', 'ui.bootstrap.tpls'])
        .controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, item, title) {

            $scope.item = item;
            $scope.title = title;
            $scope.Save = function () {
                $uibModalInstance.save($scope.item);
            };

            $scope.Delete = function () {
                $uibModalInstance.Delete($scope.item);
            };

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };
            $scope.diyfun = function (params) {
                $uibModalInstance.diyfun(params);
            };

            $scope.oprnoput = function () {
                $uibModalInstance.oprnoput($scope.item);
            };

            $scope.userput = function () {
                $uibModalInstance.userput($scope.item);
            };

            $scope.oprnoteamput = function () {
                $uibModalInstance.oprnoteamput($scope.item);
            };

            $scope.softphonedel = function () {
                $uibModalInstance.softphonedel($scope.item);
            };
        });
});
