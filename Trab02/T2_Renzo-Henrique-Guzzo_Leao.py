from SPARQLWrapper import SPARQLWrapper, JSON

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
            
                optional{
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
print(list(res))


def getRes(resDcit):
  VALUES = resDcit['results']['bindings']
  return list( map ( lambda item: dict( 
                     map ( lambda key: (key, item[key]['value']) 
                           , item.keys() )
             ) , VALUES) )

def public_apos(lista, data):
  return list( filter(lambda x: x['ano_publicado']>data, lista) )

def filtra_nome(lista, nome):
  return list (filter(lambda x: x['autor_'].__contains__(nome) , lista) )

def filtra_publicadora(lista, publicadora):
  return list (filter(lambda x: x['publicado_por'].__contains__(publicadora) , lista) )

res = getRes(results)
#print(filtra_nome(res, 'John'))
print("\n\n------------------------------------------\n\n")
#print(public_apos(res, '2015'))
print(filtra_publicadora(res, 'Harper Paperbacks'))