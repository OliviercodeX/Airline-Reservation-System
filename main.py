import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import logic_app as la

# Ventana principal (variable global)
ventana_principal = None
#
def mostrar_mensaje_info(mensaje):
    messagebox.showinfo("Información", mensaje)

def mostrar_error(mensaje):
    messagebox.showerror("Error", mensaje)

def cerrar_ventana_secundaria(ventana):
    ventana.destroy()
    ventana_principal.deiconify()  # Muestra la ventana principal de nuevo

def obtener_lista_vuelos():
    return [f"Vuelo {i+1}" for i in range(len(la.flights))]

def obtener_numero_vuelo(texto_vuelo):
    if not texto_vuelo:
        return -1
    partes = texto_vuelo.split()
    try:
        return int(partes[-1]) - 1  # "Vuelo 1" -> 0
    except:
        return -1


# Conversiones y utilidades de asientos
def letra_a_indice(s):
    s = s.strip().upper()
    if not s or not s.isalpha():
        return -1
    val = 0
    for ch in s:
        val = val * 26 + (ord(ch) - 64)
    return val - 1


def indice_a_letra(idx):
    if idx < 0:
        return "?"
    s = ""
    n = idx + 1
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def crear_mapa_asientos(parent):
    """Crea un wrapper con Canvas y scrollbars, devuelve (wrapper, canvas)."""
    wrapper = tk.Frame(parent, bg="#0b0f14")
    canvas = tk.Canvas(wrapper, bg="#0b0f14", highlightthickness=0)
    vbar = tk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
    hbar = tk.Scrollbar(wrapper, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    vbar.grid(row=0, column=1, sticky="ns")
    hbar.grid(row=1, column=0, sticky="ew")
    wrapper.grid_rowconfigure(0, weight=1)
    wrapper.grid_columnconfigure(0, weight=1)

    return wrapper, canvas


def dibujar_mapa(canvas: tk.Canvas, matrix):
    canvas.delete("all")
    if not matrix:
        canvas.configure(scrollregion=(0, 0, 0, 0))
        return
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0

    cell_w = max(28, min(60, 900 // max(1, cols)))
    cell_h = max(28, min(60, 600 // max(1, rows)))
    left = 140
    top = 100

    # Silueta simple
    canvas.create_oval(20, 20, 120, 80, fill="#123", outline="")
    canvas.create_rectangle(80, 30, 120 + cols * cell_w + 80, 70, fill="#123", outline="")

    # Cabeceras de columnas
    for c in range(cols):
        canvas.create_text(left + c * cell_w + cell_w // 2, top - 18,
                           fill="#cbd5e1", font=("Arial", 10, "bold"), text=str(c + 1))

    y = top
    for r in range(rows):
        canvas.create_text(left - 20, y + cell_h // 2, fill="#cbd5e1",
                           font=("Arial", 10, "bold"), text=indice_a_letra(r))
        x = left
        for c in range(cols):
            state = matrix[r][c]
            fill = "#a51f2d" if state == 1 else "#1f6aa5"
            canvas.create_rectangle(x, y, x + cell_w - 6, y + cell_h - 6, outline="#0e141b", fill=fill)
            canvas.create_text(x + (cell_w // 2) - 4, y + (cell_h // 2) - 4,
                               fill="white", font=("Arial", 9), text=f"{indice_a_letra(r)}{c+1}")
            x += cell_w
        y += cell_h

    total_w = left + cols * cell_w + 60
    total_h = top + rows * cell_h + 40
    canvas.configure(scrollregion=(0, 0, total_w, total_h))


def crear_ventana_nuevo_vuelo():
    ventana_principal.withdraw()  # Oculta la ventana principal
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.title("Crear Nuevo Vuelo")
    ventana.geometry("500x300")
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_secundaria(ventana))  # Maneja el cierre con X
    
    # Marco para entrada de datos
    marco_entrada = ctk.CTkFrame(ventana)
    marco_entrada.pack(padx=20, pady=20)
    
    # Etiquetas y campos de entrada
    ctk.CTkLabel(marco_entrada, text="Filas:").grid(row=0, column=0, padx=5, pady=5)
    entrada_filas = ctk.CTkEntry(marco_entrada)
    entrada_filas.grid(row=0, column=1, padx=5, pady=5)
    
    ctk.CTkLabel(marco_entrada, text="Columnas:").grid(row=1, column=0, padx=5, pady=5)
    entrada_columnas = ctk.CTkEntry(marco_entrada)
    entrada_columnas.grid(row=1, column=1, padx=5, pady=5)
    
    def guardar_vuelo():
        try:
            filas = int(entrada_filas.get())
            columnas = int(entrada_columnas.get())
            
            if filas <= 0 or columnas <= 0:
                mostrar_error("Las filas y columnas deben ser números positivos")
                return
                
            respuesta = la.create_flight(filas, columnas)
            if isinstance(respuesta, str):
                mostrar_error(respuesta)
            else:
                mostrar_mensaje_info(f"Vuelo {len(la.flights)} creado exitosamente")
                ventana.destroy()
                ventana_principal.deiconify()  # Muestra la ventana principal
        except ValueError:
            mostrar_error("Por favor ingrese números válidos")
    
    # Botones
    marco_botones = ctk.CTkFrame(ventana)
    marco_botones.pack(pady=10)
    
    ctk.CTkButton(marco_botones, text="Crear Vuelo", command=guardar_vuelo).pack(side="left", padx=5)
    ctk.CTkButton(marco_botones, text="Volver", command=lambda: cerrar_ventana_secundaria(ventana)).pack(side="left", padx=5)

def crear_ventana_asignar_datos():
    ventana_principal.withdraw()  # Oculta la ventana principal
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.title("Asignar Datos del Vuelo")
    ventana.geometry("500x300")
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_secundaria(ventana))  # Maneja el cierre con X
    
    # Marco para entrada de datos
    marco_entrada = ctk.CTkFrame(ventana)
    marco_entrada.pack(padx=20, pady=20)
    
    # Selector de vuelo
    ctk.CTkLabel(marco_entrada, text="Seleccionar Vuelo:").grid(row=0, column=0, padx=5, pady=5)
    selector_vuelo = ctk.CTkComboBox(marco_entrada, values=obtener_lista_vuelos())
    selector_vuelo.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
    
    # Campos de datos
    ctk.CTkLabel(marco_entrada, text="Origen:").grid(row=1, column=0, padx=5, pady=5)
    entrada_origen = ctk.CTkEntry(marco_entrada)
    entrada_origen.grid(row=1, column=1, padx=5, pady=5)
    
    ctk.CTkLabel(marco_entrada, text="Destino:").grid(row=2, column=0, padx=5, pady=5)
    entrada_destino = ctk.CTkEntry(marco_entrada)
    entrada_destino.grid(row=2, column=1, padx=5, pady=5)
    
    ctk.CTkLabel(marco_entrada, text="Precio:").grid(row=3, column=0, padx=5, pady=5)
    entrada_precio = ctk.CTkEntry(marco_entrada)
    entrada_precio.grid(row=3, column=1, padx=5, pady=5)

    # Nuevo campo para código (ahora manual)
    ctk.CTkLabel(marco_entrada, text="Código (manual):").grid(row=4, column=0, padx=5, pady=5)
    entrada_codigo = ctk.CTkEntry(marco_entrada)
    entrada_codigo.grid(row=4, column=1, padx=5, pady=5)
    
    def guardar_datos():
        numero_vuelo = obtener_numero_vuelo(selector_vuelo.get())
        if numero_vuelo < 0:
            mostrar_error("Seleccione un vuelo válido")
            return
            
        try:
            precio = float(entrada_precio.get())
            if precio < 0:
                mostrar_error("El precio debe ser positivo")
                return
        except ValueError:
            mostrar_error("Ingrese un precio válido")
            return
            
        origen = entrada_origen.get().strip()
        destino = entrada_destino.get().strip()
        codigo_manual = entrada_codigo.get().strip()

        if not origen or not destino or not codigo_manual:
            mostrar_error("Origen, destino y código son requeridos")
            return

        # Verificar que el código no exista ya
        existencia = any(f[0] and f[0].upper() == codigo_manual.upper() and i != numero_vuelo for i, f in enumerate(la.flights))
        if existencia:
            mostrar_error("El código ya existe para otro vuelo. Elija otro código.")
            return

        # Llamamos a la lógica para asignar datos (ahora requiere código manual)
        respuesta = la.assign_flight(origen, destino, precio, numero_vuelo, codigo_manual)
        if isinstance(respuesta, str) and respuesta:
            mostrar_error(respuesta)
            return

        mostrar_mensaje_info("Datos asignados correctamente")
        ventana.destroy()
        ventana_principal.deiconify()  # Muestra la ventana principal
    
    # Botones
    marco_botones = ctk.CTkFrame(ventana)
    marco_botones.pack(pady=10)
    
    ctk.CTkButton(marco_botones, text="Guardar", command=guardar_datos).pack(side="left", padx=5)
    ctk.CTkButton(marco_botones, text="Volver", command=lambda: cerrar_ventana_secundaria(ventana)).pack(side="left", padx=5)

def crear_ventana_reservas():
    ventana_principal.withdraw()
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.title("Reservas")
    ventana.geometry("800x600")
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_secundaria(ventana))

    top = ctk.CTkFrame(ventana); top.pack(fill="x", padx=10, pady=8)
    ctk.CTkLabel(top, text="Vuelo:").pack(side="left")
    cb_f = ctk.CTkComboBox(top, values=obtener_lista_vuelos(), width=160); cb_f.pack(side="left", padx=6)
    ctk.CTkButton(top, text="Refresh", command=lambda: (cb_f.configure(values=obtener_lista_vuelos()), draw_map())).pack(side="left", padx=6)

    ent_row = ctk.CTkEntry(top, placeholder_text="Fila (A, B, AA)", width=140); ent_row.pack(side="left", padx=6)
    ent_col = ctk.CTkEntry(top, placeholder_text="Columna (1..)", width=140); ent_col.pack(side="left", padx=6)

    wrapper, canvas = crear_mapa_asientos(ventana)
    wrapper.pack(fill="both", expand=True, padx=10, pady=10)

    def draw_map():
        idx = obtener_numero_vuelo(cb_f.get())
        matrix = la.flights[idx][4] if 0 <= idx < len(la.flights) else []
        dibujar_mapa(canvas, matrix)

    def hacer_reserva():
        idx = obtener_numero_vuelo(cb_f.get())
        if idx < 0:
            mostrar_error("Seleccione un vuelo válido")
            return
        r = letra_a_indice(ent_row.get())
        try:
            c = int(ent_col.get()) - 1
        except ValueError:
            mostrar_error("Ingrese una columna válida")
            return
        resp = la.book_flight(r, c, idx)
        if isinstance(resp, str) and resp:
            (mostrar_mensaje_info if "reservado" in resp.lower() else mostrar_error)(resp)
        draw_map()

    def cancelar_reserva():
        idx = obtener_numero_vuelo(cb_f.get())
        if idx < 0:
            mostrar_error("Seleccione un vuelo válido")
            return
        r = letra_a_indice(ent_row.get())
        try:
            c = int(ent_col.get()) - 1
        except ValueError:
            mostrar_error("Ingrese una columna válida")
            return
        la.cancel_flight(r, c, idx)
        mostrar_mensaje_info("Cancelación procesada (si estaba ocupada)")
        draw_map()

    botones = ctk.CTkFrame(ventana); botones.pack(fill="x", padx=10, pady=(0, 10))
    ctk.CTkButton(botones, text="Reservar", command=hacer_reserva).pack(side="left", padx=6)
    ctk.CTkButton(botones, text="Cancelar", command=cancelar_reserva).pack(side="left", padx=6)
    ctk.CTkButton(botones, text="Volver", command=lambda: cerrar_ventana_secundaria(ventana)).pack(side="right", padx=6)

    draw_map()

    return ventana


def crear_ventana_estado_vuelo():
    ventana_principal.withdraw()
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.title("Estado del Vuelo")
    ventana.geometry("800x600")
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_secundaria(ventana))

    top = ctk.CTkFrame(ventana); top.pack(fill="x", padx=10, pady=8)
    ctk.CTkLabel(top, text="Vuelo:").pack(side="left")
    cb_f = ctk.CTkComboBox(top, values=obtener_lista_vuelos(), width=160); cb_f.pack(side="left", padx=6)

    stats_lbl = ctk.CTkLabel(top, text="")
    stats_lbl.pack(side="left", padx=16)
    ctk.CTkButton(top, text="Refresh", command=lambda: (cb_f.configure(values=obtener_lista_vuelos()), draw_map())).pack(side="left", padx=6)
    ctk.CTkButton(top, text="Volver", command=lambda: cerrar_ventana_secundaria(ventana)).pack(side="right", padx=6)

    wrapper, canvas = crear_mapa_asientos(ventana)
    wrapper.pack(fill="both", expand=True, padx=10, pady=10)

    def draw_map():
        idx = obtener_numero_vuelo(cb_f.get())
        if 0 <= idx < len(la.flights):
            flight = la.flights[idx]
            matrix = flight[4]
            rows = len(matrix); cols = len(matrix[0]) if rows else 0
            total = rows * cols
            taken = la.ticket_sold(matrix)
            pct = (taken / total * 100) if total else 0
            stats_lbl.configure(text=f"Total: {total} | Ocupadas: {taken} | Ocupación: {pct:.2f}%")
            dibujar_mapa(canvas, matrix)
        else:
            stats_lbl.configure(text="")
            dibujar_mapa(canvas, [])

    draw_map()

    return ventana


def crear_ventana_estadisticas():
    ventana_principal.withdraw()
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.title("Estadísticas")
    ventana.geometry("700x600")
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_secundaria(ventana))

    row = ctk.CTkFrame(ventana); row.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(row, text="Vuelo:").pack(side="left")
    cb_f = ctk.CTkComboBox(row, values=obtener_lista_vuelos(), width=160); cb_f.pack(side="left", padx=6)
    ctk.CTkButton(row, text="Refresh", command=lambda: cb_f.configure(values=obtener_lista_vuelos())).pack(side="left", padx=6)

    out = ctk.CTkTextbox(ventana, height=420); out.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_ocupacion():
        idx = obtener_numero_vuelo(cb_f.get())
        out.delete("1.0", "end")
        if not (0 <= idx < len(la.flights)):
            out.insert("end", "Seleccione un vuelo válido.\n")
            return
        code, origin, dest, price, matrix, *_ = la.flights[idx]
        rows = len(matrix); cols = len(matrix[0]) if rows else 0
        total = rows * cols
        taken = la.ticket_sold(matrix)
        pct = (taken / total * 100) if total else 0
        out.insert("end", f"Vuelo {idx+1} - {code or 'NO_CODE'} {origin or '?'} → {dest or '?'}\n")
        out.insert("end", f"Total asientos: {total}\n")
        out.insert("end", f"Ocupadas: {taken}\n")
        out.insert("end", f"Ocupación: {pct:.2f}%\n")

    def mostrar_recaudacion():
        idx = obtener_numero_vuelo(cb_f.get())
        out.delete("1.0", "end")
        if not (0 <= idx < len(la.flights)):
            out.insert("end", "Seleccione un vuelo válido.\n")
            return
        code, origin, dest, price, matrix, *_ = la.flights[idx]
        tickets = la.ticket_sold(matrix)
        total_collected = tickets * (price or 0)
        out.insert("end", f"Vuelo {idx+1} - {code or 'NO_CODE'} {origin or '?'} → {dest or '?'}\n")
        out.insert("end", f"Tickets vendidos: {tickets}\n")
        out.insert("end", f"Precio por ticket: {price}\n")
        out.insert("end", f"Recaudación total: {total_collected}\n")

    btns = ctk.CTkFrame(ventana); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Ocupación", command=mostrar_ocupacion).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Recaudación", command=mostrar_recaudacion).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Volver", command=lambda: cerrar_ventana_secundaria(ventana)).pack(side="left", padx=6)

    return ventana


def crear_ventana_buscar_vuelos():
    ventana_principal.withdraw()
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.title("Buscar Vuelos")
    ventana.geometry("700x600")
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_secundaria(ventana))

    row = ctk.CTkFrame(ventana); row.pack(fill="x", padx=10, pady=10)
    ent_dest = ctk.CTkEntry(row, placeholder_text="Destino (e.g., Bogota)"); ent_dest.pack(side="left", padx=6)

    out = ctk.CTkTextbox(ventana, height=420); out.pack(fill="both", expand=True, padx=10, pady=10)

    def hacer_busqueda():
        d = ent_dest.get().strip()
        out.delete("1.0", "end")
        if not d:
            out.insert("end", "Ingrese un destino.\n")
            return
        result = la.search_flights_by_destination(d)
        out.insert("end", f"Destino: {d}\n\n")
        if not result:
            out.insert("end", "No se encontraron vuelos.\n")
            return
        out.insert("end", f'Vuelos a "{d}":\n')
        for (num, seats_free) in result:
            out.insert("end", f"- Vuelo {num} (asientos libres: {seats_free})\n")

    btns = ctk.CTkFrame(ventana); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Buscar", command=hacer_busqueda).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Volver", command=lambda: cerrar_ventana_secundaria(ventana)).pack(side="left", padx=6)

    return ventana


def crear_ventana_consecutivo():
    ventana_principal.withdraw()
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.title("Reserva Consecutiva")
    ventana.geometry("700x200")
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_secundaria(ventana))

    row = ctk.CTkFrame(ventana); row.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(row, text="Vuelo:").pack(side="left")
    cb_f = ctk.CTkComboBox(row, values=obtener_lista_vuelos(), width=160); cb_f.pack(side="left", padx=6)
    ent_row = ctk.CTkEntry(row, placeholder_text="Fila (A, B, AA)", width=130); ent_row.pack(side="left", padx=6)
    ent_start = ctk.CTkEntry(row, placeholder_text="Columna inicio", width=110); ent_start.pack(side="left", padx=6)
    ent_amount = ctk.CTkEntry(row, placeholder_text="Cantidad", width=90); ent_amount.pack(side="left", padx=6)

    def ejecutar():
        idx = obtener_numero_vuelo(cb_f.get())
        if idx < 0:
            mostrar_error("Seleccione un vuelo válido")
            return
        r = letra_a_indice(ent_row.get())
        try:
            start = int(ent_start.get()) - 1
            amount = int(ent_amount.get())
        except ValueError:
            mostrar_error("Ingrese números válidos para inicio/cantidad")
            return
        resp = la.book_consutive_seats(idx, r, start, amount)
        if isinstance(resp, str) and resp:
            if "exitosamente" in resp.lower():
                seat_list = [f"{indice_a_letra(r)}{i+1}" for i in range(start, start + amount)]
                mostrar_mensaje_info("Reservados: " + " ".join(seat_list))
            else:
                mostrar_error(resp)
        else:
            mostrar_mensaje_info("Operación finalizada.")

    btns = ctk.CTkFrame(ventana); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Reservar", command=ejecutar).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Refresh vuelos", command=lambda: cb_f.configure(values=obtener_lista_vuelos())).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Volver", command=lambda: cerrar_ventana_secundaria(ventana)).pack(side="left", padx=6)

    return ventana


def crear_ventana_venta_masiva():
    ventana_principal.withdraw()
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.title("Venta Masiva")
    ventana.geometry("500x200")
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_secundaria(ventana))

    row = ctk.CTkFrame(ventana); row.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(row, text="Porcentaje (1-100):").pack(side="left")
    ent_pct = ctk.CTkEntry(row, width=120); ent_pct.pack(side="left", padx=6)

    def ejecutar():
        try:
            pct = int(ent_pct.get())
        except ValueError:
            mostrar_error("Ingrese un porcentaje entero")
            return
        if pct < 1 or pct > 100:
            mostrar_error("Porcentaje debe ser 1..100")
            return
        resp = la.simulate_mass_booking(la.flights, pct)
        mostrar_mensaje_info(resp if isinstance(resp, str) and resp else "Venta masiva completada")

    btns = ctk.CTkFrame(ventana); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Ejecutar", command=ejecutar).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Volver", command=lambda: cerrar_ventana_secundaria(ventana)).pack(side="left", padx=6)

    return ventana


def crear_ventana_reset_vuelo():
    ventana_principal.withdraw()
    ventana = ctk.CTkToplevel(ventana_principal)
    ventana.title("Reset Vuelo")
    ventana.geometry("600x200")
    ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_secundaria(ventana))

    row = ctk.CTkFrame(ventana); row.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(row, text="Vuelo:").pack(side="left")
    cb_f = ctk.CTkComboBox(row, values=obtener_lista_vuelos(), width=160); cb_f.pack(side="left", padx=6)
    ctk.CTkButton(row, text="Refresh", command=lambda: cb_f.configure(values=obtener_lista_vuelos())).pack(side="left", padx=6)

    def ejecutar():
        idx = obtener_numero_vuelo(cb_f.get())
        if not (0 <= idx < len(la.flights)):
            mostrar_error("Seleccione un vuelo válido")
            return
        matrix = la.flights[idx][4]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = 0
        la.flights[idx][5] = 0
        mostrar_mensaje_info("Vuelo reseteado")

    btns = ctk.CTkFrame(ventana); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Reset", command=ejecutar).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Volver", command=lambda: cerrar_ventana_secundaria(ventana)).pack(side="left", padx=6)

    return ventana

def ventana_principal():
    global ventana_principal
    ventana_principal = ctk.CTk()
    ventana_principal.title("Sistema de Reservas Aéreas")
    ventana_principal.geometry("800x600")
    
    # Configuración de tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Título
    titulo = ctk.CTkLabel(ventana_principal, 
                         text="Sistema de Reservas Aéreas",
                         font=("Arial", 24, "bold"))
    titulo.pack(pady=20)
    
    # Marco para botones
    marco_botones = ctk.CTkFrame(ventana_principal)
    marco_botones.pack(pady=10)
    
    # Lista de botones y sus funciones (más completa, reflejando main.py)
    botones = [
        ("Crear Nuevo Vuelo", crear_ventana_nuevo_vuelo),
        ("Asignar Datos", crear_ventana_asignar_datos),
        ("Reservas", crear_ventana_reservas),
        ("Estado Vuelo", crear_ventana_estado_vuelo),
        ("Estadísticas", crear_ventana_estadisticas),
        ("Buscar Vuelos", crear_ventana_buscar_vuelos),
        ("Reserva Consecutiva", crear_ventana_consecutivo),
        ("Venta Masiva", crear_ventana_venta_masiva),
        ("Reset Vuelo", crear_ventana_reset_vuelo),
        ("Salir", ventana_principal.destroy)
    ]
    
    # Crear botones en grid 2x2
    for i, (texto, funcion) in enumerate(botones):
        boton = ctk.CTkButton(marco_botones, 
                             text=texto,
                             width=200,
                             command=funcion)
        boton.grid(row=i//2, column=i%2, padx=10, pady=5)
    
    ventana_principal.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    ventana_principal()
