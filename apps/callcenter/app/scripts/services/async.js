define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name rightApp.Async
   * @description
   * # Async
   * Service in the rightApp.
   */
  angular.module('callcenterApp.services.Async', [])
	.service('Async', function ($http) {
	// AngularJS will instantiate a singleton by calling "new" on this function
	    function get(url, params){
            return $http.get(url, {params: params})
        }

        function save(url, params) {
            var urlArr = url.split('/');
            var len = urlArr.length;
            if (!isNaN(parseInt(urlArr[len-1])) && parseInt(urlArr[len-1]) != NaN) {
                return $http.put(url, {params: params});
            } else {
                return $http.post(url, {params: params});
            }
        }

        function oprnoput(url, params) {
            if (params.Id != undefined) {
                return $http.put(url + params.Id, {params: params})
            } else {
                return $http.post(url, {params: params})
            }
        }

        function oprnoteamput(url, params) {
            if (params.Id != undefined) {
                return $http.put(url + params.Id, {params: params})
            } else {
                return $http.post(url, {params: params})
            }
        }

        function userput(url, params) {
            if (params.Id != undefined) {
                return $http.put(url + params.Id, {params: params})
            } else {
                return $http.post(url, {params: params})
            }
        }

        function del(url) {
            return $http.delete(url, {params: params});
        }

        function softphonedel(url, params) {
            return $http.delete(url + params.Id);
        }

        return {
            get : get,
            save : save,
            oprnoput : oprnoput,
            oprnoteamput : oprnoteamput,
            userput:userput,
            softphonedel: softphonedel,
            del : del
        }
	});
});
