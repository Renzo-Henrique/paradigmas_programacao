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
            }""")

#set return format to JSON
sparql.setReturnFormat(JSON) 

# execute query and returns result in JSON format
results = sparql.query().convert() 

#print(results)


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
#print(list(res))

def getRes(resDcit):
  VALUES = resDcit['results']['bindings']
  return list( map ( lambda item: dict( 
                     map ( lambda key: (key, item[key]['value']) 
                           , item.keys() )
             ) , VALUES) )


def print_list_melhorado(lista, message):
  print("-----" +message+ "-----")
  print('\n'.join('{}: {}'.format(*k) for k in enumerate(lista)))

#FUNCOES DIVIDIDAS POR INFORMACAO
##
#----------Sobre o autor
#
#
# Retorna uma lista de nomes de autor únicos a partir da lista de dicionários
def autor_lista(lista):
  return list(set([pos['autor_'] for pos in lista]))

# Filtra a lista de dicionários para incluir apenas entradas em que o nome do autor contém o nome especificado
def autor_filtra_nome(lista, nome):
  return list(filter(lambda x: x['autor_'].__contains__(nome), lista))

# Filtra a lista de dicionários para incluir apenas entradas em que o nome do autor é exatamente igual ao nome especificado
def autor_igual(lista, nome):
  return list(filter(lambda x: x['autor_'] == nome, lista))

# Retorna uma lista de nomes de editora únicos com as quais o autor especificado está associado
def autor_contato_com_publicadora(lista, nome):
  # Lista de dicionários em que o autor aparece
  lista_publicadoras = filter(lambda x: x['autor_'] == nome, lista)
  # Obtendo as editoras (sem repetição de nome)
  return list(set([x['publicado_por'] for x in lista_publicadoras]))

# Retorna uma lista de títulos de livros únicos associados ao autor especificado
def autor_lista_livros(lista, nome):
  # Lista de dicionários em que o autor aparece
  lista_livros = filter(lambda x: x['autor_'] == nome, lista)
  # Transforma a chave 'livro' nos dicionários em um conjunto para evitar repetições de nome de livro
  return list(set([x['livro'] for x in lista_livros]))

# Retorna uma tupla contendo o nome do autor e a contagem de livros associados a esse autor
def autor_qtd_livros(lista, nome):
  # Obtém a lista de livros do autor especificado por 'nome', calcula o tamanho e retorna uma tupla (nome, count),
  # em que count é a quantidade de livros do autor
  return (nome, len(autor_lista_livros(lista, nome)))

# Retorna uma lista de autores que escreveram mais de 5 livros
def autor_lista_bem_sucedidos(lista):
  lista_autores = [autor_qtd_livros(lista, posicao['autor_']) for posicao in lista]
  return list(set(filter(lambda x: x[1] > 5, lista_autores)))

# Retorna a quantidade total de páginas escritas pelo autor especificado
def autor_quantidade_paginas_escritas(lista, nome):
  lista_tuplas = pagina_lista_livros_com_pagina_e_autor(lista)
  return (nome, reduce(lambda x, y: x + int(y[2]) if y[0] == nome else x, lista_tuplas, 0))

##
#----------Sobre o livro
#
#
# Retorna uma lista de anos de publicação únicos para o título do livro especificado
def livro_anos_publicados(lista, livro):
  lista_livros = filter(lambda x: x['livro'] == livro, lista)
  return list(set([x['ano_publicado'] for x in lista_livros]))

# Retorna a quantidade de anos de publicação para o título do livro especificado
def livro_qtd_anos_publicados(lista, livro):
  return (livro, len(livro_anos_publicados(lista, livro)))

# Retorna uma lista de livros que foram publicados em múltiplos anos
def livro_lista_republicados(lista):
  lista_publicadoras = [(posicao['livro'], livro_anos_publicados(lista, posicao['livro'])) for posicao in lista]
  lista_republicados = list(filter(lambda x: len(x[1]) > 1, lista_publicadoras))
  # Remove as duplicatas da lista
  return [x for i, x in enumerate(lista_republicados) if x not in lista_republicados[:i]]

##
#----------Sobre o ano
#
#
# Retorna uma lista de anos de publicação únicos a partir da lista de dicionários
def ano_publicados(lista):
  return list(set([x['ano_publicado'] for x in lista]))

# Filtra a lista de dicionários para incluir apenas entradas publicadas após o ano especificado
def ano_public_apos_ano(lista, data):
  return list(filter(lambda x: int(x['ano_publicado']) > data, lista))

# Filtra a lista de dicionários para incluir apenas entradas publicadas antes do ano especificado
def ano_public_antes_ano(lista, data):
  return list(filter(lambda x: int(x['ano_publicado']) < data, lista))

# Filtra a lista de dicionários para incluir apenas entradas publicadas no ano especificado
def ano_public_mesmo_ano(lista, data):
  return list(filter(lambda x: int(x['ano_publicado']) == data, lista))

# Retorna uma lista de títulos de livros únicos publicados no ano especificado
def ano_lista_livros(lista, data):
  lista_livros = ano_public_mesmo_ano(lista, data)
  return list(set([x['livro'] for x in lista_livros]))

# Retorna uma tupla contendo o ano e a contagem de livros publicados nesse ano
def ano_qtd_livros(lista, data):
  return (data, len(ano_lista_livros(lista, data)))

# Retorna uma lista de anos de publicação com pelo menos 5 livros publicados, em ordem decrescente
def ano_lista_concorridos(lista):
  lista_anos = list(set([x['ano_publicado'] for x in lista]))
  return sorted([ano_qtd_livros(lista, x)[0] for x in lista_anos if ano_qtd_livros(lista, x)[1] >= 5], reverse=True)

##
#----------Sobre a publicadora
#
#
# Filtra a lista de dicionários para incluir apenas entradas em que o nome da editora é exatamente igual ao especificado
def publicadora_igual(lista, publicadora):
  return list(filter(lambda x: x['publicado_por'] == publicadora, lista))

# Retorna uma lista de nomes de editora únicos a partir da lista de dicionários
def publicadora_lista(lista):
  return list(set([pos['publicado_por'] for pos in lista]))

# Retorna uma lista de títulos de livros únicos associados à editora especificada
def publicadora_lista_livros(lista, publicadora):
  lista_livros = publicadora_igual(lista, publicadora)
  return list(set([x['livro'] for x in lista_livros]))


##
#----------Sobre o numero de paginas
#
#
# Retorna uma lista de tuplas (livro, pages) representando os títulos dos livros e o número de páginas a partir da lista de dicionários
def pagina_lista_livros_com_pagina(lista):
  return list(set([(pos['livro'], pos['pages']) for pos in lista]))

# Retorna uma lista de tuplas (livro, pages) representando os títulos dos livros e o número de páginas usando a função map
def pagina_lista_livros_com_pagina_usandoMap(lista):
  return list(set(map(lambda pos: (pos['livro'], pos['pages']), lista)))

# Retorna uma lista de tuplas (autor, livro, pages) representando os autores, títulos dos livros e o número de páginas a partir da lista de dicionários
def pagina_lista_livros_com_pagina_e_autor(lista):
  return list(set([(pos['autor_'], pos['livro'], pos['pages']) for pos in lista]))

# Retorna uma lista de tuplas (livro, pages) representando os títulos dos livros e o número de páginas, onde o número de páginas é maior que N
def pagina_lista_livros_paginas_maior_que_N(lista, n):
  return [tuplas for tuplas in pagina_lista_livros_com_pagina(lista) if int(tuplas[1]) > n]


"""
----------------------
----------------------
--------TESTES--------
----------------------
----------------------
"""

resultados = getRes(results)
#print(list(results))
#print("\n\n------------------------------------------\n\n")
#print(filtra_nome_autor(results, 'John'))
#print("\n\n------------------------------------------\n\n")
#print(public_apos(results, '2015'))
#print(res[0].keys())
#print(res[0]['publicado_por'])
#print(igual_publicadora(results, 'Harper Paperbacks'))
#print_list_melhorado(igual_publicadora(results, 'Harper Paperbacks'), 'Mesma publicadora')


#print(autor_lista_livros(results,"Terry Pratchett"))
#print(list(results))
#print(autor_qtd_livros(results,"Terry Pratchett"))
#print(autor_lista_bem_sucedidos(results))
#print(autor_contato_com_publicadora(results,"Terry Pratchett" ))
#print(autor_lista_livros(results, 'Robin DiAngelo'))
#print(livro_lista_republicados(results))
#print(autor_lista(results))
#print(ano_lista_livros(results, 2007))
#print(ano_qtd_livros(results, 2007))
#print(ano_lista_concorridos(results))
#print(publicadora_lista_livros(results,"Del Rey Books"))
#print(pagina_lista_livros_paginas_maior_que_N(results, 1000))
#print(autor_quantidade_paginas_escritas(results, 'Robin DiAngelo'))

print(pagina_lista_livros_com_pagina_usandoMap(results) == pagina_lista_livros_com_pagina(results))


##TO_DO: modificar para pegar somente 1 resultado de página 