from SPARQLWrapper import SPARQLWrapper, JSON
from functools import reduce

#set endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql") 
#set query
sparql.setQuery("""
    SELECT DISTINCT ?livro ?autor_  ?ano_publicado ?publicado_por
        WHERE
            {   {?Book a bibo:Book.}
                UNION
                {?Book a yago:Book106410904.}

                ?Book dbo:wikiPageWikiLink dbr:Fantasy.
                ?Book dbp:name ?livro.
                ?Book dbp:author ?Autor__.
                ?Autor__ foaf:name ?autor_.
            
                
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
def autor_lista(lista):
  return list( set([pos['autor_'] for pos in lista]))
def autor_filtra_nome(lista, nome):
  return list (filter(lambda x: x['autor_'].__contains__(nome) , lista) )
def autor_igual(lista, nome):
  return list (filter(lambda x: x['autor_'] == nome, lista) )

def autor_contato_com_publicadora(lista, nome):
  #lista_publicadoras na verdade sao os dicionarios que aquele autor aparece
  lista_publicadoras = filter(lambda x: x['autor_'] == nome, lista)
  #obtendo as publicadoras(sem repeticao de nome)
  return list(set([x['publicado_por'] for x in lista_publicadoras]))

def autor_lista_livros(lista, nome):
  #lista_livros na verdade sao os dicionarios que aquele autor aparece
  lista_livros = filter(lambda x: x['autor_'] == nome, lista)
  #transforma a key 'livro' no dicionario lista_livros em um conjunto 
  #para evitar repeticoes de nome de livro
  return list(set([x['livro'] for x in lista_livros]))

def autor_qtd_livros(lista,nome):
  #obtem a lista de livros do autor referente a nome, calcula o tamanho e entao
  #faz uma tupla com (nome, count), sendo count a quantidade de livros do autor
  return (nome,len(autor_lista_livros(lista,nome)))

def autor_lista_bem_sucedidos(lista):
    lista_autores = [autor_qtd_livros(lista,posicao['autor_']) for posicao in lista]
    #print(lista_autores)
    return list(set(filter(lambda x: x[1] >5, lista_autores)))

##
#----------Sobre o livro
#
#
def livro_anos_publicados(lista, livro):
  #lista_livros na verdade sao os dicionarios que aquele livro aparece
  lista_livros = filter(lambda x: x['livro'] == livro, lista)

  #transforma a key 'ano_publicacao' no dicionario lista_livros em um conjunto 
  #para evitar repeticoes de ano de publicacao
  return list(set([x['ano_publicado'] for x in lista_livros]))

def livro_qtd_anos_publicados(lista, livro):
  return (livro, len(livro_anos_publicados(lista, livro)))

def livro_lista_republicados(lista):
  #lista_publicadoras na verdade sao os dicionarios que aquele autor aparece
  lista_publicadoras = [(posicao['livro'], livro_anos_publicados(lista,posicao['livro'])) for posicao in lista]
  
  lista_republicados = list(filter(lambda x: len(x[1]) > 1, lista_publicadoras))
  #retira as duplicatas
  return [x for i, x in enumerate(lista_republicados) if x not in lista_republicados[:i]]

##
#----------Sobre o ano
#
#
def ano_publicados(lista):
  

  #transforma a key 'ano_publicado' dos dicionarios da lista 
  #para evitar repeticoes de ano de publicacao
  return list(set([x['ano_publicado'] for x in lista]))

def ano_public_apos_ano(lista, data):
  data = str(data)
  return list( filter(lambda x: x['ano_publicado']>data, lista) )
def ano_public_antes_ano(lista, data):
  data = str(data)
  return list( filter(lambda x: x['ano_publicado']<data, lista) )
def ano_public_mesmo_ano(lista, data):
  data = str(data)
  return list( filter(lambda x: x['ano_publicado']==data, lista) )

def ano_lista_livros(lista,data):
  lista_livros = ano_public_mesmo_ano(lista, data)
  #transforma a key 'livro' no dicionario lista_livros em um conjunto 
  #para evitar repeticoes de livro
  return list(set([x['livro'] for x in lista_livros]))

def ano_qtd_livros(lista,data):
  return (data,len(ano_lista_livros(lista,data)))

def ano_lista_concorridos(lista):
  lista_anos = list(set([x['ano_publicado'] for x in lista]))
  return sorted([ano_qtd_livros(lista, x)[0] for x in lista_anos if ano_qtd_livros(lista, x)[1] >=5], reverse=True)

##
#----------Sobre a publicadora
#
#
def publicadora_igual(lista, publicadora):
  return list (filter(lambda x: x['publicado_por'] == publicadora , lista) )

def publicadora_lista(lista):
  return list( set([pos['publicado_por'] for pos in lista]))

def publicadora_lista_livros(lista,publicadora):
  lista_livros = publicadora_igual(lista, publicadora)
  #transforma a key 'livro' no dicionario lista_livros em um conjunto 
  #para evitar repeticoes de livro
  return list(set([x['livro'] for x in lista_livros]))

"""
----------------------
----------------------
--------TESTES--------
----------------------
----------------------
"""

res = getRes(results)
#print(list(res))
#print("\n\n------------------------------------------\n\n")
#print(filtra_nome_autor(res, 'John'))
#print("\n\n------------------------------------------\n\n")
#print(public_apos(res, '2015'))
#print(res[0].keys())
#print(res[0]['publicado_por'])
#print(igual_publicadora(res, 'Harper Paperbacks'))
#print_list_melhorado(igual_publicadora(res, 'Harper Paperbacks'), 'Mesma publicadora')


#print(autor_lista_livros(res,"Terry Pratchett"))
#print(list(res))
#print(autor_qtd_livros(res,"Terry Pratchett"))
#print(autor_lista_bem_sucedidos(res))
#print(autor_contato_com_publicadora(res,"Terry Pratchett" ))
#print(autor_lista_livros(res, 'Mary Hoffman'))
#print(livro_lista_republicados(res))
#print(autor_lista(res))
#print(ano_lista_livros(res, 2007))
#print(ano_qtd_livros(res, 2007))
#print(ano_lista_concorridos(res))
print(publicadora_lista_livros(res,"Del Rey Books"))