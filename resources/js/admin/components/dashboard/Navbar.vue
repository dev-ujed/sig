<template>
    <div>
        <section class="navbar-jiji">
            <!-- <button id="user-bar-btn" class="user-bar-admin__btn" @click="$emit('toggle-sidebar')">
                <img class="user-bar-admin__btn-icon" src="/static/img/Hamburger.png" alt="Menú Icon">
                <span class="user-bar-admin__btn-text">S.I.G</span>
                <span class="user-bar-admin__btn-text-large">Sistema de algo</span>
            </button> -->
            <div class="user-bar-admin__profile">
                <div class="user-bar-admin__avatar-container">
                    <img class="user-bar-admin__avatar" src="/static/img/icono-user.png" alt="Icono user">
                </div>
                <p class="user-bar-admin__user-name">{{name}} {{ lastname }}</p>
                <ul class="user-bar-admin__profile-menu">
                    <li class="user-bar-admin__profile-menu-item user--info center-text">
                        <div class="user-bar-admin__menu-avatar-container">
                            <img class="user-bar-admin__menu-avatar" src="/static/img/icono-user.png" alt="Icono user">
                            <p class="mt-2 mb-3">{{name}} {{ lastname }}</p>
                        </div>
                    </li>
                    <li class="user-bar-admin__profile-menu-item">
                        <a :href="logout" class="user-bar-admin__profile-menu-link">
                            Cerrar sesión
                        </a>
                    </li>
                </ul>
            </div> 
            hihi
        </section>
    </div>
</template>

<script>
	export default {
		name: 'navbar',
		data() {
			return {
                logout: '',
                name: '',
                lastname: '',
			};
		},
		methods: {
			
		},
        mounted() {
            const useDiv = document.getElementById('user');
            this.logout = useDiv.dataset.url;
            this.name = useDiv.dataset.name;
            this.lastname = useDiv.dataset.lastname;
        },
	};
</script>

<style>
.navbar-jiji{
    background-color: #2a2a2e;
    height: 60px;
}
</style>