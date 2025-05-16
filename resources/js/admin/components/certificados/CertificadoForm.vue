<template>
    <div class="db-heading--admin">
        <h1 class="db-heading--admin__title">Generar certificado</h1>
    </div>
    <section class="section container">
        <div class="db-panel">
            <div class="db-panel__title"><p class="mt-3">Formulario</p></div>
            <form action="" @submit.prevent="generarCertificado">
                <div class="formulario">
                    <div class="form-group">
                        <label for="nombre">Alumno</label>
                        <input type="text" class="form-field" id="nombre"  v-model="nombre">
                    </div>
                    <div class="form-group">
                        <label for="">Tipo de constancia</label>
                        <select name="" id="" class="select-field form-field" v-model="tipoConstancia" @change="actualizarNivel">
                            <option value="" disabled selected>Seleccione un tipo de constancia</option>
                            <option
                                v-for="tipo in tipos_constancias"
                                :key="tipo.tipo_constancia_id"
                                :value="tipo.tipo_constancia_id"
                            >
                                {{ tipo.tipo_constancia_desc }}
                            </option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="">Nivel</label>
                        <select name="" id="" class="select-field form-field"  v-model="nivel">
                            <option value="" disabled selected>Seleccione un nivel</option>
                            <option value="A1">A1</option>
                            <option value="A2">A2</option>
                            <option value="B1">B1</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="calificacion">Calificación</label>
                        <input type="number" step="0.1" class="form-field" id="calificacion" v-model="calificacion">
                    </div>
                    <div class="form-group">
                        <label for="">Escuela</label>
                        <select name="" id="" class="select-field form-field" v-model="escuelaSeleccionada">
                            <option value="" disabled selected>Seleccione la escuela</option>
                            <option
                                v-for="escuela in escuelas"
                                :key="escuela.cve_escuela"
                                :value="escuela.cve_escuela"
                            >
                                {{ escuela.escuela_imprime_contenido }}
                            </option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="fecha">Fecha</label>
                        <input type="date" class="form-field" id="fecha" v-model="fechaActual">
                    </div>

                    <div class="button-container">
                        <button class="btn btn--success" v-if="!esEdicion">Generar</button>
                        <button class="btn btn--blue" v-else @click.prevent="editarCertificado">Editar</button>
                    </div>
                </div>
            </form>
        </div>
    </section>
</template>
<script>
    import axios from 'axios';
    
    export default {
        
		name: 'certificadoform',

        data(){
            return{
                fechaActual: '',
                tipoConstancia: '',
                nivel: '',
                escuelas: [],
                tipos_constancias: [],
                escuelaSeleccionada: "",
                nombre: '',
                calificacion: null,
                esEdicion: false,
            };
        },

        mounted(){
            const urlParams = new URLSearchParams(window.location.search);
            const folio = urlParams.get('folio');

            this.getEscuelas();
            this.getTiposConstancias();

            if (folio) {
                this.esEdicion = true;
                this.getConstancia(folio);
            }
        },

        methods:{
            getConstancia(folio) {
                axios.get(`http://127.0.0.1:8000/admi/get_constancia/${folio}/`)
                    .then(response => {
                        const data = response.data;

                        this.nombre = data.nombre_alumno;
                        this.tipoConstancia = data.tipo_constancia;
                        this.nivel = data.nivel;
                        this.calificacion = data.calificacion;
                        this.escuelaSeleccionada = data.escuela;
                        this.fechaActual = data.fecha;
                        

                        console.log(data);

                    })
                    .catch(error => {
                        console.error("Error al obtener los datos de la constancia:", error);
                    });
            },

            editarCertificado() {
                const urlParams = new URLSearchParams(window.location.search);
                const folio = urlParams.get('folio');

                const datos = {
                    nombre: this.nombre,
                    tipoConstancia: this.tipoConstancia,
                    nivel: this.nivel,
                    calificacion: this.calificacion,
                    escuela: this.escuelaSeleccionada,
                    fecha: this.fechaActual,
                };

                axios.put(`http://127.0.0.1:8000/admi/update_constancia/${folio}/`, datos, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => {
                        alert("Constancia editada exitosamente.");
                        console.log(response.data);
                    })
                    .catch(error => {
                        alert("Error al editar constancia.");
                        console.error(error);
                    });
            },

            generarCertificado() {
                const datos = {
                    nombre: this.nombre,
                    tipoConstancia: this.tipoConstancia,
                    nivel: this.nivel,
                    calificacion: this.calificacion,
                    escuela: this.escuelaSeleccionada,
                    fecha: this.fechaActual,
                };

                axios.post('http://127.0.0.1:8000/admi/generar_certificado/', datos, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => {
                        alert("Certificado generado exitosamente.");
                        this.limpiarFormulario();
                        console.log(response.data);
                    })
                    .catch(error => {
                        alert("Error al generar certificado.");
                        console.error(error);
                    });
            },

            getTiposConstancias(){
                axios.get('http://127.0.0.1:8000/admi/tipos_constancias/')
                    .then(response => {
                        this.tipos_constancias = response.data;
                    })
                    .catch(error => {
                        console.error("Error al traer los tipos de constancias: ", error);
                    })
            },

            mapTipoConstancia(id) {
                switch (id) {
                    case 1: return 'egreso';
                    case 2: return 'basica';
                    case 3: return 'nivel';
                    default: return '';
                }
            },

            getEscuelas(){
                axios.get('http://127.0.0.1:8000/admi/escuelas/')
                    .then(response => {
                        this.escuelas = response.data;
                    })
                    .catch(error => {
                    console.error("Error al obtener las escuelas:", error);
                });
            },

            limpiarFormulario() {
                this.nombre = '';
                this.tipoConstancia = '';
                this.nivel = '';
                this.calificacion = null;
                this.escuelaSeleccionada = '';
                this.fechaActual = '';
            },

            actualizarNivel() {
                if (this.tipoConstancia === 1) {
                    this.nivel = 'B1';
                } else if (this.tipoConstancia === 2) {
                    this.nivel = 'A2';
                } else if (this.tipoConstancia === 3) {
                    this.nivel = 'A1';
                } else {
                    this.nivel = '';
                }
            },

        }
    }
</script>