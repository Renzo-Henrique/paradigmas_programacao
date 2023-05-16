from functools import reduce
#####----A
def list_1_to_N(n):
    list_numbers = list(range(1, n+1))
    #for i in range[1:n+1]:
        #list.append()
    
    return list_numbers

#####----B
def list_N_to_1(n):
    list_numbers = list_1_to_N(n)
    reversed_list = list_numbers[::-1]

    return reversed_list

#####----C
def list_double_1_to_N(n):
    list_numbers = list_1_to_N(n)
    #[2*x for x in list_numbers]

    # Using map instead of reduce to double each element
    list_doubled = list(map(lambda x: 2*x, list_numbers))  

    return list_doubled

#####----D
def list_1_to_doubleN(n):
    
    return list_1_to_N(2*n)

#####----E
def list_1_to_N_divisible_by_3(n):
    list_numbers = list_1_to_N(n)

    return list(filter(lambda x: x%3==0, list_numbers))

#####----F
def list_oddSquare_pairDouble_1_to_N(n):
    list_numbers = list_1_to_N(n)
    #[2*x for x in list_numbers]

    # Using map instead of reduce to double each element
    list_modified = list(map(lambda x: 2*x if(x%2 ==0) else x*x, list_numbers)) 

    return list_modified

#####----G
def list_multiply_by_k(list_numbers, k):
    return list(map(lambda x: k*x, list_numbers))

#####----H
def list_addOdd_subtractPair(list_numbers):
    last_number = list_numbers[-1]
    if last_number %2 == 0:
        last = -1*last_number
    else:
        last = last_number
    return reduce((lambda x, y: x-y if y%2==0 else x+y), list_numbers, 0 )

#####----I
def list_numbers_components_added_from_N(n):
    list_numbers = list_1_to_N(n)

    def sum_digits(x):
        # Converte o número em uma lista de dígitos
        digits = list(str(x))
        
        # Converte cada dígito de volta para número e soma-os usando a função `sum`
        return sum(map(int, digits))
    
    return [(x,y) for x in list_numbers for y in list_numbers if  x!=y and (sum_digits(x) + sum_digits(y) == n)  ] 

#####----J
def list_from_list(list_numbers):
    return [([list_numbers[x], list_numbers[x+1],list_numbers[x+2] ]) for x in range(0, len( list_numbers) -2)]

#####----K
def list_min_max(list_numbers):
    return (min(list_numbers), max(list_numbers))

n = 10
k=3

print('Order:\n1_to_N\nN_to_1\n1_to_doubleN\n1_to_N_divisible_by_3')
print(list_1_to_N(n))
print(list_N_to_1(n))
print(list_double_1_to_N(n))
print(list_1_to_N_divisible_by_3(n))

print('\noddSquare_pairDouble_1_to_N\nmultiply_by_k\naddOdd_subtractPair')
print(list_oddSquare_pairDouble_1_to_N(n))
print(list_multiply_by_k(list_1_to_N(n), k))
print(list_addOdd_subtractPair(list_1_to_N(n)))
print('\nnumbers_components_added_form_N\nfrom_list\nmin_max')
print(list_numbers_components_added_from_N(n))
print(list_from_list(list_1_to_N(n)))
print(list_min_max(list_1_to_N(n)))


######### numbers_components
