.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
;
.run(function($rootScope, $log, $http, $cookies){
    $http.defaults.header.common['X-CSRFToken'] = $cookies['csrftoken'];
});
