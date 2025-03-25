<template>
    <div class="admin-container">
        <Navbar @toggle-sidebar="toggleSidebar" />
        <div class="admin-main">
            <sidebar-menu 
                    :menu="menu"
                    :relative="true"
                >
            </sidebar-menu>
            <div class="admin-main__content">
                <slot>

                </slot>
            </div>
        </div>
    </div>
</template>
<script>
    import Navbar from './Navbar.vue';
    import Sidebar from './Sidebar.vue';
    import { SidebarMenu } from 'vue-sidebar-menu'
    import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

    export default {
		name: 'admin',

        components: {
            Navbar,
            SidebarMenu
        },

        data() {
            return {
                showSidebar: false,
                menu: [
                    {
                        header: 'S.I.G',
                        hiddenOnCollapse: true
                    },
                    {
                        href: '/',
                        title: 'Unidades',
                        icon: 'bi bi-shield-minus'
                    },
                    {
                        title: 'Profesores',
                        icon: 'bi bi-shield-plus',
                        child: [
                            {
                                href: '/charts/sublink',
                                title: 'Profesor'
                            },
                            {
                                href: '/charts/sublink',
                                title: 'Profesor'
                            }
                        ]
                    }
                ]
            };
        },
        methods: {
            toggleSidebar() {
                this.showSidebar = !this.showSidebar;
            }
        }
    }
</script>