#entrada sao tuplas com coordenadas x,y
#verifica se as coordenadas sao validas
def posicao_valida(pos):
    return 0 < pos[0] and pos[0] <= 8 and 0< pos[1] and pos[1] <= 8


######################33
########################
########################
#movimentacoes possiveis

def movDiagonal_uma_casa(pos):
    return  [   (pos[0]+ dx, pos[1] + dy) for dx in [-1,1] for dy in [-1,1] if(posicao_valida((pos[0]+ dx, pos[1] + dy))) ]

def movHorizontalVertical(pos):
    list_horizontal = [     (pos[0]+ dx, pos[1])       for dx in range(-7,9)    if(posicao_valida((pos[0]+ dx, pos[1])) and dx !=0) ]
    list_vertical   = [     (pos[0], pos[1] + dy)      for dy in range(-7,9)    if(posicao_valida((pos[0], pos[1]+dy)) and dy !=0) ]
    
    return  list_horizontal +list_vertical

def movDiagonal(pos):
    list_1 = [  (pos[0] + dx, pos[1])    for dx in range(-7,9) if(posicao_valida((pos[0]+ dx, pos[1]))  and dx !=0)  ]
    list_2 = [  (pos[0], pos[1] + dy)    for dy in range(-7,9) if(posicao_valida((pos[0], pos[1] + dy)) and dy !=0) ]

    return list_1+list_2

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



print(movDiagonal((4,4)))


















#entrada sao tuplas com coordenadas x,y
def verificaMovPossivel_cavalo(mov,pos):
    if(posicao_valida(mov) and posicao_valida(pos)):
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

