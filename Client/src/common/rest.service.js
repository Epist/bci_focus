(function () {
    angular.module('app')
        .service('RESTService', ['$http', 'API_URL', RESTService]);

    var service, $http, uri;

    function RESTService(_$http_, _API_URL_) {
        service = this;
        $http = _$http_;
        uri = _API_URL_;
    }

    RESTService.prototype.get = function (path, header) {
        var url = uri + path;

        var req = {
            method: 'GET',
            url: url,
            headers: header
        };

        return $http(req);
    };


})();