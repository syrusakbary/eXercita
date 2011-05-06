# -*- coding: utf-8 -*-
import sys
from plasTeX.TeX import TeX
from plasTeX.Renderers.XHTML import Renderer

exercise = u'''\begin{document}
\exer{exercise}
a
\exer{title}
  Máximos y mínimos
\exer{/title}

\exer{requires}
  \exer{format}{LaTeX}
  \exer{package}{[spanish]babel}
  \exer{package}{[latin1]inputenc}
  \exer{package}{codex}
\exer{/requires}

\exer{statement}
 \exer{text}
  Se dispone de varias secuencias de números enteros, y se desea
  hallar el mínimo de los máximos elementos de las secuencias.
  Por ejemplo, para las secuencias siguientes,
  \begin{center}\begin{tabular}{l}
     16, 49, 21, 2, 58, 15; \\
     50, 71, 23, 40, 81, 34, 23, 75; \\
     23, 53, 25, 15; \\
     45, 90, 12
  \end{tabular}\end{center}
  los máximos son, respectivamente, 58, 81, 53, 90, y el mínimo
  de ellos es 53.

  Lo que se pide es un procedimiento para ese cálculo, suponiendo que
  los datos están consignados en una lista de listas.
 \exer{/text}
\exer{/statement}

\exer{solution}{solImperativa}
 \exer{text}
   Se van a dar dos soluciones, una siguiendo literalmente el procedimiento
   descrito y otra, más eficiente, basada en una interesante
   observación. Ambas soluciones operan con una lista de listas de enteros,
   que se define como sigue:
   \exer{conditional}
     \exer{case}{value{language}{C++}}
\begin{codex}[C++]
typedef struct NodoEntero {
  int inf;
  NodoEntero* sig;
} NodoEntero;
typedef NodoEntero* ListaEnteros;

typedef struct NodoLista {
  ListaEnteros inf;
  NodoLista* sig;
} NodoLista;
typedef NodoLista* ListaListas;
\end{codex}
     \exer{/case}
     \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
  TYPE
    tPuntListaEnteros = ^tNodoEntero;
    tNodoEntero = RECORD
      inf: integer;
      sig: tPuntListaEnteros
    END; {tNodoEntero}
    tPuntListaListas = ^tNodoLista;
    tNodoLista = RECORD
      inf: tPuntListaEnteros;
      sig: tPuntListaListas
    END; {tPuntListaListas}
\end{codex}       
     \exer{/case}
     \exer{default}
       \exer{error}{Lenguaje NO definido}
     \exer{/default}
   \exer{/conditional}
   No debemos olvidar los procedimientos para liberar la memoria dinámica:
   escribiremos uno para las listas de enteros y otro para las listas de listas:\\
   \exer{conditional}
     \exer{case}{value{language}{C++}}
\vbox{%
\begin{codex}[C++]
void liberar(ListaEnteros& lista) {
  NodoEntero* actual = lista;
  while (actual != NULL) {
    NodoEntero* aux = actual;
    actual = actual->sig;
    delete aux;
  }
  lista = NULL;
}

void liberar(ListaListas& lista) {
  NodoLista* actual = lista;
  while (actual != NULL) {
    NodoLista* aux = actual;
    actual = actual->sig;
    liberar(aux->inf);
    delete aux;
  }
  lista = NULL;
}
\end{codex}       
}
     \exer{/case}
     \exer{case}{value{language}{Pascal}}
       \exer{error}{Esto no esta escrito}
     \exer{/case}
     \exer{default}
       \exer{error}{Lenguaje NO definidio}
     \exer{/default}
   \exer{/conditional}
   

  \exer{section}{Solución primera, ineficiente}
    Una primera solución consiste sencillamente en seguir literalmente
    el método descrito: recorrer completamente 
    todas las secuencias
    hallando sus máximos, y seleccionar el mínimo entre ellos.
\begin{codex}[C++]
[[Se parte de un mínimo ficticio, |minimo| = ``infinito'']]
while ([[queden listas]]) {
  [[Hallar el elemento máximo de una lista, |maximo|]]
  if ([[|maximo| $<$ |minimo|]]) {
    [[se sustituye el valor de |minimo| por el de |maximo|]]
  }
}
\end{codex}
 El procedimiento se puede expresar con pocos detalles técnicos:
    \exer{conditional}
      \exer{case}{value{language}{C++}}
\begin{codex}[C++]
int maxMin(ListaListas const lista) {
  int minimo = INT_MAX;
  ListaListas auxLista = lista;
  while (auxLista != NULL) {
    int maximo = maximoLista(auxLista->inf);
    if (maximo < minimo) minimo = maximo;
    auxLista = auxLista->sig;
  }
  return minimo;
}        
\end{codex}
      \exer{/case}
      \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
  FUNCTION maxMin ({in} lista: tPuntListaListas): integer;
    VAR
      minimo,                        {de cada fila}
      maxFila: integer;              {de los máximos de las filas}
      listaListas: tPuntListaListas; {para recorrer la lista}
  BEGIN
    minimo := MaxInt;
    listaListas := lista;
    WHILE listaListas <> NIL DO BEGIN
      maxFila := MaximoValor (listaListas^.inf);
      IF maxFila < minimo THEN
        minimo := maxFila;
      listaListas := listaListasAux^.sig
    End; {while}
    MaxMin := minimo
  END; {MaxMin}
\end{codex}        
      \exer{/case}
      \exer{default}
        \exer{error}{Lenguaje NO definidio}
      \exer{/default}
    \exer{/conditional}
    
\noindent
Finalmente, para terminar, queda por describir 
la función \begin{codex}[C++]maximoValor\end{codex},
que halla el máximo elemento de una lista de enteros:\\
    \exer{conditional}
      \exer{case}{value{language}{C++}}
\vbox{%
\begin{codex}[C++]
int maximoLista(ListaEnteros const lista) {
  int maximo = INT_MIN;
  ListaEnteros auxLista = lista;
  while (auxLista != NULL) {
    if (auxLista->inf > maximo) maximo = auxLista->inf;
    auxLista = auxLista->sig;
  }
  return maximo;  
}
\end{codex}
}
      \exer{/case}
      \exer{case}{value{language}{Pascal}}    
\begin{codex}[Pascal]
  FUNCTION maximoValor ({in} lista: tPuntListaEnteros): integer;
    VAR
      maximo: integer;
      listaAux: tPuntListaEnteros; {para recorrer la lista}
  BEGIN
    maximo := - MaxInt; {valor ficticio inicial}
    listaAux := lista;
    WHILE listaAux <> NIL DO BEGIN
      IF listaAux^.inf > maximo THEN
        maximo := listaAux^.inf;
      lista := lista^.sig
    End; {while}
    MaximoValor := maximo
  END; {MaxMin}
\end{codex}        
        Como es natural, esta función se deberá incluir localmente a la
        función \begin{codex}[Pasca]maxMin\end{codex}.
      \exer{/case}
      \exer{default}
        \exer{error}{Lenguaje NO definidio}
      \exer{/default}
    \exer{/conditional}

  \exer{/section}
  
  \exer{section}{Solución eficiente, truncando la búsqueda}
    La solución dada puede mejorarse si se hace una observación algo
    sutil: con el ejemplo anterior, el máximo elemento de la primera
    secuencia es 58; o sea, que al repasar la segunda secuencia buscando
    el máximo, cuando se supere (o se iguale) el 58 (al encontrar el 71)
    no hará falta seguir, porque esta cantidad (u otra superior, como el 81,
    en el resto de esa secuencia) ya no podrá mejorar a 58 como mínimo de
    los máximos.
    
    Este hecho permite mejorar el programa cambiando la función
    \begin{codex}[C++]maximoValor\end{codex} (de una lista) por otra que, dada
    una \begin{codex}[C++]lista\end{codex} de enteros y un entero (\begin{codex}[C++]z\end{codex}), 
    halla directamente
    \emph{el mínimo entre el entero z y el máximo entero de la lista},
    interrumpiendo la búsqueda cuando se sabe que va a ser infructuosa:


    \exer{conditional}
      \exer{case}{value{language}{C++}}
\begin{codex}[C++]
int minEntMaxLista(int const z, ListaEnteros const lista) {
  int maximo = INT_MIN;
  ListaEnteros auxLista = lista;
  while (auxLista != NULL && maximo < z) {
    if (auxLista->inf > maximo) maximo = auxLista->inf;
    auxLista = auxLista->sig;
  }
  return maximo < z ? maximo : z;
}
\end{codex}
      \exer{/case}
      \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
  FUNCTION minEntMaxLista
    ({in} z    : integer;
     {in} lista: tPuntListaEnteros): integer;
    VAR
      maximo: integer;
      listaAux: tPuntListaEnteros; {para recorrer la lista}
  BEGIN
    maximo := - MaxInt; {valor ficticio inicial}
    listaAux := lista;
    WHILE (listaAux <> NIL) AND (maximo < z) DO BEGIN
      IF listaAux^.inf > maximo THEN
        maximo := listaAux^.inf;
      lista := lista^.sig
    END {while}
      IF maximo < z THEN
        MaximoValor := maximo
      ELSE
        MaximoValor := z
  END; {MinEntMaxLista\}
\end{codex}        
      \exer{/case}
      \exer{default}
        \exer{error}{Lenguaje NO definidio}
      \exer{/default}
    \exer{/conditional}
    \noindent
    La mejora en la eficiencia se produce sustituyendo,
    en la función \begin{codex}[C++]maxMin\end{codex}, la llamada
    \exer{conditional}
      \exer{case}{value{language}{C++}}
\begin{codex}[C++]
maximoValor(auxLista->inf);
\end{codex}
      \exer{/case}
      \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
maximoValor (listaListas^.inf)}
\end{codex}        
      \exer{/case}
      \exer{default}
        \exer{error}{Lenguaje NO definidio}
      \exer{/default}
    \exer{/conditional}
    por esta otra:
    \exer{conditional}
      \exer{case}{value{language}{C++}}
\begin{codex}[C++]
minEntMaxLista(minimo, auxLista->inf);
\end{codex}
      \exer{/case}
      \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
minEntMaxLista (minimo,listaListas^.inf)
\end{codex}        
        así como las correspondientes definiciones locales de las funciones.
      \exer{/case}
      \exer{default}
        \exer{error}{Lenguaje NO definidio}
      \exer{/default}
    \exer{/conditional}
    
    Por otra parte, es sencillo comprobar que el resultado de la función
    anterior es siempre menor o igual que el entero $z$ de partida, con lo
    que sobra la comparación posterior:
    \exer{conditional}
      \exer{case}{value{language}{C++}}
\begin{codex}[C++]
    if (maxFila < minimo) [[...]]
\end{codex}
      \exer{/case}
      \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
    If maxFila < minimo Then ...
\end{codex}        
      \exer{/case}
      \exer{default}
        \exer{error}{Lenguaje NO definidio}
      \exer{/default}
    \exer{/conditional}
    De esta forma, el bucle \texttt{while} se simplifica del siguiente modo,
    \exer{conditional}
      \exer{case}{value{language}{C++}}
\begin{codex}[C++]
  while (auxLista != NULL) {
    minimo = minEntMaxLista(minimo, auxLista->inf);
    auxLista = auxLista->sig;
  }
\end{codex}
      \exer{/case}
      \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
  WHILE listaListas <> NIL DO BEGIN
    maxFila := minEntMaxLista (minimo, listaListas^.inf);
    listaListas := listaListasAux^.sig
  END; {while}
\end{codex}        
      \exer{/case}
      \exer{default}
        \exer{error}{Lenguaje NO definidio}
      \exer{/default}
    \exer{/conditional}
    y la función \begin{codex}[C++]maxMin\end{codex} queda finalmente así:\\
    \exer{conditional}
      \exer{case}{value{language}{C++}}
\vbox{%
\begin{codex}[C++]
int maxMin(ListaListas const lista) {
  int minimo = INT_MAX;
  ListaListas auxLista = lista;
  while (auxLista != NULL) {
    minimo = minEntMaxLista(minimo, auxLista->inf);
    auxLista = auxLista->sig;
  }
  return minimo;
}
\end{codex}
}
      \exer{/case}
      \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
  FUNCTION maxMin ({in} lista: tPuntListaListas): integer;
    VAR
      minimo,            {de cada fila}
      maxFila : integer; {de los máximos de las filas}
      listaListas: tPuntListaListas; {para recorrer la lista}
  BEGIN
    minimo := MaxInt;
    listaListas := lista;
    WHILE listaListas <> NIL DO BEGIN
      minimo := MinEntMaxLista (minimo, listaListas^.inf);
      listaListas := listaListasAux^.sig
    END; {while}
    maxMin := minimo
  END; {MaxMin}
\end{codex}        
      \exer{/case}
      \exer{default}
        \exer{error}{Lenguaje NO definidio}
      \exer{/default}
    \exer{/conditional}    
\exer{/section}

        \exer{conditional}
          \exer{case}{defined{en-libro}}
          \exer{/case}
          \exer{default}
\exer{section}{Ejercicios suplementarios}
   \begin{enumerate}
   \item Como el único uso de la función
   \begin{codex}[C++]minEntMaxLista\end{codex} 
   sirve para modificar la variable \begin{codex}[C++]maxFila\end{codex}, 
   la asignación
     \exer{conditional}
       \exer{case}{value{language}{C++}}
\begin{codex}[C++]
minimo = minEntMaxLista(minimo, auxLista->inf);
\end{codex}
       \exer{/case}
       \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
minimo := minEntMaxLista (minimo, listaListas^.inf)
\end{codex}         
       \exer{/case}
       \exer{default}
         \exer{error}{Lenguaje NO definidio}
       \exer{/default}
     \exer{/conditional}
     se puede reemplazar por una llamada a procedimiento
     \exer{conditional}
       \exer{case}{value{language}{C++}}
\begin{codex}[C++]
hallarMinEntMaxLista (minimo, listaListas->inf)         
\end{codex}
       \exer{/case}
       \exer{case}{value{language}{Pascal}}
\begin{codex}[Pascal]
hallarMinEntMaxLista (minimo, listaListas^.inf)
\end{codex}         
       \exer{/case}
       \exer{default}
         \exer{error}{Lenguaje NO definidio}
       \exer{/default}
     \exer{/conditional}
     Efectúa las modificaciones descritas.

   \item La función desarrollada no puede comprobarse sin un
     programa que le proporcione una lista de listas que
     inspeccionar.
     Desarrolla un subprograma apropiado para ello, que capte
     unas cuantas líneas de la entrada estándar y, con ellas,
     construya la correspondiente estructura.
     
   \item También tiene interés medir experimentalmente
     la ganancia de tiempo lograda por la mejora.
     Para ello, se describen dos útiles:
     \begin{enumerate}
     \item Insertar un par de contadores para tantear el
       número de enteros de las listas y el de los
       revisados por el procedimiento mejorado.
       La diferencia entre ambos representa el ahorro
       neto obtenido; y el cociente entre esa diferencia
       y el tama\~no de la estructura inicial es el
       ahorro relativo.
     \item En vez de un programa que lee de la entrada estándar
       la lista de listas, esta estructura se puede
       generar aleatoriamente,
       eligiendo al azar la
       cantidad de listas, el tama\~no de cada una de
       ellas y cada uno de sus elementos.
     \end{enumerate}
     De este modo, se puede repetir el experimento un gran número
     de veces.
     
     Se propone incluir estas mejoras para averiguar la ganancia
     media relativa.
   \end{enumerate}
\exer{/section}
          \exer{/default}
        \exer{/conditional}
\exer{/text} 
\exer{/solution}

\exer{bibliography}
  \exer{text}
    El enunciado de este ejercicio
    (tomado de~\cite{AlphaBetaAlgorithm-Bird-Hughes})
    tiene una generalización conocida para trabajar con listas de listas
    de listas\ldots, invirtiendo la elección: máximo, mínimo, máximo, etc.
    Esta generalización se llama \emph{minimax} (o \emph{maximín}), y su
    campo de aplicación son los juegos: un jugador debe escoger el mejor
    movimiento, teniendo en cuenta que, seguidamente, el otro jugador 
    realizará el movimiento más ventajoso para él y por tanto el más 
    perjudicial para el primer jugador.
    En la solución de este ejercicio se propone una mejora para truncar 
    la búsqueda que recibe el nombre de \emph{poda alfa-beta}, 
    y puede consultarse en libros especializados en algoritmos,
    como~\cite{EstructuraDatosAlgoritmos-Aho-Hopcroft-Ullman,FundamentosAlgoritmia-Brassard-Bratley,IntroductionAlgorithmsCreative-Manber,Algorithms-Sedgewick}.
  \exer{/text}
\exer{/bibliography}


\exer{/exercise}
\end{document}
'''

exercise = '''\documentclass[12pt]{article}
\usepackage{lingmacros}
\usepackage{tree-dvips}
\begin{document}


Don't forget to include examples of topicalization.
They look like this:

{\small
\enumsentence{Topicalization from sentential subject:\\ 
\shortex{7}{a John$_i$ [a & kltukl & [el & 
  {\bf l-}oltoir & er & ngii$_i$ & a Mary]]}
{ & {\bf R-}clear & {\sc comp} & 
  {\bf IR}.{\sc 3s}-love   & P & him & }
{John, (it's) clear that Mary loves (him).}}
}


I'll just assume a tree structure like (\ex{1}).

{\small
\enumsentence{Structure of A$'$ Projections:\\ [2ex]
\begin{tabular}[t]{cccc}
    & \node{i}{CP}\\ [2ex]
    \node{ii}{Spec} &   &\node{iii}{C$'$}\\ [2ex]
        &\node{iv}{C} & & \node{v}{SAgrP}
\end{tabular}
\nodeconnect{i}{ii}
\nodeconnect{i}{iii}
\nodeconnect{iii}{iv}
\nodeconnect{iii}{v}
}
}


Mood changes when there is a topic, as well as when
there is WH-movement.  \emph{Irrealis} is the mood when
there is a non-subject topic or WH-phrase in Comp.
\emph{Realis} is the mood when there is a subject topic
or WH-phrase.

\end{document}
'''
exercise = u'\\begin{document}\\exer{exercise}\r\n\\exer{title} Un dibujo de Escher\r\n\\exer{/title} \\exer{requires}\r\n\\exer{format}{latex} \\exer{package}{[T1]fontenc} \\exer{package}{[latin1]inputenc} \\exer{package}{[spanish]babel} \\exer{package}{evenmoreverb} \\exer{package}{graphicx}\r\n\\exer{/requires} \\exer{statement} \\exer{text}\r\nObserva el dibujo de M.\\ C.\\ Escher (1898--1972) que aparece en la figura~\\exer{latexref}{cachivache} titulado \\emph{Wentelteefje}. \\begin{figure}[ht]\r\n\\begin{center} \\exer{resource}{cachivache.eps.gz}{\\scalebox{0.6}{\\includegraphics{#}}} \\caption{\\emph{Wentelteefje} de M.C. Escher} \\exer{latexlabel}{cachivache}\r\n\\end{center} \\end{figure}\r\nNo pretendemos en este ejercicio imitar la maestr\xeda de Escher al dibujar sus \\emph{animalillos-cachivache}, como \xe9l los llama, pero s\xed el texto que sirve de marco para la acci\xf3n de los mismos.\r\nEscribe un programa que lea los datos de un fichero de texto y los escriba en la pantalla siguiendo un patr\xf3n como el que muestra el dibujo de Escher. Ten en cuenta que hay varios par\xe1metros que considerar a la hora de definir el patr\xf3n.\r\n\\exer{/text} \\exer{hint}{pisParametros}\r\n\\exer{text} Los diversos par\xe1metros que pueden modificar el patr\xf3n de escritura son: el espacio en blanco inicial para la primera l\xednea; la anchura total de las l\xedneas; el n\xfamero de l\xedneas en blanco hasta que aparece la primera l\xednea a la izquierda; y el n\xfamero de caracteres en los que decrece o aumenta cada\r\n2.2\tPiezas y par\xe1metros\t2\tVISI\xd3N PANOR\xc1MICA CON EJEMPLOS\r\nl\xednea con respecto a \\exer{/text}\r\n\\exer{/hint} \\exer{example}{eje}\r\n\\exer{text} Aqu\xed podemos ver una que contiene los 123\r\n\\vbox{\\begin{center}\\strut \\begin{fittedverbatim}\r\nla anterior.\r\nejecuci\xf3n del programa que toma como entrada un fichero primeros d\xedgitos del n\xfamero $\\pi$:\r\n31415926535897932 384626433832795 0288419716939 93751058209 944592307 0628620 899862 80348 25342117\t067 9821480865\t1\r\n328230664709 \\end{fittedverbatim}\\relax \\end{center}}%vbox\r\n\\exer{/text} \\exer{/example} \\exer{/statement}\r\n\\exer{solution}{solPascal} \\exer{text}\r\n74 8164\r\n\\exer{development} Sin soluci\xf3n en Pascal\r\n\\exer{/development} \\exer{/text}\r\n\\exer{/solution} \\exer{/exercise}\\end{document}'

document = TeX().input(exercise)
document = document.parse()
renderer = Renderer()
print dir(renderer)
renderer.render(document)
