/* Trabalho de Paradigmas de programação
 * Escopo: Aprender e praticar prolog juntamente de sparql
 * Feito por Renzo Henrique Guzzo Leão
 * Data: 11/05/2023
 *
 * */

:- data_source(livros,
               sparql("SELECT DISTINCT ?livro ?autor_  ?ano_publicado ?publicado_por
                      WHERE { {?Book a bibo:Book.}
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
                        }",
                      [ endpoint('http://dbpedia.org/sparql')
                      ])).

livros_de_fantasia(Nome, Autor, Ano, Publicadora) :-
    livros{livro:Nome,
           autor_:Autor,
           ano_publicado: Ano,
           publicado_por:Publicadora}.


/*INFERENCIAS DIVIDIDAS POR INFORMACAO**/

 /**Sobre o autor
 *
 *
 *
 *
 * ***/

/*Autor do Livro tal*/
autor_de(Autor,Livro):-
    distinct([Livro,Autor], (livros_de_fantasia(Livro, Autor,_,_))).


/*Autor fez livro pra tal publicadora*/
autor_fez_publicadora(Autor,Publicadora):-
    distinct([Autor,Publicadora], (livros_de_fantasia(_, Autor,_,Publicadora))).

/*Quantidade de livros do autor*/
quantidade_de_livros_do_autor(Autor,Count):-
    distinct([Autor], ( autor_de(Autor,_))),
    aggregate_all(count, (autor_de(Autor,_)), Count).

/*Autor Possui mais de 5 livros*/
autor_bem_sucedido(Autor, Count):-
quantidade_de_livros_do_autor(Autor,Count), Count @> 5.

/*Lista de livros do autor*/
autor_com_livros(Autor, Lista_de_livros):-
    bagof(Livro,autor_de(Autor,Livro),Lista_de_livros).


/**Sobre o livro
 *
 *
 *
 *
 * ***/

/*Livro1 e Livro2 possuem o mesmo autor*/
mesmo_autor(Livro1,Livro2):-
    distinct(
        	[Livro1,Autor,Livro2],
        	(livros_de_fantasia(Livro1,Autor,_,_),livros_de_fantasia(Livro2,Autor,_,_))
        	), 
    dif(Livro1,Livro2).

/*Livro1 e Livro2 possuem mesma publicadora*/
mesma_publicadora(Livro1,Livro2):-
    distinct(
        	[Publicadora,Livro1,Livro2], 
        	(publicadora_de(Publicadora,Livro1),publicadora_de(Publicadora,Livro2)
        	)),
    dif(Livro1,Livro2).

/*Livro foi republicado: Possui mais de 1 ano de publicacao
 * */
republicado(Livro):-
    distinct([Livro], (livros_de_fantasia(Livro,_,_,_))),
    ano_do_livro(Ano1,Livro) , ano_do_livro(Ano2,Livro),
    Ano1 @> Ano2.
%livro pode aparecer varias vezes por ter sido republicado muitas vezes


/**Sobre o ano
 *
 *
 *
 *
 * ***/

/*Ano em que o Livro foi publicado */
ano_do_livro(Ano, Livro):-
    distinct([Livro,Ano], (livros_de_fantasia(Livro,_,Ano,_))).



/*Ano e a sua lista de livros*/
ano_lista_de_livros(Ano,Lista_de_livros):-
    bagof(Livro,
          distinct([Ano,Livro], (ano_do_livro(Ano,Livro))),
          Lista_de_livros).


/*Ano e a sua quantidade de livros lancado*/
ano_com_livros(Ano,Count):-
    distinct([Ano], (ano_do_livro(Ano,_))),
    aggregate_all(count, (ano_do_livro(Ano, _)), Count).


/*Ano em que teve mais de 5 livros*/
ano_concorrido(Ano):-
    ano_com_livros(Ano,Count), Count @> 5.


/*Lista de anos de publicacao de um livro*/
livro_anos_de_publicacao(Livro, Lista):-
    bagof(Ano,
          (distinct([Livro,Ano], (republicado(Livro), ano_do_livro(Ano,Livro))) ),
          Lista).

% livro_anos_de_publicacao("The Lord of the Rings", Lista).
% livro_anos_de_publicacao(Livro, [2007|_]).

% acima nao eh uma consulta muito boa pois necessita que 2007 seja o cabeca da lista
% mas eh uma consulta boa

/**Sobre a publicadora
 *
 *
 *
 *
 * ***/

/* É Publicadora do Livro*/
publicadora_de(Publicadora, Livro):-
	distinct(
        [Livro,Publicadora], 
        (livros_de_fantasia(Livro, _,_,Publicadora))
        ),
    dif(Publicadora, '$null$').

/*Lista de livros da Publicadora*/
publicadora_com_livros(Publicadora, Lista_de_livros):-
    bagof(Livro,publicadora_de(Publicadora,Livro),Lista_de_livros).

 
/*Lista de autores que tiveram livro na Publicadora*/
publicadora_com_autores(Publicadora, Lista_de_autores):-
    bagof(Autor,
          distinct([Autor,Publicadora], (autor_fez_publicadora(Autor,Publicadora))),
          Lista_de_autores),
    dif(Publicadora, '$null$').

/*Publicadora com quantidade de livros*/
publicadora_quantidade_de_livros(Publicadora,Count):-
    publicadora_com_livros(Publicadora,Lista_de_livros),
    proper_length(Lista_de_livros,Count).

/*Publicadora que possui mais de 7 livros*/
publicadora_famosa_por_livros(Publicadora):-
    publicadora_quantidade_de_livros(Publicadora,Count), Count @>7.

/*Publicadora com quantidade de autores em contato com ela*/
publicadora_quantidade_de_autores(Publicadora,Count):-
    publicadora_com_autores(Publicadora,Lista_de_autores),
    proper_length(Lista_de_autores,Count).

/*Publicadora com mais de 4 autores em que pediram
 * pra publicar seus livros*/
publicadora_famosa_entre_autores(Publicadora):-
    publicadora_quantidade_de_autores(Publicadora,Count), Count @>4.



/** <examples>
?- autor_de(Autor,_).
?- autor_de("Terry Pratchett", X).
?- autor_com_livros("Terry Pratchett", Lista_de_livros).
?- autor_bem_sucedido(Autor, Count).

?- republicado(Livro).
?- mesma_publicadora(Livro1,Livro2).
?- mesma_publicadora( "Pyramids",Livro2).

?- ano_com_livros(Ano,6).
?- ano_lista_de_livros(Ano,Lista_de_livros).
?- ano_do_livro(Ano, _).
?- livro_anos_de_publicacao(Livro, Lista).

?- publicadora_com_livros(Publicadora, Lista_de_livros).
?- publicadora_famosa_por_livros(Publicadora).
?- publicadora_com_autores(Publicadora, Lista_de_autores).
*/