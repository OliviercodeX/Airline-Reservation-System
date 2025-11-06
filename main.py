import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

import logic_app as la

# ==========================
# Global app state (procedural, no OOP)
# ==========================
root = None

# ==========================
# Helpers (procedural)
# ==========================

def letter_to_index(s: str) -> int:
    s = s.strip().upper()
    if not s or not s.isalpha():
        return -1
    val = 0
    for ch in s:
        val = val * 26 + (ord(ch) - 64)
    return val - 1


def index_to_letter(idx: int) -> str:
    if idx < 0:
        return "?"
    s = ""
    n = idx + 1
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def show_info(msg: str):
    messagebox.showinfo("Info", msg)


def show_error(msg: str):
    messagebox.showerror("Error", msg)


def flight_items():
    return [f"Flight {i+1}" for i in range(len(la.flights))]


def parse_flight_index(s: str) -> int:
    if not s:
        return -1
    parts = s.split()
    try:
        return int(parts[-1]) - 1
    except Exception:
        return -1

# ==========================
# Seat map (Canvas with scrollbars) – procedural
# ==========================

def create_seatmap(parent):
    wrapper = tk.Frame(parent)
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


def draw_seatmap(canvas: tk.Canvas, matrix):
    canvas.delete("all")
    if not matrix:
        canvas.configure(scrollregion=(0, 0, 0, 0))
        return
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0

    # Layout constants
    cell_w = max(28, min(60, 900 // max(1, cols)))
    cell_h = max(28, min(60, 600 // max(1, rows)))
    left = 140
    top = 100

    # Simple airplane silhouette
    canvas.create_oval(20, 20, 120, 80, fill="#123", outline="")
    canvas.create_rectangle(80, 30, 120 + cols * cell_w + 80, 70, fill="#123", outline="")

    # Column headers
    for c in range(cols):
        canvas.create_text(left + c * cell_w + cell_w // 2, top - 18,
                           fill="#cbd5e1", font=("Arial", 10, "bold"), text=str(c + 1))

    # Seats
    y = top
    for r in range(rows):
        canvas.create_text(left - 20, y + cell_h // 2, fill="#cbd5e1",
                           font=("Arial", 10, "bold"), text=index_to_letter(r))
        x = left
        for c in range(cols):
            state = matrix[r][c]
            fill = "#a51f2d" if state == 1 else "#1f6aa5"
            canvas.create_rectangle(x, y, x + cell_w - 6, y + cell_h - 6, outline="#0e141b", fill=fill)
            canvas.create_text(x + (cell_w // 2) - 4, y + (cell_h // 2) - 4,
                               fill="white", font=("Arial", 9), text=f"{index_to_letter(r)}{c+1}")
            x += cell_w
        y += cell_h

    total_w = left + cols * cell_w + 60
    total_h = top + rows * cell_h + 40
    canvas.configure(scrollregion=(0, 0, total_w, total_h))

# ==========================
# Toplevel windows (procedural)
# ==========================

def back_to_main(win):
    if win is not None and win.winfo_exists():
        win.destroy()
    if root is not None and root.state() == 'withdrawn':
        root.deiconify()


def open_create_flight():
    win = ctk.CTkToplevel(root)
    win.title("Create Flight")
    win.geometry("480x240")

    row1 = ctk.CTkFrame(win); row1.pack(padx=12, pady=12, fill="x")
    ctk.CTkLabel(row1, text="Rows:").pack(side="left")
    ent_rows = ctk.CTkEntry(row1, width=100); ent_rows.pack(side="left", padx=6)
    ctk.CTkLabel(row1, text="Columns:").pack(side="left")
    ent_cols = ctk.CTkEntry(row1, width=100); ent_cols.pack(side="left", padx=6)

    msg = ctk.CTkLabel(win, text=""); msg.pack(pady=(0, 8))

    def do_create():
        try:
            r = int(ent_rows.get()); c = int(ent_cols.get())
        except ValueError:
            show_error("Enter integers for rows/columns.")
            return
        resp = la.create_flight(r, c)
        if isinstance(resp, str) and resp:
            show_error(resp)
        else:
            msg.configure(text=f"Flight {len(la.flights)} created successfully.")

    btns = ctk.CTkFrame(win); btns.pack(pady=8)
    ctk.CTkButton(btns, text="Create", command=do_create, width=120).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Back", command=lambda: back_to_main(win), width=120).pack(side="left", padx=6)


def open_assign_data():
    win = ctk.CTkToplevel(root)
    win.title("Assign Data")
    win.geometry("560x260")

    row1 = ctk.CTkFrame(win); row1.pack(padx=12, pady=8, fill="x")
    ctk.CTkLabel(row1, text="Flight:").pack(side="left")
    cb_f = ctk.CTkComboBox(row1, values=flight_items(), width=160); cb_f.pack(side="left", padx=6)
    ctk.CTkButton(row1, text="Refresh", command=lambda: cb_f.configure(values=flight_items())).pack(side="left", padx=6)

    row2 = ctk.CTkFrame(win); row2.pack(padx=12, pady=8, fill="x")
    ent_origin = ctk.CTkEntry(row2, placeholder_text="Origin"); ent_origin.pack(side="left", padx=6)
    ent_dest = ctk.CTkEntry(row2, placeholder_text="Destination"); ent_dest.pack(side="left", padx=6)
    ent_price = ctk.CTkEntry(row2, placeholder_text="Price"); ent_price.pack(side="left", padx=6)

    def do_assign():
        idx = parse_flight_index(cb_f.get())
        if idx < 0:
            show_error("Select a valid flight.")
            return
        try:
            price = float(ent_price.get())
        except ValueError:
            show_error("Enter a valid price.")
            return
        resp = la.assign_flight(ent_origin.get().strip(), ent_dest.get().strip(), price, idx)
        if isinstance(resp, str) and resp:
            show_error(resp)
        else:
            show_info("Data assigned correctly.")

    btns = ctk.CTkFrame(win); btns.pack(pady=8)
    ctk.CTkButton(btns, text="Assign", command=do_assign, width=120).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Back", command=lambda: back_to_main(win), width=120).pack(side="left", padx=6)


def open_reservations():
    win = ctk.CTkToplevel(root)
    win.title("Reservations")
    win.geometry("1000x680")

    top = ctk.CTkFrame(win); top.pack(fill="x", padx=10, pady=8)
    ctk.CTkLabel(top, text="Flight:").pack(side="left")
    cb_f = ctk.CTkComboBox(top, values=flight_items(), width=160); cb_f.pack(side="left", padx=6)
    ctk.CTkButton(top, text="Refresh", command=lambda: cb_f.configure(values=flight_items())).pack(side="left", padx=6)

    ent_row = ctk.CTkEntry(top, placeholder_text="Row (A, B, AA)", width=140); ent_row.pack(side="left", padx=6)
    ent_col = ctk.CTkEntry(top, placeholder_text="Column (1..)", width=140); ent_col.pack(side="left", padx=6)

    def draw_map():
        idx = parse_flight_index(cb_f.get())
        matrix = la.flights[idx][4] if 0 <= idx < len(la.flights) else []
        draw_seatmap(canvas, matrix)

    def do_book():
        idx = parse_flight_index(cb_f.get())
        if idx < 0:
            show_error("Select a valid flight.")
            return
        r = letter_to_index(ent_row.get())
        try:
            c = int(ent_col.get()) - 1
        except ValueError:
            show_error("Enter a valid column number.")
            return
        resp = la.book_flight(r, c, idx)
        if isinstance(resp, str) and resp:
            (show_info if "reservado" in resp.lower() else show_error)(resp)
        draw_map()

    def do_cancel():
        idx = parse_flight_index(cb_f.get())
        if idx < 0:
            show_error("Select a valid flight.")
            return
        r = letter_to_index(ent_row.get())
        try:
            c = int(ent_col.get()) - 1
        except ValueError:
            show_error("Enter a valid column number.")
            return
        la.cancel_flight(r, c, idx)
        show_info("Seat cancellation processed (if it was occupied).")
        draw_map()

    ctk.CTkButton(top, text="Book", command=do_book).pack(side="left", padx=6)
    ctk.CTkButton(top, text="Cancel", command=do_cancel).pack(side="left", padx=6)
    ctk.CTkButton(top, text="Back", command=lambda: back_to_main(win)).pack(side="right", padx=6)

    wrapper, canvas = create_seatmap(win)
    wrapper.pack(fill="both", expand=True, padx=10, pady=10)
    draw_map()


def open_status():
    win = ctk.CTkToplevel(root)
    win.title("Flight Status")
    win.geometry("1000x680")

    top = ctk.CTkFrame(win); top.pack(fill="x", padx=10, pady=8)
    ctk.CTkLabel(top, text="Flight:").pack(side="left")
    cb_f = ctk.CTkComboBox(top, values=flight_items(), width=160); cb_f.pack(side="left", padx=6)
    ctk.CTkButton(top, text="Refresh", command=lambda: (cb_f.configure(values=flight_items()), draw_map())).pack(side="left", padx=6)

    stats_lbl = ctk.CTkLabel(top, text=""); stats_lbl.pack(side="left", padx=16)
    ctk.CTkButton(top, text="Back", command=lambda: back_to_main(win)).pack(side="right", padx=6)

    wrapper, canvas = create_seatmap(win)
    wrapper.pack(fill="both", expand=True, padx=10, pady=10)

    def draw_map():
        idx = parse_flight_index(cb_f.get())
        if 0 <= idx < len(la.flights):
            flight = la.flights[idx]
            matrix = flight[4]
            rows = len(matrix); cols = len(matrix[0]) if rows else 0
            total = rows * cols
            taken = la.ticket_sold(matrix)
            pct = (taken / total * 100) if total else 0
            stats_lbl.configure(text=f"Total seats: {total} | Taken: {taken} | Occupancy: {pct:.2f}%")
            draw_seatmap(canvas, matrix)
        else:
            stats_lbl.configure(text="")
            draw_seatmap(canvas, [])

    draw_map()


def open_statistics():
    win = ctk.CTkToplevel(root)
    win.title("Statistics")
    win.geometry("620x340")

    row = ctk.CTkFrame(win); row.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(row, text="Flight:").pack(side="left")
    cb_f = ctk.CTkComboBox(row, values=flight_items(), width=160); cb_f.pack(side="left", padx=6)
    ctk.CTkButton(row, text="Refresh", command=lambda: cb_f.configure(values=flight_items())).pack(side="left", padx=6)

    out = ctk.CTkTextbox(win, height=220); out.pack(fill="both", expand=True, padx=10, pady=10)

    def show_occ():
        idx = parse_flight_index(cb_f.get())
        if not (0 <= idx < len(la.flights)):
            out.delete("1.0", "end")
            out.insert("end", "Select a valid flight.\n")
            return
        code, origin, dest, price, matrix, *_ = la.flights[idx]
        rows = len(matrix); cols = len(matrix[0]) if rows else 0
        total = rows * cols
        taken = la.ticket_sold(matrix)
        pct = (taken / total * 100) if total else 0
        out.delete("1.0", "end")
        out.insert("end", f"Flight {idx+1} - {code or 'NO_CODE'} {origin or '?'} → {dest or '?'}\n")
        out.insert("end", f"Total seats: {total}\n")
        out.insert("end", f"Taken: {taken}\n")
        out.insert("end", f"Occupancy: {pct:.2f}%\n")

    def show_rev():
        idx = parse_flight_index(cb_f.get())
        if not (0 <= idx < len(la.flights)):
            out.delete("1.0", "end")
            out.insert("end", "Select a valid flight.\n")
            return
        code, origin, dest, price, matrix, *_ = la.flights[idx]
        tickets = la.ticket_sold(matrix)
        total_collected = tickets * (price or 0)
        out.delete("1.0", "end")
        out.insert("end", f"Flight {idx+1} - {code or 'NO_CODE'} {origin or '?'} → {dest or '?'}\n")
        out.insert("end", f"Tickets sold: {tickets}\n")
        out.insert("end", f"Ticket price: {price}\n")
        out.insert("end", f"Total revenue: {total_collected}\n")

    btns = ctk.CTkFrame(win); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Occupancy", command=show_occ).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Revenue", command=show_rev).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Back", command=lambda: back_to_main(win)).pack(side="left", padx=6)


def open_search():
    win = ctk.CTkToplevel(root)
    win.title("Search Flights")
    win.geometry("620x340")

    row = ctk.CTkFrame(win); row.pack(fill="x", padx=10, pady=10)
    ent_dest = ctk.CTkEntry(row, placeholder_text="Destination (e.g., Bogota)")
    ent_dest.pack(side="left", padx=6)
    out = ctk.CTkTextbox(win, height=220); out.pack(fill="both", expand=True, padx=10, pady=10)

    def do_search():
        d = ent_dest.get().strip()
        out.delete("1.0", "end")
        if not d:
            out.insert("end", "Enter a destination.\n")
            return
        result = la.search_flights_by_destination(d)
        out.insert("end", f"Destination: {d}\n\n")
        if not result:
            out.insert("end", "No flights found.\n")
            return
        out.insert("end", f'Flights to "{d}":\n')
        for (num, seats_free) in result:
            out.insert("end", f"- Flight {num} (available seats: {seats_free})\n")

    btns = ctk.CTkFrame(win); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Search", command=do_search).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Back", command=lambda: back_to_main(win)).pack(side="left", padx=6)


def open_consecutive():
    win = ctk.CTkToplevel(root)
    win.title("Consecutive Booking")
    win.geometry("620x280")

    row = ctk.CTkFrame(win); row.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(row, text="Flight:").pack(side="left")
    cb_f = ctk.CTkComboBox(row, values=flight_items(), width=160); cb_f.pack(side="left", padx=6)
    ent_row = ctk.CTkEntry(row, placeholder_text="Row (A, B, AA)", width=130); ent_row.pack(side="left", padx=6)
    ent_start = ctk.CTkEntry(row, placeholder_text="Start column", width=110); ent_start.pack(side="left", padx=6)
    ent_amount = ctk.CTkEntry(row, placeholder_text="Amount", width=90); ent_amount.pack(side="left", padx=6)

    def do_run():
        idx = parse_flight_index(cb_f.get())
        if idx < 0:
            show_error("Select a valid flight.")
            return
        r = letter_to_index(ent_row.get())
        try:
            start = int(ent_start.get()) - 1
            amount = int(ent_amount.get())
        except ValueError:
            show_error("Enter numbers for start/amount.")
            return
        resp = la.book_consutive_seats(idx, r, start, amount)
        if isinstance(resp, str) and resp:
            if "exitosamente" in resp.lower():
                # Las variables start y amount ya están definidas en el scope de do_run
                seat_list = [f"{index_to_letter(r)}{i+1}" for i in range(int(ent_start.get())-1, 
                                                                        int(ent_start.get())-1 + int(ent_amount.get()))]
                show_info("Booked successfully: " + " ".join(seat_list))
            else:
                show_error(resp)
        else:
            show_info("Operation done.")

    btns = ctk.CTkFrame(win); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Book", command=do_run).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Back", command=lambda: back_to_main(win)).pack(side="left", padx=6)


def open_mass_sale():
    win = ctk.CTkToplevel(root)
    win.title("Mass Sale")
    win.geometry("480x220")

    row = ctk.CTkFrame(win); row.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(row, text="Percentage (1-100):").pack(side="left")
    ent_pct = ctk.CTkEntry(row, width=120); ent_pct.pack(side="left", padx=6)

    def do_run():
        try:
            pct = int(ent_pct.get())
        except ValueError:
            show_error("Enter an integer percentage.")
            return
        if pct < 1 or pct > 100:
            show_error("Percentage must be 1..100.")
            return
        resp = la.simulate_mass_booking(la.flights, pct)
        show_info(resp if isinstance(resp, str) and resp else "Mass sale done.")

    btns = ctk.CTkFrame(win); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Run", command=do_run).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Back", command=lambda: back_to_main(win)).pack(side="left", padx=6)


def open_reset():
    win = ctk.CTkToplevel(root)
    win.title("Reset Flight")
    win.geometry("520x240")

    row = ctk.CTkFrame(win); row.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(row, text="Flight:").pack(side="left")
    cb_f = ctk.CTkComboBox(row, values=flight_items(), width=160); cb_f.pack(side="left", padx=6)

    def do_reset():
        idx = parse_flight_index(cb_f.get())
        if not (0 <= idx < len(la.flights)):
            show_error("Select a valid flight.")
            return
        matrix = la.flights[idx][4]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = 0
        la.flights[idx][5] = 0  # sold counter reset
        show_info("Flight seats reset.")

    btns = ctk.CTkFrame(win); btns.pack(pady=(0, 8))
    ctk.CTkButton(btns, text="Reset", command=do_reset).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Back", command=lambda: back_to_main(win)).pack(side="left", padx=6)

# ==========================
# Main window (fixed size)
# ==========================

def main_window():
    global root
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root.title("Airline Reservation System")
    root.geometry("1000x700")  # fixed size as requested
    root.resizable(False, False)

    title = ctk.CTkLabel(root, text="Welcome to the Airline Reservation System", font=("Arial", 22, "bold"))
    title.pack(pady=16)

    grid = ctk.CTkFrame(root)
    grid.pack(pady=8)

    buttons = [
        ("Create Flight", open_create_flight),
        ("Assign Data", open_assign_data),
        ("Reservations", open_reservations),
        ("Flight Status", open_status),
        ("Statistics", open_statistics),
        ("Search Flights", open_search),
        ("Consecutive Booking", open_consecutive),
        ("Mass Sale", open_mass_sale),
        ("Reset Flight", open_reset),
        ("Exit", root.destroy),
    ]

    for i, (text, cmd) in enumerate(buttons):
        btn = ctk.CTkButton(grid, text=text, width=220, command=cmd)
        btn.grid(row=i // 2, column=i % 2, padx=10, pady=8, sticky="ew")

    root.mainloop()


if __name__ == "__main__":
    main_window()
