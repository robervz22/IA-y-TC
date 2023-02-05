blind_search.py: En este archivo se encuentra implementada la búsqueda en anchura (BFS) y profundidad (DFS) en clases. Cada clase tiene cada una de las siguientes funciones 

1. _init_ : Inicializa las variables de la clase

2. get_InvCount: Cuenta el número de inversiones respecto a la configuración [1,2,3,4,5,6,7,8,0] (en forma de lista). 
Una inversión en una configuración 'conf' será cuando en posiciones de arreglo i,j con i menor j se tenga conf[i] es mayor que conf[j], sin considerar el número que representa la cadena vacía. 

3. isSolvable(puzzle): Verifica si a partir del 'puzzle' se puede llegar al final, para ello analiza la paridad el número de inversiones de cada tablero. Si el tablero final es alcanzable, la paridad del número de inversiones para cada tablero debe ser la misma. 

4. get_succesors(current_state): Obtiene los hijos de un nodo dado considerando el orden 'down', 'up', 'left' y 'right'.

5. deal_repetitions(sons): Elimina de la lista sons las repeticiones de nodos que ya se han visitado (closed_states) o expandido (open_states).

6. append_open(sons): Agrega la lista sons a la lista de abiertos (open_states) siguiente el paradigma de cola en BFS y pila en DFS.

7. main(): Función que valida primero si la configuración final es alcanzable a partir de la inicial. Si es alcanzable imprime la solución, el número de pasos, los nodos visitados (closed_states), los nodos por visitar (open_states) y el número de nodos en el grafo (open_states+closed_states).

En DFS
8. depth(current_state): Obtiene la profundidad en donde está ubicado el estado current_state. Esta función nos permite dar un límite de profunidad.

Tarea_2_IA.ipynb:

En este archivo se encuentra lo que se solicita en la tarea. Utilizamos al archivo blind_search.py como módulo importado para mayor claridad. En este archivo discutimos las observaciones pertinentes a los algoritmos de búsqueda.

Tarea_2_IA.pdf

Es la versión pdf del notebook de Jupyter. 