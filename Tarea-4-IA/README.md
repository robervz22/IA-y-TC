perceptron.py: Aquí se encuentra implementada la red neuronal con una capa oculta y la versión propia del backpropagation.

Class perceptron: 

1. _init_: Inicializa las variables de la clase. Recibe el conjunto de entrenamiento, un arreglo con las longitudes de la capa inicial, oculta y de salida además del número máximo de épocas.

2. forward(X): Recibe el vector X, actualiza el input y output de cada neurona. 

3.  backpropagation(Y): Dada la rutina anterior, calcula los errores utilizando el algoritmo backpropagation, actualiza los pesos y el vector de bias. 

4. output_value(X): Es la salida de la neurona de la capa de salida, es un valor entre 0 y 1 pues se utiliza la función sigmoide. 

5. class_value(X): De acuerdo a el valor de salida de la red si es mayor o igual a 0.5 lo etiqueta como de la clase positiva y se es menor a 0.5 como de la clase negativa. 

4. train(): Entrena a la red e imprime los resultados que se piden en los numerales de la tarea. 

5. test(X_test,y_test): Hace la clasificación de los valores X_test e imprime las métricas que se piden en la tarea

6. report_parameters(): Reporta los pesos de la red, el término de bias de la capa escondida y de salida, el número de parámetros totales. 

Tarea_4_IA.ipynb: 
Este es el notebook de Jupyter. Aquí se utiliza el archivo perceptron.py para utilizar las funciones anteriores de forma mas concisa. Aquí se hacen las observaciones y las visualizaciones correspondientes.

Tarea_4_IA.pdf:
Versión pdf del notebook de Jupyter para mayor portabilidad.

train.csv: Este es el conjunto de entrenamiento que se genera con una semilla específica y que te utiliza para el entrenamiento de ambos métodos.

test.csv: El conjunto de validación que se utiliza para ambos métodos.