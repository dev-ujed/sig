<template>
  <aside :class="['sidebar', { 'collapsed': !isOpen }]">
    <section v-for="(item, index) in menu" :key="item.id">
      <div 
        v-if="!item.children"
        class="sidebar-item"
        :data-text="item.text"
        @click="goTo(item.link)"
      >
        <i :class="`mdi ${item.icon} icon`"></i>
        <span class="text">{{item.text}}</span>
      </div>

      <div v-else>
        <div
          class="sidebar-item sub"
          :id="`${item.key}Button`"
          @click="toggleMenu(item.key, item.text)"
        >
          <i :class="`mdi ${item.icon} icon`"></i>
          <span class="text">{{item.text}}</span>
          <i v-if="isMenuOpen[item.key]" class="mdi mdi-chevron-down icon"></i>
          <i v-else class="mdi mdi-chevron-right icon"></i>
        </div>

        <div 
          v-for="(child, index) in item.children" :key="item.id" 
          v-if="isMenuOpen[item.key] && isOpen" 
          class="sidebar-submenu"
        >
          <div 
            class="sidebar-item" 
            @click="goTo(child.link)"
          >
            <i :class="`mdi ${child.icon} icon`"></i>
            <span class="text">{{child.text}}</span>
          </div>
        </div>
      </div>

      <transition name="fade-slide">
        <div
          v-if="isMenuOpen[item.key] && !isOpen"
          class="floating-menu"
          :style="{ top: floatingMenuPosition.top + 'px', left: floatingMenuPosition.left + 'px' }"
        >
        <div style="margin-bottom: 10px;">{{titleSubMenu}}</div>
          <div 
            v-for="(child, index) in item.children" :key="child.id" 
            class="floating-menu-item"
            @click="goTo(child.link)"
          >
            <i :class="`mdi ${child.icon} icon`"></i>
            <span class="text">{{child.text}}</span>
          </div>
        </div>
      </transition>

    </section>
  </aside>
</template>


<script>
  export default {
    name: 'Sidebar',
    props: {
      isOpen: Boolean,
      menu: {
          type: Array,
          required: true
      },
    },
    data() {
      return {
        isMenuOpen: {
        },
        floatingMenuPosition: {
          top: 0,
          left: 0,
        },
        titleSubMenu : '',
        menu2: [
          { id: '1', text: 'Inicio', icon: 'mdi-home', link: 'inicio/' },
          { id: '2', text: 'Perfil', icon: 'mdi-account', link: 'perfil/'},
          {
            id: '3', 
            text: 'Configuración',
            icon: 'mdi-cog',
            key: 'settings',
            children: [
              { id: '1', text: 'Configuración 1', icon: 'mdi-account', link: 'settings1/'},
              { id: '2', text: 'Configuración 2', icon: 'mdi-cog', link: 'settings2/'},
            ],
          },
          {
            id: '4', 
            text: 'Labels',
            icon: 'mdi-cog',
            key: 'labels',
            children: [
              { id: '3', text: 'Label 1', icon: 'mdi-account', link: 'label1/'},
              { id: '4', text: 'Label 2', icon: 'mdi-cog', link: 'label2/' },
            ],
          },
        ],
      };
    },
    methods: {
      toggleMenu(menu, title) {
        if (this.isMenuOpen[menu]) {
          this.isMenuOpen[menu] = !this.isMenuOpen[menu];
        }
        else{
          this.isMenuOpen = {};
          this.isMenuOpen[menu] = !this.isMenuOpen[menu];
        }
        this.titleSubMenu = title;

        this.$nextTick(() => {
          const button = this.$el.querySelector(`#${menu}Button`);
          if (button) {
            const rect = button.getBoundingClientRect();
            const offsetTop = !this.isOpen && this.isMenuOpen[menu] ? rect.top : rect.top + 20;
            const offsetLeft = !this.isOpen && this.isMenuOpen[menu] ? rect.right + 1 : rect.right + 5 - 185;

            this.floatingMenuPosition.top = offsetTop;
            this.floatingMenuPosition.left = offsetLeft;
          }
        });
      },
      goTo(link){
        window.location.href = this.$root.originPath+'/admi/'+link;
      }
    },
  };
</script>

