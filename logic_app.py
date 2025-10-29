import random

#fuction to create flights
flights = []
People = [[]]

#E: code(string), origin(string), destination(string), price(float), price(integer), column,column(integer), sold_count(int)
#S: a list with new elements
#R: only if the row is less than 50 and row 20
def create_flight(code, origin, destination, price, row, column):
    seat_matrix = [[0]*row for i in range(column)]
    if row > 50 and column > 20:
        return "Has sobrepasado el limite maximo permitido row: 50, column:20"
    flights.append([code,origin,destination, price, seat_matrix,0])
    

print(create_flight("M","A","B",0, 3,3 ))

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

    if row >= lenght_row or column >= lenght_column or row < 0 or column < 0:
        return f"Ingrese un valor dentro del rango."
    
    for _ in range(len(matrix)):
        for _ in range(len(matrix[0])):

            if matrix[row][column] == 0:  #if the number keep going 0 get chance it by 1
                matrix[row][column] = 1
                flights[index][-1] += 1
                flights[index][4] = matrix
                return "Asiento reservado"
                
            else:
                return "El campo esta ocupado"


def all_are_one(row, matrix):
    if row < 0 or row >= len(matrix):
        return False
    
    for i in range (len(matrix[0])):
        if matrix[row][i] == 0:
            return False
    return True




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

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):

            if matrix[row][column] != 0:
                matrix[row][column] == 0
                
                
    flights[index][4] == matrix


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


