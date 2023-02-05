heuristic_search.py: En este archivo se encuentra implementada la búsqueda con heurística a través del algoritmo A* en una clase A_star.  

Clase A_star

1. _init_ : Inicializa las variables de la clase

2. get_InvCount: Cuenta el número de inversiones respecto a la configuración [1,2,3,4,5,6,7,8,0] (en forma de lista). 
Una inversión en una configuración 'conf' será cuando en posiciones de arreglo i,j con i menor j se tenga conf[i] es mayor que conf[j], sin considerar el número que representa la cadena vacía. 

3. isSolvable(puzzle): Verifica si a partir del 'puzzle' se puede llegar al final, para ello analiza la paridad el número de inversiones de cada tablero. Si el tablero final es alcanzable, la paridad del número de inversiones para cada tablero debe ser la misma. 

4. get_succesors(current_state): Obtiene los hijos de un nodo dado considerando el orden 'down', 'up', 'left' y 'right'.

5. deal_repetitions(sons): Elimina de la lista sons las repeticiones de nodos que ya se han visitado (closed_states) o expandido (open_states).

6. append_open(sons): Agrega la lista sons a la lista de abiertos (open_states) siguiente el paradigma de cola en BFS y pila en DFS.

7. get_better(dist_func): Recibe como argmuneto la función distancia que se considerará. Obtiene de la lista de abiertos el nodo expandido con menor costo.

8. main(dist): Función que valida primero si la configuración final es alcanzable a partir de la inicial. Si es alcanzable imprime la solución, el número de pasos, los nodos visitados (closed_states), los nodos por visitar (open_states) y el número de nodos en el grafo (open_states+closed_states).

Funciones y clases extras

1. depth(current_state): Obtiene la profundidad en donde está ubicado el estado current_state. Esta función nos permite dar un límite de profunidad.

2. node: Clase nodo, contiene el valor del tablero, el costo y la profundidad a la que está del árbol

3. print_dashboard(A): Imprime el tablero que se pasa como argumento.

4. is_equal(A,B): Regresa una variable de tipo bool. Nos dice si dos configuraciones son iguales.

Distancias

1. Manhattan_dist(current_value,final_value): Calcula la distancia Manhattan entre current_value y final_value

2. Counting_dist(current_value, final_value): Cálcula la distancia de Hamming de current_value respecto a final_value, es decir, el número de fichas en posición errónea. 

3. Inversion_dist(current_value,final_value): Calcular el número de inversiones de current_value y final_value. Regresa la diferencia absoluta. 




Tarea_3_IA.ipynb:

En este archivo se encuentra lo que se solicita en la tarea. Utilizamos al archivo blind_search.py como módulo importado para mayor claridad. En este archivo discutimos las observaciones pertinentes a los algoritmos de búsqueda.

Tarea_3_IA.pdf

Es la versión pdf del notebook de Jupyter. 