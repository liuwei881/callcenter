define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name rightApp.controller:callcenterApp
     * @description
     * # CompanyCtrl
     * Controller of the rightApp
     */
    angular.module('callcenterApp.controllers.StatusCodeCtrl', [])
        .controller('StatusCodeCtrl', function ($scope, $cookies,$state,Async) {

            $scope.agentoprno = '';
            $scope.startcodetime = '';
            $scope.endcodetime = '';
            $scope.Go = function(){
                //状态码总数
                Async.get('/api/v2/statuscode/count',{agentoprno:$scope.agentoprno,startcodetime:$scope.startcodetime,endcodetime:$scope.endcodetime}).success(function(response){
                $scope.lstLog = response.rows;
                if(response.status == 200){
                    Highcharts.chart('count', {
                        title: {
                            text: '呼叫中心状态码统计',
                            x: -20 //center
                        },
                        xAxis: {
                            categories: response.xAxis
                        },
                        yAxis: {
                            title: {
                                text: '状态码数量'
                            },
                            plotLines: [{
                                value: 0,
                                width: 1,
                                color: '#808080'
                            }]
                        },
                        legend: {
                            layout: 'vertical',
                            align: 'right',
                            verticalAlign: 'middle',
                            borderWidth: 0
                        },
                        plotOptions: {
                            line: {
                                dataLabels: {
                                    enabled: true
                                },
                                enableMouseTracking: false
                            }
                        },
                        series: response.rows
                    });
                }
            });
            //状态码比例
            Async.get('/api/v2/statuscode/count',{agentoprno:$scope.agentoprno,startcodetime:$scope.startcodetime,endcodetime:$scope.endcodetime}).success(function(response){
                $scope.lstLog = response.rows;
                if(response.status == 200){
                    Highcharts.chart('percent', {
                        title: {
                            text: '呼叫中心状态码比例',
                            x: -20 //center
                        },
                        xAxis: {
                            categories: response.xAxis
                        },
                        yAxis: {
                            title: {
                                text: '状态码比例(%)'
                            },
                            plotLines: [{
                                value: 0,
                                width: 1,
                                color: '#808080'
                            }]
                        },
                        legend: {
                            layout: 'vertical',
                            align: 'right',
                            verticalAlign: 'middle',
                            borderWidth: 0
                        },
                        plotOptions: {
                            line: {
                                dataLabels: {
                                    enabled: true
                                },
                                enableMouseTracking: false
                            }
                        },
                        series: response.rowspercent
                    });
                }
            });

            }

            $scope.initPage = function(){
                $scope.username = $cookies.get('user').substring(0,3);

        };
            $scope.initPage();

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
