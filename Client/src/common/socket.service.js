(function(){
    'use strict';
    angular.module('app')
        .service('socketService', ['$http', 'API_URL', SocketService]);


    function SocketService(){

    }

    SocketService.prototype.genericFunction = function(arg1, arg2){

    };


})();