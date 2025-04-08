<template>
  <aside :class="['sidebar', { 'collapsed': !isOpen }]">
    <div class="sidebar-item" data-text="Inicio">
      <i class="mdi mdi-home icon"></i>
      <span class="text">Inicio</span>
    </div>

    <div class="sidebar-item" data-text="Perfil">
      <i class="mdi mdi-account icon"></i>
      <span class="text">Perfil</span>
    </div>

    <div
      class="sidebar-item sub"
      ref="settingsButton"
      @click="toggleMenu('settings')"
    >
      <i class="mdi mdi-cog icon"></i>
      <span class="text">Configuración</span>
      <i v-if="isMenuOpen.settings" class="mdi mdi-chevron-down icon"></i>
      <i v-else class="mdi mdi-chevron-right icon"></i>
    </div>

    <div v-if="isMenuOpen.settings && isOpen" class="sidebar-submenu">
      <div class="sidebar-item">
        <i class="mdi mdi-account icon"></i>
        <span class="text">Subopción 1</span>
      </div>
      <div class="sidebar-item">
        <i class="mdi mdi-cog icon"></i>
        <span class="text">Subopción 2</span>
      </div>
    </div>

    <transition name="fade-slide">
      <div
        v-if="isMenuOpen.settings && !isOpen"
        class="floating-menu"
        :style="{ top: floatingMenuPosition.top + 'px', left: floatingMenuPosition.left + 'px' }"
      >
      <div style="margin-bottom: 10px;">Configuración</div>
        <div class="floating-menu-item">
          <i class="mdi mdi-account icon"></i>
          <span class="text">Subopción 1</span>
        </div>
        <div class="floating-menu-item">
          <i class="mdi mdi-cog icon"></i>
          <span class="text">Subopción 2</span>
        </div>
      </div>
    </transition>
  </aside>
</template>


<script>
  export default {
    name: 'Sidebar',
    props: {
      isOpen: Boolean,
    },
    data() {
      return {
        isMenuOpen: {
          settings: false,
        },
        floatingMenuPosition: {
          top: 0,
          left: 0,
        },
      };
    },
    methods: {
      toggleMenu(menu) {
        this.isMenuOpen[menu] = !this.isMenuOpen[menu];

        if (!this.isOpen && this.isMenuOpen[menu]) {
          this.$nextTick(() => {
            const button = this.$refs[`${menu}Button`];
            if (button) {
              const rect = button.getBoundingClientRect();
              this.floatingMenuPosition.top = rect.top;
              this.floatingMenuPosition.left = rect.right + 5;
            }
          });
        }
      },
    },
  };
</script>

