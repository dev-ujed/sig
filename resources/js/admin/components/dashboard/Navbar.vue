<template>
    <div>
        <section class="user-bar-admin">
            <button id="user-bar-btn" class="user-bar-admin__btn" @click="$emit('toggle-sidebar')">
                {{ isSidebarOpen ? ' ☰ ' : ' ☰' }}
                <span class="user-bar-admin__btn-text">S.I.G</span>
                <span class="user-bar-admin__btn-text-large">Sistema de Indicadores y Monitoreo</span>
            </button>
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
                        <a :href="logoutUrl" class="user-bar-admin__profile-menu-link">
                            Cerrar sesión
                        </a>
                    </li>
                </ul>
            </div>
        </section>
    </div>
</template>
  
<script>
    export default {
        name: 'Navbar',
        data() {
            return {
                logoutUrl: '',
            };
        },
        props: {
            isSidebarOpen: Boolean,
        },
        mounted() {
                this.logoutUrl = this.$root.originPath+ '/logout/';
        },
    };
</script>

<style>
.navbar {
  width: 100%;
  height: 60px;
  background: #222;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
  font-size: 18px;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  margin-right: 15px;
}

.navbar h2 {
  color: white;
}
</style>