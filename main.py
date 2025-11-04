import customtkinter as ctk
import random

def close_window():
    app.withdraw()

def main_window():
    global app
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Airline System")
    app.resizable(False,False)

    # Buttons
    # Botón de cierre situado en la esquina superior derecha
    exit_button = ctk.CTkButton(
        app,
        text="Salir",
        command=close_window,
        width=90,
        height=32,
        corner_radius=8,
        font=("Times New Roman", 16)
    )

    # Colocar en la esquina superior derecha (relx=1.0 es el borde derecho)
    exit_button.place(relx=1.0, x=-10, y=10, anchor='ne')




    app.mainloop()
    





if __name__ == "__main__":
    main_window()