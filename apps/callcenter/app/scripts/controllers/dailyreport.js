define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name rightApp.controller:callcenterApp
     * @description
     * # CompanyCtrl
     * Controller of the rightApp
     */
    angular.module('callcenterApp.controllers.DailyReportCtrl', [])
        .controller('DailyReportCtrl', function ($scope, $state, $uibModal, Async) {
             $scope.Go = function(){
                Async.get('/api/v2/dailyreport/'+$scope.cellphone).success(function(response){
                    if(response.status == 200){
                        $scope.result = response.rows;
                        $scope.admin = response.admin;
                    }
                    else{
                        alert(response.info);
                    }
                });
            }

            $scope.initPage = function(){
            Async.get('/api/v2/dailyreport/').
                success(function (data) {
                    $scope.result = data.rows;
                    $scope.username = data.username.substring(0,3);
                });
        };

            $scope.initPage();

            $scope.listenKey = function(keyEvent){
                if (keyEvent.which === 13){
                    $scope.Go();
                }
            }
        });
});
