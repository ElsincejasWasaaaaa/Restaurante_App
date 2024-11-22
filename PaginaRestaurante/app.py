import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from utils.menu_data import menu_data
from utils.reservaciones import init_reservaciones_file, guardar_reservacion, obtener_reservaciones

# Configuración de la página
st.set_page_config(
    page_title="Restaurante El Gourmet",
    page_icon="🍽️",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
    }
    h1, h2, h3 {
        color: #2C3E50;
    }
    .dish-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        color: #2C3E50; /* Cambia el texto a un color visible */
    }
    .dish-card h3 {
        color: #34495E; /* Color más oscuro para los títulos */
    }
    .dish-card p {
        color: #2C3E50; /* Color visible para el texto descriptivo */
    }
    .reservation-table {
        margin-top: 1rem;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


def show_home():
    st.header("Bienvenidos a El Gourmet")
    st.write("""
    Descubra una experiencia culinaria única donde la tradición se encuentra con la innovación.
    Nuestro chef ejecutivo y su equipo crean platos excepcionales utilizando los ingredientes
    más frescos y técnicas culinarias de clase mundial.
    """)
    
    st.subheader("Horario")
    st.write("""
    - Lunes a Jueves: 12:00 - 22:00
    - Viernes y Sábado: 12:00 - 23:00
    - Domingo: 12:00 - 21:00
    """)

    st.subheader("Ubicación")
    st.write("Av. Gastronómica 123, Ciudad Gourmet")

def show_menu():
    st.header("Nuestro Menú")
    
    for categoria, platos in menu_data.items():
        st.subheader(categoria)
        cols = st.columns(2)
        for idx, (nombre, detalles) in enumerate(platos.items()):
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"""
                    <div class="dish-card">
                        <h3>{nombre}</h3>
                        <p><strong>Precio:</strong> {detalles['precio']}</p>
                        <p><strong>Descripción:</strong> {detalles['descripcion']}</p>
                        <p><strong>Ingredientes:</strong> {detalles['ingredientes']}</p>
                    </div>
                    """, unsafe_allow_html=True)

def show_reservations():
    st.header("Reserva tu Mesa")
    
    tabs = st.tabs(["Hacer Reservación", "Ver Reservaciones"])
    
    with tabs[0]:
        with st.form("reservation_form"):
            nombre = st.text_input("Nombre completo")
            email = st.text_input("Email")
            telefono = st.text_input("Teléfono")
            
            fecha = st.date_input(
                "Fecha de reservación",
                min_value=datetime.today(),
                max_value=datetime.today() + timedelta(days=30)
            )
            
            hora = st.selectbox(
                "Hora de reservación",
                ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
            )
            
            personas = st.slider("Número de personas", 1, 10, 2)
            comentarios = st.text_area("Comentarios adicionales")
            
            submitted = st.form_submit_button("Realizar Reservación")
            
            if submitted:
                if nombre and email and telefono:
                    if guardar_reservacion(fecha, hora, nombre, email, telefono, personas, comentarios):
                        st.success(f"¡Gracias por tu reservación, {nombre}! Te hemos enviado un correo de confirmación.")
                        st.balloons()
                else:
                    st.error("Por favor, completa todos los campos requeridos.")
    
    with tabs[1]:
        st.subheader("Reservaciones Actuales")
        # Agregar un campo de contraseña para ver las reservaciones
        password = st.text_input("Ingrese la contraseña de administrador", type="password")
        if password == "admin123":  # En un entorno real, usar un sistema de autenticación seguro
            reservaciones = obtener_reservaciones()
            if not reservaciones.empty:
                st.dataframe(
                    reservaciones,
                    column_config={
                        "fecha": "Fecha",
                        "hora": "Hora",
                        "nombre": "Nombre",
                        "email": "Email",
                        "telefono": "Teléfono",
                        "personas": "Personas",
                        "comentarios": "Comentarios"
                    },
                    hide_index=True
                )
            else:
                st.info("No hay reservaciones registradas.")
        elif password:
            st.error("Contraseña incorrecta")

def main():
    # Inicializar archivo de reservaciones
    init_reservaciones_file()
    
    # Header
    st.title("🍽️ Restaurante El Gourmet")
    st.markdown("---")

    # Menú de navegación
    menu = ["Inicio", "Menú", "Reservaciones"]
    choice = st.sidebar.selectbox("Navegación", menu)

    if choice == "Inicio":
        show_home()
    elif choice == "Menú":
        show_menu()
    else:
        show_reservations()

if __name__ == "__main__":
    main()