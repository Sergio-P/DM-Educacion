"use strict";

let app = angular.module("Educacion",[]);

app.controller("MainController",function($scope){
    var self = $scope;
    self.page = 1;

    self.setPage = (i) => {
    	self.page = i;
    };

});