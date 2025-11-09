import random
import string

#fuction to create flights
flights = []

def generate_seat_labels(rows, columns):
    """
    Genera etiquetas de asientos tipo A1, A2... AA1, AB1, etc.
    según las filas y columnas del vuelo.
    """
    seat_labels = []
    letters = []

    # Generar letras de la A a la Z, luego AA, AB, etc.
    for i in range(rows):
        if i < 26:
            letters.append(chr(65 + i))  # 65 = 'A'
        else:
            first = chr(65 + (i // 26) - 1)
            second = chr(65 + (i % 26))
            letters.append(first + second)

    # Combinar letras con números de columna
    for letter in letters:
        row_labels = []
        for col in range(1, columns + 1):
            label = f"{letter}{col}"
            row_labels.append(label)
        seat_labels.append(row_labels)

    return seat_labels


#E: code(string), origin(string), destination(string), price(float), price(integer), column,column(integer), sold_count(int)
#S: a list with new elements
#R: only if the row is less than 50 and row 20
def create_flight(row,column):

    if row > 50 or column > 20:
        return "Has sobrepasado el limite maximo permitido row: 50, column:20"
    seat_matrix = [[0]*column for _ in range(row)]
    seat_labels = generate_seat_labels(row, column)
    flights.append(["","","", 0, seat_matrix,0,seat_labels])





def assign_flight(origin, destination, price, index_flight, code):
    """
    Asigna datos a un vuelo existente. Ahora requiere un `code` manual.
    Retorna un mensaje de error (string) en caso de fallo, o None en caso exitoso.
    """
    if index_flight < 0 or index_flight >= len(flights):
        return "Invalid flight number."

    if not code or not isinstance(code, str):
        return "Se requiere un código de vuelo válido."

    # Verificar que el código no exista en otro vuelo
    for i, f in enumerate(flights):
        if i != index_flight and isinstance(f, list) and f and f[0] and f[0].upper() == code.upper():
            return "El código ya está en uso por otro vuelo."

    flight = flights[index_flight]
    flight[0] = code
    flight[1] = origin
    flight[2] = destination
    flight[3] = price
#E: a integer
#S: one list inside the main list of the program
def get_flight(index):
    return flights[index]


#E: row, column, index
#S: a new matrix with the selected seat occupied
def book_flight(row,column,index): #version convencional de reservar individualmente
    
    matrix = flights[index][4]  #to look the matrix inside the flight selected of index of flights
    lenght_row = len(matrix)
    lenght_column = len(matrix[0])
    taking_seats = flights[index][-1]
    

    if row >= lenght_row or column >= lenght_column or row < 0 or column < 0:
        return f"Ingrese un valor dentro del rango."
    
    for _ in range(len(matrix)):
        for _ in range(len(matrix[0])):

            if matrix[row][column] == 0:  #if the number keep going 0 get chance it by 1
                matrix[row][column] = 1
                
                return "Asiento reservado"
                
            else:
                return "El campo esta ocupado"

#E: integer and matrix
#S: boolean value
def all_are_one(row, matrix):
    if row < 0 or row >= len(matrix):
        return False
    
    for i in range (len(matrix[0])):
        if matrix[row][i] == 0:
            return False
    return True


#E: index_flight, row, start column and amount seats = int
#S: a new matrix with

def book_consutive_seats(index_flight,row, start_colum, amount_seats):
    matrix = flights[index_flight][4] #es la matriz de asientos

    column_matrix = len(matrix[0])
    seats_free = 0
    
    if not isinstance(index_flight, int) or not isinstance(amount_seats, int): #si no es un entero
        return "Error: número de vuelo y cantidad deben ser enteros."
    
    if index_flight < 0 or index_flight >= len(flights): #si se el parametro ingresado 
        return "Error: el vuelo no existe."                 #no esta en el rango

    
    if all_are_one(row, matrix): #si todos son uno tira error
        return "Todos los asientos están ocupados"
    
    if amount_seats > column_matrix or amount_seats <= 0:#si a cantidad es mayor o menor a cero
        return "Error: cantidad de asientos inválida."

    if start_colum + amount_seats > column_matrix: #si se sale de rango
        return "Error: no hay espacio suficiente en esa fila."

    for i in range(start_colum, start_colum + amount_seats):
    
        if matrix[row][i] == 0:
            seats_free += 1
        else:
            break
    
    if seats_free == amount_seats:

        for i in range(start_colum, start_colum + amount_seats):
            matrix[row][i] = 1
        return "Reservados exitosamente"
    else:
        return "No se pudo reservar los asientos exitosamamente"


#E: row, column, index
#S: a new matrix without that seat ocuppied

def cancel_flight(row,column,index):
    matrix = flights[index][4]
                                                    #todo Revisar función
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):

            if matrix[row][column] != 0:
                matrix[row][column] = 0

#_________________________________________________________________________________________________________
#sección para la función de venta masiva
def ticket_sold(matrix):
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                count += 1

    return count

def count_seat_matrix(matrix):
    counter = 0
    for _ in range(len(matrix)):
        for _ in range(len(matrix[0])):
            counter += 1
    return counter


def simulate_mass_booking(flights, percentage):
    if not flights:
        return "No hay vuelos disponibles aún"
    
    if percentage > 100 and percentage < 1:
        return "Ingrese un porcentaje dentro del rango de 1 a 100"
    
    for flight in range(len(flights)):
            

            matrix = flights[flight][4]

            current_occupied = ticket_sold(matrix)   #cantidad de asientos ocupados antes 
            total_seats = count_seat_matrix(matrix) #cantidad de asientos de la matriz
            
            target_occupied = int((percentage/100) * total_seats)  #total de asientos que deben estar ocupados al final
            seats_remaining = target_occupied -current_occupied  #asientos que faltan para llegar a la meta 

            if seats_remaining <= 0:
                continue


            while seats_remaining > 0:

                row_random = random.randint(0, len(matrix)-1)    #pos aleatoria
                column_random = random.randint(0, len(matrix[0])-1)  #columna pos aleatoria

                if matrix[row_random][column_random] == 0:    
                            matrix[row_random][column_random] = 1

                            seats_remaining -= 1

    return "Venta masiva hecha correctamente"


#___________________________________________________________________________________________________________

def calcute_percentage(matrix,total_seat):
    return  round((matrix / total_seat) * 100, 2)


def count_seat_matrix(matrix):
    counter = 0
    for _ in range(len(matrix)):
        for _ in range(len(matrix[0])):
            counter += 1
    return counter

#E: get the number of flight
#S: all data inside the lists in a string
#R: the correct flight
def statics(index_flight):
    matrix = flights[index_flight][4]
    code_flight = flights[index_flight][0]
    origin =  flights[index_flight][1]
    destination = flights[index_flight][2]
    total_seat = count_seat_matrix(matrix)

    collection_percent = calcute_percentage(flights[index_flight][-1],total_seat)
    
    return  [code_flight, origin, destination, total_seat, collection_percent]



def ticket_sold(matrix):
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                count += 1

    return count


def revenue_stats(index_flight):
   matrix = flights[index_flight][4]  #la matriz de asientos
   code_flight = flights[index_flight][0]    #el codigo del vuelo
   origin =  flights[index_flight][1]   #el origen
   destination = flights[index_flight][2] #el destino
   price = flights[index_flight][3]       #precio de boleto
   tickets = ticket_sold(matrix)          #boletos vendidos
   total_collected = tickets * price      #total recaudado

   return [code_flight, origin, destination, price, total_collected]


def get_available_flights():
    available_flights = []

    if not flights:
        return []

    for i in range(len(flights)):
        flight = flights[i]
        code, origin, destination, price, seat_matrix, sold = flight

        rows = len(seat_matrix)
        columns = len(seat_matrix[0]) if seat_matrix else 0  # one-line check
        total_seats = rows * columns
        available_seats = total_seats - sold

        available_flights.append([
            f"Flight {i + 1}",
            code,
            origin,
            destination,
            price,
            total_seats,
            available_seats
        ])

    return available_flights


#_______________________________________________________________________________________________________
#sección para la función de buscar vuelos y demas funcionalidades de esta

def counts_seats_free(matrix):
    result = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
           if matrix[i][j] == 0:
            result += 1
    return result


def search_flights_by_destination(destination):
    result = []
    for flight in range(len(flights)):
        
        seats_free = counts_seats_free(flights[flight][4])
        destination_flight = flights[flight][2]
        if destination_flight.lower() == destination.lower():
            result.append((flight+1, seats_free) )
    return result


#_______________________________________________________________________________________________________