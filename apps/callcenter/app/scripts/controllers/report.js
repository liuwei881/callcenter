define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name callcenterApp.controller:ReportCtrl
     * @description
     * # ReportCtrl
     * Controller of the callcenterApp
     */
    angular.module('callcenterApp.controllers.ReportCtrl', [])
        .controller('ReportCtrl', function ($scope,Async) {
            this._AuthorCompany_ = 'Ciprun';

            Async.get('/api/v2/callcenter/weekly').success(function(response){
                if(response.status == 200){
                    Highcharts.chart('weekly', {
                        title: {
                            text: '呼叫中心周度统计',
                            x: -20 //center
                        },
                        xAxis: {
                            categories: response.xAxis
                        },
                        yAxis: {
                            title: {
                                text: '通话数量'
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
            // 月报表
            Async.get('/api/v2/callcenter/monthly').success(function(response){
                if(response.status == 200){
                    Highcharts.chart('monthly', {
                        title: {
                            text: '呼叫中心月度统计',
                            x: -20 //center
                        },
                        xAxis: {
                            categories: response.xAxis
                        },
                        yAxis: {
                            title: {
                                text: '通话数量'
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
        });
});
