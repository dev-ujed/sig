<template>
	<div class="content">
		<div class="login">
			<div class="login__fondo"></div>
			<div class="login__container">
				<div class="login__img">
					<img src="/static/img/LogoUJEDvertical.png" alt="">
				</div>
				<button @click="login" class="btn btn--gray google-button" id="email" name="email" >
					<div class="google-button__icon">
						<img src="/static/img/google_icon.png" alt="Google">
					</div>
					<p class="google-button__text">Ingresa con Google</p>
				</button>
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