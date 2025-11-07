# EL AJA — Asistente Académico Universitario

**EL AJA** es una aplicación web desarrollada con **Flet** y conectada a **Firebase**, diseñada para mejorar la comunicación académica entre estudiantes y docentes.  
Ofrece un **chatbot académico**, un **foro interactivo**, un **registro de horario personalizado** y una **interfaz adaptable** moderna y responsiva.

---

## Despliegue del Proyecto

### 🔹 Plataforma de Liberación
El proyecto fue desplegado en **Render** (https://render.com), utilizando la versión más reciente del código alojado en GitHub, esto para la simulación de liberación del proyecto.

### 🔹 Repositorio del Proyecto
**GitHub:** [https://github.com/jjuanita/el_aja](https://github.com/jjuanita/el_aja)

### 🔹 Video de Demostración
**Demostración funcional:** [https://drive.google.com/file/d/1gQutJ9LUa9tkJxDulLWu1nD8w4HJV33W/view?usp=drive_link] 

---

##  Instalación y Ejecución Local

```bash
git clone https://github.com/jjuanita/el_aja.git
cd el_aja
python -m venv venv
venv\Scripts\activate   # En Windows
pip install -r requirements.txt
flet run main.py
````
## Monitoreo con UptimeRobot
Para garantizar la disponibilidad del sistema después de su despliegue, se configuró un monitoreo mediante UptimeRobot, una herramienta gratuita que permite verificar el estado y tiempo de respuesta de aplicaciones web.
Se creó un monitor tipo HTTP(s) con la URL del proyecto desplegado en Render, comprobando periódicamente que el servicio se encuentra activo.

El resultado mostró el estado “UP”, indicando que la aplicación responde correctamente y mantiene una buena disponibilidad en línea.
Este monitoreo básico permite detectar posibles caídas del sistema y asegurar una respuesta rápida ante fallos.

