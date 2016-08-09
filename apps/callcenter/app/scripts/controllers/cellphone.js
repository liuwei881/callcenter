define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name rightApp.controller:callcenterApp
     * @description
     * # CompanyCtrl
     * Controller of the rightApp
     */
    angular.module('callcenterApp.controllers.CellPhoneCtrl', [])
        .controller('CellPhoneCtrl', function ($scope, $state, $uibModal, Async) {
            $scope.total = 0;
            $scope.pageSize = 15;
            $scope.page = 1;
            $scope.cellphone = '';
            $scope.Go = function(){
                Async.get('/api/v2/cellphonebill',{'cellphone': $scope.cellphone}).success(function(response){
                    if(response.status == 200){
                        $scope.lstLog = response.rows;
                    }
                    else{
                        alert(response.info);
                    }
                });
            }
            $scope.AudioPlay = function(file,AgentOprno){
                var player = $('#player')
                player.attr('src',"http://cc.iprun.com:81/?act=recordYhj&filename="+file+'&oprno='+AgentOprno);
                player[0].play();
            }
            $scope.listenKey = function(keyEvent){
                if (keyEvent.which === 13){
                    $scope.Go();
                }
            }
        });
});
