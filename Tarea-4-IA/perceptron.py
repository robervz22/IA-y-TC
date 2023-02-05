import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score


'''
Network structure
'''
L_FACTOR=0.1 # Learning Factor
TOL_ERROR=0.05
# Sigmoid function
def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))

# Perceptron
class perceptron:
    ''' 
    Initialization
    '''
    def __init__(self,X_train,y_train,layer_lenghts,max_epochs):
        # Index for layers
        np.random.seed(22) # Seed for replication
        self.index_l0=np.arange(0,layer_lenghts[0])
        self.index_l1=np.arange(layer_lenghts[0],layer_lenghts[1]+layer_lenghts[0])
        self.index_l2=np.arange(layer_lenghts[0]+layer_lenghts[1],layer_lenghts[0]+layer_lenghts[1]+layer_lenghts[2])
        self.X_train=X_train
        self.y_train=y_train
        self.max_epochs=max_epochs
        self.output=np.empty(sum(layer_lenghts)) # Output of each neuron
        self.input=np.empty(sum(layer_lenghts))  # Input of eache neuron
        self.error=np.empty(sum(layer_lenghts))  # Error for each neuron
        # Random initialization of weights
        self.weights=np.random.uniform(-5,5,size=(sum(layer_lenghts),sum(layer_lenghts)))
        self.initial_weights=self.weights
        self.bias=np.random.uniform(-5,5,sum(layer_lenghts)) # Bias de a_0=-1, not for input layer
        self.initial_bias=self.bias
    '''
    Forward
    '''
    def forward(self,X):
        # Layer 0
        self.input[np.ix_(self.index_l0)]=X
        self.output[np.ix_(self.index_l0)]=X
        # Layer 1
        self.input[np.ix_(self.index_l1)]=self.output[np.ix_(self.index_l0)]@ self.weights[np.ix_(self.index_l0,self.index_l1)]-self.bias[np.ix_(self.index_l1)]
        self.output[np.ix_(self.index_l1)]=sigmoid(self.input[np.ix_(self.index_l1)])
        # Layer 2
        self.input[np.ix_(self.index_l2)]=self.output[np.ix_(self.index_l1)]@ self.weights[np.ix_(self.index_l1,self.index_l2)]-self.bias[np.ix_(self.index_l2)]
        self.output[np.ix_(self.index_l2)]=sigmoid(self.input[np.ix_(self.index_l2)])
    ''' 
    Backpropagation
    '''
    def backpropagation(self,Y):
        # Layer 2
        a=self.output[np.ix_(self.index_l2)]
        self.error[np.ix_(self.index_l2)]=a*(1.0-a)*(Y-a) # len(Y)==len(a)
        self.bias[np.ix_(self.index_l2)]=self.bias[np.ix_(self.index_l2)]-L_FACTOR*self.error[np.ix_(self.index_l2)]

        # Layer 1
        a=self.output[np.ix_(self.index_l1)]
        a_aux=a
        a_aux=a_aux[np.newaxis]
        delta=self.error[np.ix_(self.index_l2)]
        delta=delta[np.newaxis]
        tmp=self.weights[np.ix_(self.index_l1,self.index_l2)]@delta.T
        self.error[np.ix_(self.index_l1)]=a*(1.0-a)*(tmp.T)
        self.weights[np.ix_(self.index_l1,self.index_l2)]=self.weights[np.ix_(self.index_l1,self.index_l2)]+L_FACTOR*a_aux.T@delta
        self.bias[np.ix_(self.index_l1)]=self.bias[np.ix_(self.index_l1)]-L_FACTOR*self.error[np.ix_(self.index_l1)]

        # Layer 0
        a=self.output[np.ix_(self.index_l0)]
        a_aux=a
        a_aux=a_aux[np.newaxis]
        delta=self.error[np.ix_(self.index_l1)]
        delta=delta[np.newaxis]
        tmp=self.weights[np.ix_(self.index_l0,self.index_l1)]@delta.T
        self.error[np.ix_(self.index_l0)]=a*(1.0-a)*(tmp.T)
        self.weights[np.ix_(self.index_l0,self.index_l1)]=self.weights[np.ix_(self.index_l0,self.index_l1)]+L_FACTOR*a_aux.T@delta
    ''' 
    Perceptron Output Value
    '''
    def output_value(self,X):
        self.forward(X)
        return self.output[-1]
    ''' 
    Class value 
    '''
    def class_value(self,X):
        self.forward(X)
        value=self.output[-1]
        if value>=0.5:
            return 1.0
        else:
            return 0.0
    '''
    Training
    '''
    def train(self):
        num_iter=0
        MSE=10.0
        while MSE>TOL_ERROR and num_iter<self.max_epochs:
            # Training Part
            for X,y in zip(self.X_train,self.y_train):
                self.forward(X)
                self.backpropagation(y)
            # Computing de MSE            
            output_per_sample=np.array([self.output_value(X) for X in self.X_train])
            MSE=mean_squared_error(self.y_train,output_per_sample)
            num_iter+=1

        self.num_iter=num_iter
        train_output=np.array([self.output_value(X) for X in self.X_train])
        self.train_classes=np.array([self.class_value(X) for X in self.X_train])
        self.train_MSE=mean_squared_error(self.y_train,train_output)
        self.train_accuracy=accuracy_score(self.y_train,self.train_classes,normalize=False)
        self.train_accuracy_score=accuracy_score(self.y_train,self.train_classes)
        print('Numero de iteraciones para el conjunto de entrenamiento: %d' %(self.num_iter))
        print('MSE para el entrenamiento: %.4f' %(self.train_MSE))
        print('Numero de muestras bien clasificadas (Entrenamiento): %d' %(self.train_accuracy))
        print('Numero de muestras mal clasificadas  (Entrenamiento): %d' %(self.X_train.shape[0]-self.train_accuracy))
        print('Numero de muestras en el conjunto de entrenamiento: %d' %(self.X_train.shape[0]))
        print('Precision del entrenamiento: %.4f' %(self.train_accuracy_score))
    '''
    Test
    '''
    def test(self,X_test,y_test):
        test_output=np.array([self.output_value(X) for X in X_test])
        self.test_classes=np.array([self.class_value(X) for X in X_test])
        self.test_MSE=mean_squared_error(y_test,test_output)
        self.test_accuracy=accuracy_score(y_test,self.test_classes,normalize=False)
        self.test_accuracy_score=accuracy_score(y_test,self.test_classes)
        print('MSE para la validacion: %.4f' %(self.test_MSE))
        print('Numero de muestras bien clasificadas (Validacion): %d' %(self.test_accuracy))
        print('Numero de muestras mal clasificadas (Validacion): %d' %(X_test.shape[0]-self.test_accuracy))
        print('Numero de muestras en el conjunto de validacion: %d' %(X_test.shape[0]))
        print('Precision en la validacion: %.4f' %(self.test_accuracy_score))
    ''' 
    Report Parameters
    '''
    def report_parameters(self):
        print('Los pesos de la capa inicial a la capa oculta son:')
        print(self.weights[np.ix_(self.index_l0,self.index_l1)])
        print('\n')
        print('Los pesos de la capa oculta a la capa de salida son:')
        print(self.weights[np.ix_(self.index_l1,self.index_l2)])
        print('\n')
        print('El coeficiente asociado al bias para cada neurona de la capa oculta es: ')
        print(self.bias[np.ix_(self.index_l1)])
        print('\n')
        print('El coeficiente asociado al bias para cada neurona de la capa de salida es: ')
        print(self.bias[np.ix_(self.index_l2)])
        print('\n')
        self.num_parameters=len(self.index_l0)*len(self.index_l1)+len(self.index_l1)*len(self.index_l2)+len(self.index_l1)+len(self.index_l2)
        print('Numero de parametros contando el bias: %d' %(self.num_parameters))


