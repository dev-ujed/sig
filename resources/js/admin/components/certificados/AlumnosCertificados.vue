<template>
    <div class="db-heading--admin">
        <h1 class="db-heading--admin__title">Lista de certificados</h1>
    </div>

    <div class="contenedor__header container">
        <div class="header__input">
            <form action="" class="db-search-form" @submit.prevent="buscarConstancia">
                <div class="search-wrapper">
                    <input id="search-input"  name="buscar" type="search" placeholder="Buscar por nombre" class="form-field" v-model="buscar">
                    <img class="search-icon" src="/static/img/Icon search.png" alt="Icon filtro">
                </div>
            </form>
        </div>
        <div class="header__button">
            <button class="btn btn--success btn-generar" @click="goToForm">Nuevo</button>
        </div>
    </div>
    
    <div class="container">
        <div class="db-panel">
            <div class="list-container">
                <div class="record" v-for="(constancia, index) in constancias.constancias" :key="index">
                    <div class="record__contaier">
                        <div class="record__container--sub title">
                            <p>{{ constancia.nombre_alumno }} </p>
                            <p>{{ constancia.tipo_constancia_desc }}</p>
                            <p>{{ constancia.nivel }}</p>
                            <p>{{ constancia.calificacion }}</p>
                            <p>{{ constancia.escuela }}</p>
                            <p>{{ constancia.fecha }}</p>
                            <button class="btn btn--blue" @click="editarConstancia(constancia.folio)">Editar</button>
                            <button class="btn btn--danger" @click="openModal(constancia.folio)">Eliminar</button>
                            <button class="btn btn--pdf" @click="downloadPdf(constancia.folio)">
                                Descargar
                                <i class="mdi mdi-file-pdf-box"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Constancia</th>
                            <th>Nivel</th>
                            <th>Calificación</th>
                            <th>Escuela</th>
                            <th>Fecha</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(constancia, index) in constancias.constancias" :key="index">
                            <td>{{ constancia.nombre_alumno }}</td>
                            <td>{{ constancia.tipo_constancia_desc }}</td>
                            <td>{{ constancia.nivel }}</td>
                            <td>{{ constancia.calificacion }}</td>
                            <td>{{ constancia.escuela }}</td>
                            <td>{{ constancia.fecha }}</td>
                            <td><button class="btn btn--blue" @click="editarConstancia(constancia.folio)">Editar</button></td>
                            <td><button class="btn btn--danger" @click="openModal(constancia.folio)">Eliminar</button></td>
                            <td>
                                <button class="btn btn--pdf" @click="downloadPdf(constancia.folio)">
                                Descargar
                                <i class="mdi mdi-file-pdf-box"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <nav role="navegation" class="pagination-container">
                <ul class="pagination pagination--dashboard">
                    <li v-for="page in visiblePages" :key="page">
                        <button 
                            class="pagination-item"
                            :class="{ 'pagination-item--selected': currentPage === page }"
                            @click="changePage(page)"
                            :disabled="currentPage === page"
                        >{{ page }}</button>
                    </li>
                    <li>
                        <button class="pagination-next" @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">
                            <span class="pagination-next__icon"><span class="pagination-next__text">Siguiente</span></span>
                        </button>
                    </li>
                </ul>
            </nav>
        </div>

        <!-- Modal de confirmación -->
        <div v-if="isModalVisible" class="modal">
            <div class="modal-content">
                <h3>¿Eliminar constancia?</h3>
                <p>Esta acción eliminará permanentemente la constancia seleccionada.</p>
                <div class="modal-actions">
                    <button @click="eliminarConstancia(folio)" class="btn btn--danger">Eliminar</button>
                    <button @click="closeModal">Cancelar</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

    export default{
        name: 'alumnoscertificados',
        
        data(){
            return{
                constancias: [],
                currentPage: 1,
                totalPages: 10,
                visiblePages: [],
                isModalVisible: false,
                folio: null,
                buscar: '',
            }
        },

        watch: {
            currentPage(newPage) {
                this.calculateVisiblePages();
            }
        },

        mounted(){
            this.get_constancias_datos();
            this.calculateVisiblePages();
        },

        methods: {
            goToForm() {
                window.location.href = '/admi/certificado/form/';
            },

            editarConstancia(folio) {
                window.location.href = `/admi/certificado/form/?folio=${folio}`;
            },

            openModal(folio) {
                this.folio = folio;
                this.isModalVisible = true;
            },

            closeModal() {
                this.isModalVisible = false;
            },
            
            calculateVisiblePages() {
                const range = 2;
                const start = Math.max(1, this.currentPage - range);
                const end = Math.min(this.totalPages, this.currentPage + range);
                
                this.visiblePages = [];
                for (let i = start; i <= end; i++) {
                    this.visiblePages.push(i);
                }
            },

            changePage(page) {
                if (page === 'next' && this.currentPage < this.totalPages) {
                    this.currentPage++;
                } else if (page === 'prev' && this.currentPage > 1) {
                    this.currentPage--;
                } else {
                    this.currentPage = page;
                }
                this.get_constancias_datos(); 
            },

            buscarConstancia() {
                axios.get(`${this.$root.originPath}/admi/datos_constancias/?buscar=${encodeURIComponent(this.buscar)}&page=${this.currentPage}&page_size=10`)
                    .then(response => {
                    this.constancias = response.data;
                    this.totalPages = response.data.total_pages;
                    this.calculateVisiblePages();
                    })
                    .catch(error => {
                    console.error("Error al buscar constancia:", error);
                    });
            },


            get_constancias_datos(){
                axios.get(`${this.$root.originPath}/admi/datos_constancias/?page=${this.currentPage}&page_size=10`)
                    .then(response => {
                        this.constancias = response.data;
                        this.totalPages = response.data.total_pages;
                    })
                    .catch(error => {
                    console.error("Error al obtener la info:", error);
                });
            },

            eliminarConstancia(folio) {
                axios.delete(`${this.$root.originPath}/admi/delete_constancia/${parseInt(folio)}/`)
                    .then(response => {
                        this.isModalVisible = false,
                        this.get_constancias_datos();
                    })
                    .catch(error => {
                        console.error("Error al eliminar:", error);
                        alert("Ocurrió un error al intentar eliminar la constancia.");
                });
            },

            downloadPdf(folio) {
                window.open(this.$root.originPath + '/admi/const_puali/pdf/'+ folio, '_blank');
            },
        }
    }
</script>

<style>
    .modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    }

    .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    width: 300px;
    }

    .modal-actions button {
    margin: 10px;
    padding: 10px 20px;
    cursor: pointer;
    }

    .modal-actions button:hover {
    opacity: 0.8;
    }

</style>