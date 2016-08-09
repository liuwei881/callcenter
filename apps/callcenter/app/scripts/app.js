/*jshint unused: vars */

define(['angular', 'controllers/footer', 'controllers/header','controllers/login','controllers/main','controllers/modalinstance','controllers/pagehead','controllers/sidebar','controllers/seattable','controllers/tableset','controllers/softphone','controllers/outrecord','controllers/inrecord','controllers/cellphone','controllers/dailyreport','controllers/report','controllers/serverjudge','controllers/missedcall','controllers/statuscode','directives/paging', 'services/httpinterceptor', 'services/async', 'services/sync', 'directives/ngspinnerbar']/*deps*/, function (angular, MainCtrl, PagingDirective, LoginCtrl,  HeaderCtrl, SidebarCtrl, PageHeadCtrl, FooterCtrl, SeatTableCtrl,TableSetCtrl,SoftPhoneCtrl,OutRecordCtrl,InRecordCtrl,CellPhoneCtrl,DailyReportCtrl,ServerJudgeCtrl,MissedCallCtrl,ReportCtrl,StatusCodeCtrl,HttpInterceptorFactory, ModalinstanceCtrl,NgSpinnerBarDirective)/*invoke*/ {

  'use strict';

  /**
   * @ngdoc overview
   * @name callcenterApp
   * @description
   * # callcenterApp
   *
   * Main module of the application.
   */
  return angular
       .module('callcenterApp', ['callcenterApp.controllers.MainCtrl',
       'callcenterApp.directives.Paging',
       'callcenterApp.controllers.LoginCtrl',
       'callcenterApp.controllers.HeaderCtrl',
       'callcenterApp.controllers.SidebarCtrl',
       'callcenterApp.controllers.PageHeadCtrl',
       'callcenterApp.controllers.FooterCtrl',
       'callcenterApp.controllers.SeatTableCtrl',
       'callcenterApp.controllers.TableSetCtrl',
       'callcenterApp.controllers.SoftPhoneCtrl',
       'callcenterApp.controllers.OutRecordCtrl',
       'callcenterApp.controllers.InRecordCtrl',
       'callcenterApp.controllers.CellPhoneCtrl',
       'callcenterApp.controllers.DailyReportCtrl',
       'callcenterApp.controllers.ServerJudgeCtrl',
       'callcenterApp.controllers.MissedCallCtrl',
       'callcenterApp.controllers.ReportCtrl',
       'callcenterApp.controllers.StatusCodeCtrl',
       'callcenterApp.services.HttpInterceptor',
       'callcenterApp.controllers.ModalInstanceCtrl',
       'callcenterApp.services.Async',
       'callcenterApp.services.Sync',
       'callcenterApp.directives.NgSpinnerBar',
       /*angJSDeps*/'ngCookies','ngResource','ngSanitize','ui.router'])
    .config(function ($stateProvider, $urlRouterProvider) {
       // $httpProvider.interceptors.push('httpInterceptor');
        $stateProvider
            .state('dashboard', {
                url: '/',
                templateUrl: 'views/main.html',
            })
            .state('login', {
                url: '/login',
                templateUrl: 'views/login.html',
                controller: 'LoginCtrl'
            })

            .state('dashboard.seattable', {
                    url: 'seattable',
                    templateUrl: 'views/seattable.html',
                    controller: 'SeatTableCtrl',
                    nav: '坐席管理',
                    needRequest: true
                })
            .state('dashboard.tableset', {
                    url: 'tableset',
                    templateUrl: 'views/tableset.html',
                    controller: 'TableSetCtrl',
                    nav: '坐席组管理',
                    needRequest: true
                })
            .state('dashboard.softphone', {
                    url: 'softphone',
                    templateUrl: 'views/softphone.html',
                    controller: 'SoftPhoneCtrl',
                    nav: '软电话管理',
                    needRequest: true
                })
            .state('dashboard.judge', {
                    url: 'judge',
                    templateUrl: 'views/judge.html',
                    controller: 'ServerJudgeCtrl',
                    nav: '用户评价',
                    needRequest: true
                })
            .state('dashboard.outrecord', {
                    url: 'outrecord',
                    templateUrl: 'views/outrecord.html',
                    controller: 'OutRecordCtrl',
                    nav: '呼出记录',
                    needRequest: true
                })
            .state('dashboard.inrecord', {
                    url: 'inrecord',
                    templateUrl: 'views/inrecord.html',
                    controller: 'InRecordCtrl',
                    nav: '呼入记录',
                    needRequest: true
                })
            .state('dashboard.cellphone', {
                    url: 'cellphone',
                    templateUrl: 'views/cellphone.html',
                    controller: 'CellPhoneCtrl',
                    nav: '呼入手机搜索',
                    needRequest: true
                })
            .state('dashboard.missedcall', {
                    url: 'missedcall',
                    templateUrl: 'views/missedcall.html',
                    controller: 'MissedCallCtrl',
                    nav: '未接来电查询',
                    needRequest: true
                })
            .state('dashboard.dailyreport', {
                    url: 'dailyreport',
                    templateUrl: 'views/dailyreport.html',
                    controller: 'DailyReportCtrl',
                    nav: '每日统计',
                    needRequest: true
                })
            .state('dashboard.report', {
                url: 'report',
                templateUrl: 'views/report.html',
                controller: 'ReportCtrl',
                nav: '报告统计',
            })
            .state('dashboard.statuscode', {
                url: 'statuscode',
                templateUrl: 'views/statuscode.html',
                controller: 'StatusCodeCtrl',
                nav: '状态码统计',
            })


     $urlRouterProvider.otherwise('/');
    })
    .run(function ($rootScope, $state, $stateParams, $cookies) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        $rootScope.$on('$stateChangeStart', function (event, toState, fromState) {
            if (toState.url === '/login') {
                $('body').addClass('login');
            }
            else {
                $('body').removeClass('login');
                if ($cookies.get('user') === undefined) {
                    event.preventDefault();
                    $state.go('login');
                }
            }
        });
    });
    ;
});
