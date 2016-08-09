define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name rightApp.controller:callcenterApp
     * @description
     * # CompanyCtrl
     * Controller of the rightApp
     */
    angular.module('callcenterApp.controllers.InRecordCtrl', [])
        .controller('InRecordCtrl', function ($scope, $cookies,$state, $uibModal, Async) {
            $scope.total = 0;
            $scope.pageSize = 15;
            $scope.page = 1;
            $scope.agentoprno = '';
            $scope.starttimein = '';
            $scope.endtimein = '';
            $scope.Go = function(){
                Async.get('/api/v2/inbill',{agentoprno: $scope.agentoprno,starttimein:$scope.starttimein,endtimein:$scope.endtimein,page:$scope.page,pageSize:$scope.pageSize}).success(function(response){
                    if(response.status == 200){
                        $scope.lstLog = response.rows;
                        $scope.total = response.total;
                    }
                    else{
                        alert(response.info);
                    }
                });
            }

            $scope.initPage = function(){
                $scope.username = $cookies.get('user').substring(0,3);
        };
            $scope.initPage();

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

            $scope.pageAction = function (page) {
            Async.get('/api/v2/inbill',{agentoprno: $scope.agentoprno,starttimein:$scope.starttimein,endtimein:$scope.endtimein,page: page}).success(function (response) {
                    $scope.lstLog = response.rows;
                });
        };

            $scope.inlineOptions = {
                customClass: getDayClass,
                minDate: new Date(),
                showWeeks: true
            };

            $scope.dateOptions = {
                dateDisabled: disabled,
                formatYear: 'yy',
                maxDate: new Date(2020, 5, 22),
                minDate: new Date(),
                startingDay: 1
              };


          function disabled(data) {
            var date = data.date,
              mode = data.mode;
            var d = new Date();
            return mode === "day"&& (date.getDay()===0 && date.getDay()===6);
          }

          $scope.toggleMin = function() {
            $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
            $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
          };

          $scope.toggleMin();

          $scope.open1 = function() {
            $scope.popup1.opened = true;
          };

          $scope.open2 = function() {
            $scope.popup2.opened = true;
          };

          $scope.setDate = function(year, month, day) {
            $scope.dt = new Date(year, month, day);
          };


          $scope.popup1 = {
            opened: false
          };

          $scope.popup2 = {
            opened: false
          };

          var tomorrow = new Date();
          tomorrow.setDate(tomorrow.getDate() + 1);
          var afterTomorrow = new Date();
          afterTomorrow.setDate(tomorrow.getDate() + 1);
          $scope.events = [{
            date: tomorrow,
            status: 'full'
          }, {
            date: afterTomorrow,
            status: 'partially'
          }];

          function getDayClass(data) {
            var date = data.date,
              mode = data.mode;
            if (mode === 'day') {
              var dayToCheck = new Date(date).setHours(0, 0, 0, 0);

              for (var i = 0; i < $scope.events.length; i++) {
                var currentDay = new Date($scope.events[i].date).setHours(0, 0, 0, 0);

                if (dayToCheck === currentDay) {
                  return $scope.events[i].status;
                }
              }
            }

            return '';
          }



        });
});
