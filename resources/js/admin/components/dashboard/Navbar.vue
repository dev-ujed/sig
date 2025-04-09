<template>
    <nav class="navbar">
        <button class="toggle-btn" @click="$emit('toggleSidebar')">
        {{ isSidebarOpen ? '☰' : '☰' }}
        </button>
        <h2>S.I.G</h2>
    </nav>
</template>
  
<script>
    export default {
        name: 'Navbar',
        props: {
            isSidebarOpen: Boolean, // Asegúrate de definirlo aquí correctamente
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