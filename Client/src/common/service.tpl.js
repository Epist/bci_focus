(function(){
    'use strict';
    angular.module('app')
        .service('serviceName', ['dep1', 'dep2', ServicePrototypicalObject]);


    var service, dep1Lib, dep2Lib;

    function ServicePrototypicalObject(dep1, dep2){
        service = this;
        dep1Lib = dep1;
        dep2Lib = dep2;
    }

    ServicePrototypicalObject.prototype.genericFunction = function(arg1, arg2){
        var x = dep1Lib.actionFromDependency();

        return _privateHelperFunction(x, 2);
    };

    function _privateHelperFunction(a, b){
        dep2Lib.anotherAction();
        return a + b;
    }


})();