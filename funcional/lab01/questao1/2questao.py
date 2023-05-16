#entrada sao tuplas com coordenadas x,y
#verifica se as coordenadas sao validas
def tupla_valida(pos):
    return 0 < pos[0] and pos[0] <= 8 and pos[1] and pos[1] <= 8

#entrada sao tuplas com coordenadas x,y
def verificaMovPossivel_cavalo(mov,pos):
    if(tupla_valida(mov) and tupla_valida(pos)):
        #distancia de x1 e x2 deve ser 1 ou 2, se n for movimento impossivel
        dist_x = abs(mov[0] - pos[0])
        dist_y = abs(mov[1] - pos[1])
        if(dist_x ==1):
            return dist_y ==2
        elif(dist_x ==2):
            return dist_y ==1

    
    return False

#entrada sao tuplas com coordenadas x,y
def MovPossivel_cavalo(pos):
    def next_move(index):
         
        if(index == 1):
            tupla = (1,2)
        elif(index == 2):
            tupla = (2,1)
        elif(index == 3):
            tupla = (2,-1)
        elif(index == 4):
            tupla = (1,-2)
        elif(index == 5):
            tupla = (-1,-2)
        elif(index == 6):
            tupla = (-2,-1)
        elif(index == 7):
            tupla = (-2,1)
        else:
            tupla = (-1,2)
        
        #print(( pos[0]+tupla[0], pos[1]+tupla[1]))
        return ( pos[0]+tupla[0], pos[1]+tupla[1])
        
    list_ = [next_move(index) for index in range(1,9) if verificaMovPossivel_cavalo(next_move(index),pos)]
    reversed_list =list_[::-1]
    return reversed_list

#entrada sao tuplas com coordenadas x,y
def possivelEliminar_cavalo(posCav,outraPeca):
    return verificaMovPossivel_cavalo(posCav,outraPeca)


print(MovPossivel_cavalo((5,4)))