# 🛫 Proyecto I – Sistema de Reservas de Vuelos  
**Curso:** Introducción a la Programación  
**Institución:** Instituto Tecnológico de Costa Rica (ITCR)  
**Autor:** Mainor Olivier Martínez Sánchez  
**Carné:** 2025094482   
**Edad:** 18 años  

---

## 📘 Descripción del proyecto  
El **Sistema de Reservas de Vuelos** es un programa desarrollado en **Python** con interfaz gráfica construida con **CustomTkinter**, que simula el funcionamiento de un sistema de reservas de asientos para vuelos comerciales.  

Permite crear vuelos, asignar su origen, destino y precio, así como visualizar y administrar los asientos disponibles y reservados. Todo se gestiona en memoria utilizando **listas y matrices**, cumpliendo con los lineamientos del curso.

---

## 🎯 Objetivos  
- Aplicar los conceptos de programación estructurada.  
- Practicar el uso de **funciones, listas y matrices** en Python.  
- Implementar una **interfaz gráfica completa** para la interacción con el usuario.  
- Validar entradas, controlar errores y generar reportes visuales del estado de los vuelos.  

---

## 🧠 Estructura de datos utilizada  
Cada vuelo se representa como una lista con la siguiente estructura:

```python
["Código de vuelo", "Origen", "Destino", precio_boleto, matriz_asientos, cantidad_vendidos]
```

Ejemplo:
```python
["CM123", "San José", "México", 350, [[0,1,0],[0,0,0]], 15]
```

> La variable global `flights` contiene todos los vuelos creados:
> ```python
> flights = [vuelo1, vuelo2, vuelo3, ...]
> ```

---

## 🧩 Funcionalidades principales  

### 1️⃣ Crear nuevo vuelo  
Permite definir la cantidad de filas y columnas del avión.  
Valida los valores máximos (50 filas y 20 columnas).

### 2️⃣ Asignar datos del vuelo  
Asigna **origen, destino, precio y código** de vuelo.  
Evita duplicados y valida tipos de datos.

### 3️⃣ Ver estado del vuelo  
Muestra gráficamente los asientos del avión (ocupados en rojo, libres en azul).

### 4️⃣ Reservar y cancelar asiento  
Permite seleccionar un asiento por su **letra (fila)** y **número (columna)**.  
Incluye validaciones de rango y estado del asiento.

### 5️⃣ Estadísticas  
Muestra ocupación total, boletos vendidos y total recaudado.

### 6️⃣ Búsqueda de vuelos  
Permite buscar vuelos disponibles por **destino**.

### 7️⃣ Reserva consecutiva  
Reserva una cantidad específica de asientos seguidos en una fila.

### 8️⃣ Venta masiva  
Simula la ocupación de asientos según un porcentaje ingresado (1–100%).

### 9️⃣ Reiniciar vuelo  
Libera todos los asientos de un vuelo y reinicia las estadísticas.

---

## 🧰 Requisitos del sistema  
- Python 3.10 o superior  
- Librerías requeridas:

```txt
customtkinter==5.2.2
pillow==12.0.0
```

---

## ⚙️ Instalación y ejecución  
1. Clonar o descargar el proyecto.  
2. Instalar dependencias con:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el programa con:
   ```bash
   python main.py
   ```

---

## 🖼️ Interfaz gráfica  
El proyecto utiliza **CustomTkinter** para una apariencia moderna.  
- Los asientos se representan en un **canvas interactivo**.  
- Los botones permiten navegar entre las secciones del sistema.  
- Los mensajes de error y éxito se muestran mediante cuadros de diálogo (`messagebox`).

---

## 🧪 Validaciones incluidas  
- Verificación de tipos de datos (numéricos, texto).  
- Control de rangos (filas, columnas, porcentaje).  
- Restricción de creación y reserva sin datos asignados.  
- Prevención de códigos de vuelo repetidos.  
- Evita reservas dobles o cancelaciones inválidas.

---

## 📁 Estructura del proyecto  

```
Proyecto_Reservas_Vuelos/
│
├── main.py                 # Interfaz gráfica (CustomTkinter)
├── logic_app.py            # Lógica original del proyecto
├── requirements.txt        # Dependencias mínimas del proyecto
├── ProyectoI_ReservasDeVuelos.pdf  # Enunciado oficial del TEC
└── README.md               # Este archivo
```

---

## 📚 Aprendizajes aplicados  
- Programación estructurada  
- Manejo de listas y matrices  
- Separación de lógica y presentación (backend y GUI)  
- Validaciones y manejo de errores  
- Uso de librerías gráficas en Python  

---

## 🏁 Conclusión  
Este proyecto demuestra la aplicación de los fundamentos de programación en la creación de un sistema funcional, validado y con interfaz gráfica completa.  

Fue desarrollado como parte del **Proyecto Programado I** del curso **Introducción a la Programación** del **Instituto Tecnológico de Costa Rica**, cumpliendo los requerimientos establecidos.

---

**© 2025 – Mainor Olivier Martínez Sánchez**  
*Estudiante de Ingeniería en Computación, ITCR*  

---

💡 *Nota:* Aunque no fue requerido en la entrega formal, este README se incluye como documentación técnica del proyecto, con el fin de mantener buenas prácticas y facilitar su comprensión y mantenimiento futuro.
