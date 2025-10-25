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
def book_flight(row,column,index):
    matrix = flights[index][4]  #to look the matrix inside the flight selected of index of flights
    if row >= len(matrix) or column >= len(matrix[0]) or row < 0 or column < 0:
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
    

print(book_flight(0,0,0))
print(book_flight(0,1,0))
print(book_flight(0,2,0))
print(book_flight(1,0,0))
print(book_flight(1,1,0))
print(book_flight(1,2,0))
print(book_flight(2,0,0))
print(book_flight(2,1,0))
print(book_flight(2,2,0))




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
    return (matrix/total_seat)*100
#E: get the number of flight
#S: all data inside the lists in a string
#R: the correct flight
def statics(index_flight):
    matrix = flights[index_flight][4]
    code_flight = flights[index_flight][0]
    origin =  flights[index_flight][1]
    destination = flights[index_flight][2]
    price = flights[index_flight][3]
    total_seat = 0

    for _ in range(len(matrix)):
        for _ in range(len(matrix[0])):
            total_seat += 1
    collection_percent = calcute_percentage(flights[index_flight][-1],total_seat)
    collection_percent = round(collection_percent,2)
    return  [code_flight, origin, destination, price, total_seat, collection_percent]

print(statics(0))



