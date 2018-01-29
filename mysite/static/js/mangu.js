var app = angular.module('myApp', []);

app.controller('myCtrl', function($scope, $http) {
    $scope.$watch("iurl", function(newVal, oldVal) {
        if (newVal !== oldVal) {
            var myurl = url_for_angular + '?url=' + $scope.iurl;
            $http.get(myurl).then(function(response){
                var result = JSON.parse(JSON.stringify(response.data));
                if ( result['url_checked'] ) {
                    $scope.url_checked = result['url_checked'];
                    $scope.mismath_url = result['mismath_url'];
                    $scope.len_keywords = result['len_keywords'];
                    $scope.output_list = result['output_list'];
                    $scope.remain = result['remain'];
                    var oll = result['output_list'].length;
                };
            });
        }
    });
});
