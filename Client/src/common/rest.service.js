(function(){
  angular.module('app')
    .service('RESTService', ['$http', 'API_URL', RESTService]);

  var service, $http, uri, cors_api_url;

  function RESTService(_$http_, _API_URL_){
    service = this;
    $http   = _$http_;
    uri     = _API_URL_;

    
    /*
      This is a temporary fix to a CORS problem: the server only allows same-domain requests in chrome (and other 
      browsers). The cors-anywhere API lets me proxy the server with the proper headers and get around the problem.
      I wouldn't use this in production.
     */
    var cors_api_host = 'cors-anywhere.herokuapp.com'; 
    cors_api_url = 'https://' + cors_api_host + '/';
  }

  RESTService.prototype.get = function(path, header){
    var url = cors_api_url + uri + path;

    var req = {
      method: 'GET',
      url: url,
      headers: header
    };

    return $http(req);

  };
})();