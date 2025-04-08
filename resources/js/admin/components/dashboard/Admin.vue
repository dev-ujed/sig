<template>
    <div class="layout">
      <Navbar :isSidebarOpen="isSidebarOpen" @toggleSidebar="toggleSidebar" />
      <div class="main-container">
        <Sidebar :isOpen="isSidebarOpen" />
        <main class="content">
          <h1>Bienvenido</h1>
          <p>Aquí va el contenido...</p>
        </main>
      </div>
    </div>
  </template>
  
  <script>
  import Navbar from './Navbar.vue';
  import Sidebar from './Sidebar.vue';
  
  export default {
    name: 'Admin',
    components: { Navbar, Sidebar },
  
    data() {
      return {
        isSidebarOpen: true,
        windowWidth: window.innerWidth,
        windowHeight: window.innerHeight,
      };
    },
    
    mounted() {
      window.addEventListener('resize', this.handleResize);
    },

    beforeDestroy() {
      window.removeEventListener('resize', this.handleResize);
    },

    methods: {
      toggleSidebar() {
        this.isSidebarOpen = !this.isSidebarOpen;
      },

      handleResize() {
        this.windowWidth = window.innerWidth;
        this.windowHeight = window.innerHeight;
        if (window.innerWidth <= 768) {
          this.isSidebarOpen = false;
        }
      }
    },
  };
  </script>
  

<style>


.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-container {
  display: flex;
  flex: 1;
}
.content {
  flex: 1;
  padding: 20px;
  background: #f5f5f5;
}
</style>