angular
.module('recoverPasswordView', [])
.controller('recoverPasswordViewCtrl', function($scope, $http) {

	$scope.guideText = "Recuerda que tu contraseña debe tener 8 caracteres";
	$scope.validPassword = false;
	$scope.validPasswordConfimation = false;
	$scope.disabled = true;
	$scope.normal = true;
	$scope.password = "";
	$scope.passwordConfimation = "";
	$scope.successfulChanged = false;

	$scope.isAValidPassword = function(){
		if( $scope.password.length < 8 ){
			$scope.guideText = "La contraseña debe tener 8 caracteres.";
			$scope.validPassword = false;
			$scope.normal = false;
		}else{
			$scope.guideText = "Así está bien.";
			$scope.validPassword = true;
			$scope.normal = true;
		}
		$scope.disabled = !($scope.validPassword && $scope.validPasswordConfimation);
	};

	$scope.isAValidPasswordConfirmation = function(){
		if( $scope.password != $scope.passwordConfirmation ){
			$scope.guideText = "Las contraseñas no coinciden."
			$scope.validPasswordConfimation = false;
			$scope.normal = false;
		}else{
			$scope.guideText = "Ahora sí";
			$scope.validPasswordConfimation = true;
			$scope.normal = true;
		}
		$scope.disabled = !($scope.validPassword && $scope.validPasswordConfimation);
	};

	$scope.changePassword = function(){
		var token = window.location.pathname.split('/')[2];
		$http.post("/api/reset-password/", {
			'token': token,
			'password': $scope.password
		})
		.then(function(response) {
			$scope.successfulChanged = true;
		});
	};
});