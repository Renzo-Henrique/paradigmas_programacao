from SPARQLWrapper import SPARQLWrapper, JSON
from functools import reduce


#set endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql") 
#set query
sparql.setQuery("""
    SELECT DISTINCT ?Book ?livro ?autor_  (max(?pages_) as ?pages) ?ano_publicado ?publicado_por
        WHERE
            {   {?Book a bibo:Book.}
                UNION
                {?Book a yago:Book106410904.}

                ?Book dbp:name ?livro.
                ?Book dbp:author ?Autor__.
                ?Autor__ foaf:name ?autor_.

                ?Book dbo:numberOfPages ?pages_.
                
                FILTER(datatype(?pages_) = (xsd:positiveInteger) && ?pages_  <2000)

                  
            
                
                {
                  ?Book dbp:publisher ?Publicadora_.
                  ?Publicadora_ rdfs:label ?publicado_por.
                  FILTER ( lang(?publicado_por) = 'en' && ?publicado_por!= ''@en )
                }
                UNION
                {
                  ?Book dbp:publisher ?publicado_por.   
                  FILTER ( lang(?publicado_por) = 'en' && ?publicado_por!= ''@en )
                }
                

                {
                    ?Book dbp:pubDate ?ano_publicacao.
                    FILTER(datatype(?ano_publicacao) = xsd:date)

                    BIND( YEAR(xsd:date(?ano_publicacao) )  as  ?ano_publicado ).
                }
                UNION
                {
                    ?Book dbp:pubDate ?ano_publicado.
                    FILTER(datatype(?ano_publicado) = xsd:integer)      
                }

                FILTER ( lang(?livro) = 'en' && ?livro != ''@en)
                FILTER ( lang(?autor_) = 'en' && ?autor_ != ''@en )
            }LIMIT 2000""")

#set return format to JSON
sparql.setReturnFormat(JSON) 

# execute query and returns result in JSON format
results = sparql.query().convert() 


### PROCESSING THE RESULTS USING FUNCTIONAL FEATURES
if results:
  ## results has two parts: head and results with lots of info
  ## we are mainly interested in varibles and the bindings
  ## we want to process those into a more meaningful dictionary 
  ## we start by (re)naming the two as follows:
  VALUES = results['results']['bindings']
  KEYS = results['head']['vars']

  ## 1st: we want to visualize what is in each of them
  #print(KEYS)
  #print()
  #print(VALUES)

  # GOAL: TRANSFORM THIS STRUCTURE 
  # [{'birthdate': {'type': 'typed-literal', 'datatype': 'http://www.w3.org/2001/XMLSchema#date', 'value': '1718-05-16'}, 
  #   'uri': {'type': 'uri', 'value': 'http://dbpedia.org/resource/Maria_Gaetana_Agnesi'}, 
  #   'name': {'type': 'literal', 'xml:lang': 'en', 'value': 'Maria Gaetana Agnesi'}, 
  #   'description': {'type': 'literal', 'xml:lang': 'en', 'value': 'Maria Gaetana Agne...'} 
  #  }, ...]
  # INTO
  # [{'birthdate': '1718-05-16', 
  #   'uri': 'http:/.../Maria_Gaetana_Agnesi', 
  #   'name': 'Maria Gaetana Agnesi', 
  #   'description': 'Maria Gaetana Agne...' 
  #  }, ... ] 

  ## 2nd: what is in KEYS is also in VALUES as the keys of the dictionary
  ## so we need to use only VALUES to
  ## print dict-like results using nested loops
  # for item in VALUES:
  #   for key in item.keys():
  #     print(key, ': ', item[key]['value'])
  #   print()

  ## 3rd: eliminating one loop using comprehesion
  # for item in VALUES:
  #   print({key: item[key]['value'] for key in item.keys() })

  ## 4th: eliminating both loops using comprehesion
  # print( [ { key: item[key]['value']
  #            for key in item.keys()
  #          } 
  #         for item in VALUES       
  #        ] )
  
  ## 5th: eliminating one comprehension using map
  # print( [ dict( map ( lambda key: (key, item[key]['value']) 
  #                     , item.keys() ) )
  #         for item in VALUES       
  #        ] )

  ## 6th: eliminating both comprehensions using map
  res = map ( lambda item: dict( 
                     map ( lambda key: (key, item[key]['value']) 
                           , item.keys() )
             ) , VALUES)

def getRes(resDcit):
  VALUES = resDcit['results']['bindings']
  return list( map ( lambda item: dict( 
                     map ( lambda key: (key, item[key]['value']) 
                           , item.keys() )
             ) , VALUES) )




##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
#FUNCOES DIVIDIDAS POR INFORMACAO
##
#----------print
#
#
#recomendado usar quando quiser visualizar melhor os dicionários dos resultados
def print_list_melhorado(lista):
  print('\n'.join('{}: {}'.format(*k) for k in enumerate(lista)))

############################################
#----------Sobre o autor
###########################################
###########################################
#lista de todos os autores
def autor_lista(lista):
  return list( set([pos['autor_'] for pos in lista]))

#lista de todos os autores usando map
def autor_lista_map(lista):
  return list( set(map(lambda pos: pos['autor_'], lista)))

#lista de autores de que possuem *autor* em alguma parte do seu nome
def autor_filtra_nome(lista, autor):
  return list (filter(lambda x: x['autor_'].__contains__(autor) , lista) )

#retorna os resultados pesquisados pelo autor do autor
def autor_igual(lista, autor):
  return list (filter(lambda x: x['autor_'] == autor, lista) )

#retorna o nome das publicadoras que o autor tem contato
def autor_contato_com_publicadora(lista, autor):
  #lista_publicadoras na verdade sao os dicionarios que aquele autor aparece
  lista_publicadoras = filter(lambda x: x['autor_'] == autor, lista)
  #obtendo as publicadoras(sem repeticao de autor)
  return list(set(map(lambda x: x['publicado_por'], lista_publicadoras)))

#retorna a lista de um dado autor
def autor_lista_livros(lista, autor):
  #lista_livros na verdade sao os dicionarios que aquele autor aparece
  lista_livros = filter(lambda x: x['autor_'] == autor, lista)
  #transforma a key 'livro' no dicionario lista_livros em um conjunto 
  #para evitar repeticoes de autor de livro
  return list(set(map(lambda x: x['livro'], lista_livros)))

#retorna a quantidade de livros de um dado autor
def autor_qtd_livros(lista,autor):
  #obtem a lista de livros do autor referente a autor, calcula o tamanho e entao
  #faz uma tupla com (autor, count), sendo count a quantidade de livros do autor
  return (autor,len(autor_lista_livros(lista,autor)))

#retorna a lista de autores com mais de cinco livros
def autor_lista_bem_sucedidos(lista):
    lista_autores = [autor_qtd_livros(lista,posicao['autor_']) for posicao in lista]
    #print(lista_autores)
    return list(set(filter(lambda x: x[1] >5, lista_autores)))

#retorna a quantidade de paginas de livros escritas pelo autor
def autor_quantidade_paginas_escritas(lista, nome):
  lista_tuplas = pagina_lista_livros_com_pagina_e_autor(lista)
  return (nome,reduce(lambda x, y: x + int(y[2]) if  y[0] == nome else x, lista_tuplas, 0))

############################################
#----------Sobre o livro
###########################################
###########################################

#retorna os resultados que possuem *livro* em alguma parte do seu nome
def livro_filtra_nome(lista, livro):
  return list (filter(lambda x: x['livro'].__contains__(livro) , lista))

#retorna os resultados pesquisados pelo livro do livro
def livro_igual(lista, livro):
  return list (filter(lambda x: x['livro'] == livro, lista) )

#retorna a lista de anos publicados de um dado livro
def livro_anos_publicados(lista, livro):
  #lista_livros na verdade sao os dicionarios que aquele livro aparece
  lista_livros = filter(lambda x: x['livro'] == livro, lista)

  #transforma a key 'ano_publicacao' no dicionario lista_livros em um conjunto 
  #para evitar repeticoes de ano de publicacao
  return list(set(map(lambda x: x['ano_publicado'], lista_livros)))

#retorna a quantidade de anos publicados de um livro
def livro_qtd_anos_publicados(lista, livro):
  return (livro, len(livro_anos_publicados(lista, livro)))

#retorna a lista de livros republicados
def livro_lista_republicados(lista):
  #lista_publicadoras na verdade sao os dicionarios que aquele autor aparece
  lista_publicadoras = [(posicao['livro'], livro_anos_publicados(lista,posicao['livro'])) for posicao in lista]
  
  lista_republicados = list(filter(lambda x: len(x[1]) > 1, lista_publicadoras))
  #retira as duplicatas
  return [x for i, x in enumerate(lista_republicados) if x not in lista_republicados[:i]]

############################################
#----------Sobre o ano
###########################################
###########################################

#retorna a lista de anos em que houve ao menos uma publicacao de livro
def ano_publicados(lista):
  
  #transforma a key 'ano_publicado' dos dicionarios da lista 
  #para evitar repeticoes de ano de publicacao
  return list(set(map(lambda x: x['ano_publicado'], lista)))

#retorna os resultados que possuem o ano de publicacao apos data
def ano_public_apos_ano(lista, data):
  return list( filter(lambda x: int(x['ano_publicado'])>data, lista) )
#retorna os resultados que possuem o ano de publicacao antes de data
def ano_public_antes_ano(lista, data):
  return list( filter(lambda x: int(x['ano_publicado'])<data, lista) )
#retorna os resultados que possuem o ano de publicacao igual a data
def ano_public_mesmo_ano(lista, data):
  return list( filter(lambda x: int(x['ano_publicado'])==data, lista) )

def ano_public_entre_data1_data2(lista, data1, data2):
  return list( filter(lambda x: int(x['ano_publicado'])>data1 and int(x['ano_publicado'])<data2, lista) )

#retorna a lista de livros de um ano
def ano_lista_livros(lista,data):
  lista_livros = ano_public_mesmo_ano(lista, data)
  #transforma a key 'livro' no dicionario lista_livros em um conjunto 
  #para evitar repeticoes de livro
  return list(set(map(lambda x: x['livro'], lista_livros)))

#retorna a quantidade de livros de um dado ano
def ano_qtd_livros(lista,data):
  return (data,len(ano_lista_livros(lista,data)))

#retorna a lista de anos em que houve mais de N publicacoes (ordenado)
def ano_lista_maior_N(lista, n):
  lista_anos = list(set(map(lambda x: x['ano_publicado'], lista)))
  return sorted([ano_qtd_livros(lista, x)[0] for x in lista_anos if ano_qtd_livros(lista, int(x))[1] >=n], reverse=True)

############################################
#----------Sobre a publicadora
###########################################
###########################################

#retorna os resultados que possuem *publicadora* em alguma parte do seu nome
def publicadora_filtra_nome(lista, publicadora):
  return list (filter(lambda x: x['autor_'].__contains__(publicadora) , lista) )

#retorna os resultados que possuem a publicadora
def publicadora_igual(lista, publicadora):
  return list (filter(lambda x: x['publicado_por'] == publicadora , lista) )

#retorna a lista de publicadoras
def publicadora_lista(lista):
  return list( set(map(lambda pos: pos['publicado_por'], lista)))

#retorna a lista de livros de uma dada publicadora
def publicadora_lista_livros(lista,publicadora):
  lista_livros = publicadora_igual(lista, publicadora)
  #transforma a key 'livro' no dicionario lista_livros em um conjunto 
  #para evitar repeticoes de livro
  return list(set(map(lambda x: x['livro'], lista_livros)))



############################################
#----------Sobre o numero de paginas
###########################################
###########################################

#retorna os resultados que possuem o mais paginas que pag
def pagina_livro_mais_quantidade_pagina(lista, pag):
  return list( filter(lambda x: int(x['pages']) > pag, lista) )
#retorna os resultados que possuem o ano de publicacao antes de data
def pagina_livro_menos_quantidade_pagina(lista, pag):
  return list( filter(lambda x: int(x['pages']) < pag, lista) )
#retorna os resultados que possuem o ano de publicacao igual a data
def pagina_livro_mesma_quantidade_pagina(lista, pag):
  return list( filter(lambda x: int(x['pages'])==pag, lista) )

def ano_public_entre_data1_data2(lista, data1, data2):
  return list( filter(lambda x: int(x['pages'])>data1 and int(x['pages'])<data2, lista) )

#retorna uma lista de tuplas contendo (nome_do_livro, paginas)
def pagina_lista_livros_com_pagina(lista):
  return list( set(map(lambda pos: (pos['livro'], pos['pages']), lista)))


#retorna uma lista de tuplas contendo (autor, nome_do_livro, paginas)
def pagina_lista_livros_com_pagina_e_autor(lista):
  return list( set(map(lambda pos: (pos['autor_'], pos['livro'], pos['pages']), lista)))

#retorna uma lista de tuplas contendo os livros que possuem mais que n paginas
def pagina_lista_livros_paginas_maior_que_N(lista, n):
  return [tuplas for tuplas in pagina_lista_livros_com_pagina(lista) if(int(tuplas[1])>n)]

#retorna uma lista de tuplas contendo os livros que possuem menos que n paginas
def pagina_lista_livros_paginas_menos_que_N(lista, n):
  return [tuplas for tuplas in pagina_lista_livros_com_pagina(lista) if(int(tuplas[1])>n)]

#retorna uma lista de tuplas contendo os livros que possuem igual a n paginas
def pagina_lista_livros_paginas_igual_N(lista, n):
  return [tuplas for tuplas in pagina_lista_livros_com_pagina(lista) if(int(tuplas[1])>n)]

#retorna uma lista de tuplas contendo os livros que possuem entre n e m paginas
def pagina_lista_livros_paginas_entre_N_M(lista, n, m):
  return [tuplas for tuplas in pagina_lista_livros_com_pagina(lista) if(int(tuplas[1])>n and int(tuplas[1])<m )]

"""
----------------------
----------------------
------TESTADORES------
----------------------
----------------------
"""

resultados_query = getRes(results)


#testador de funcoes implementadas
def meu_testador_1(res):

  autor_ex = "Terry Pratchett"
  ano_ex = 2007
  quantidade_ex = 50

  print("\nLista de livros de ", autor_ex, ":\n", autor_lista_livros(res,autor_ex))
  print("\nLista de páginas escritas por ", autor_ex, ":\n", autor_quantidade_paginas_escritas(res, autor_ex))
  print("\nLista de livros do ano ",ano_ex, ":\n", ano_lista_livros(res, ano_ex))
  print(ano_qtd_livros(res,ano_ex))
  print("\nLista de anos com mais de ", quantidade_ex, " livros:\n", ano_lista_maior_N(res, quantidade_ex))

#testador de funcoes implementadas
def meu_testador_2(res):

  autor_ex = "Mary Renault"
  autor_filtra = "Mary"
  publicadora_ex = "Del Rey Books"

  print("\nLista de livros da publicadora ", publicadora_ex, ":\n", publicadora_lista_livros(res,publicadora_ex))
  print("\nLista de publicadoras em contato com ", autor_ex, ":\n", autor_contato_com_publicadora(res,autor_ex))
  
  print("\nFiltrando resultados de nome do autor com ",autor_filtra, ":")
  print_list_melhorado(autor_filtra_nome(res, autor_filtra))

#combinando funcoes implementadas
def meu_testador_3(res):
  autor_filtra = "John"
  ano_ex = 2015
  pagina_ex = 300

  lista_autor = autor_filtra_nome(res, autor_filtra)
  lista_autor_ano = ano_public_apos_ano(lista_autor, ano_ex)
  lista_autor_ano_pagina =  pagina_livro_mais_quantidade_pagina(lista_autor_ano, pagina_ex)
  
  print("\nFiltrando resultados de nome do autor com ",autor_filtra, ":")
  print(  lista_autor)
  print("\nFiltrando resultados de nome do autor com ",autor_filtra, "e apos o ano ", ano_ex, ":")
  print_list_melhorado( lista_autor_ano)
  print("\nFiltrando resultados de nome do autor com ",autor_filtra, ", apos o ano ", ano_ex, " e com mais paginas que ", pagina_ex, ":")
  print_list_melhorado( lista_autor_ano_pagina)

    
##########################################
##########################################
##########################################
##########TESTES RECOMENDADOS#############
#meu_testador_1(resultados_query)
#meu_testador_2(resultados_query)
meu_testador_3(resultados_query)


