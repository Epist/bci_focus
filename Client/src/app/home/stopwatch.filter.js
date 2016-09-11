(function () {
    'use strict';

    angular.module('app').filter('hhmmss', function () {
        return function (time) {
            var ms_num = parseInt(time, 10);
            var sec_num = ms_num / 100; // don't forget the second param
            var hours = Math.floor(sec_num / 3600);
            var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
            var seconds = Math.floor(sec_num - (hours * 3600) - (minutes * 60));
            var ms = ms_num % 100;
            if (hours < 10) {
                hours = "0" + hours;
            }
            if (minutes < 10) {
                minutes = "0" + minutes;
            }
            if (seconds < 10) {
                seconds = "0" + seconds;
            }
            if (ms < 10) {
                ms = "0" + ms;
            }
            var current_time = hours + ':' + minutes + ':' + seconds + "." + ms;
            return current_time;
        };
    });
})();