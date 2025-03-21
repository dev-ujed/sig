<template>
	<div class="content">
		<div class="login">
			<div class="login__fondo"></div>
			<div class="login__container">
				<div class="login__img">
					<img src="../../../../static/img/LogoUJEDvertical.png" alt="">
				</div>
				<div class="login__form">
					<button @click="login">Google</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'inicio',
		data() {
			return {
				form: {
					email: '',
					password: ''
				},
				errors: {
					message: '' // Aquí se almacenará el mensaje de error
				}
			};
		},
		methods: {
			login(){
				window.location.href = 'http://localhost:8000/accounts/google/login/';
			}
		}
	};
</script>

<style scoped>
	.error-message {
		color: red;
		font-size: 14px;
		margin-top: 5px;
		text-align: center;
	}
</style>