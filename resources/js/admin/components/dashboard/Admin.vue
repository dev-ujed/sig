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
        isSidebarOpen: true, // Ahora está correctamente definido en data()
      };
    },
  
    methods: {
      toggleSidebar() {
        this.isSidebarOpen = !this.isSidebarOpen;
      },
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