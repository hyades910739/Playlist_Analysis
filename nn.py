import tensorflow
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Input, MaxPooling1D, Convolution1D, Embedding, Activation
from keras import regularizers
from sklearn.model_selection import train_test_split
import pandas as pd
import os

def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    y = pd.read_csv("music2vec50.csv",index_col=0)
    df = pd.read_csv("song_feature_32403",index_col=0)
    df = df.drop(columns=['id','track','artist'])
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.05, random_state=42)
    model_input = Input(shape=(14,))
    z = Dense(500, activation="relu")(model_input)
    z = Dropout(0.5)(z)
    z = Dense(400, activation="relu")(z)          
    z = Dropout(0.5)(z)
    z = Dense(300, activation="relu")(z)          
    z = Dropout(0.5)(z)
    model_output = Dense(100, activation="linear",kernel_regularizer=regularizers.l2(0.001))(z)
    model = Model(model_input,model_output)
    model.summary()
    model.compile(loss='mse', optimizer='adam',metrics=['mse'])
    model.fit(X_train, y_train, epochs=30,batch_size=100)
    score = model.evaluate(X_test, y_test)
    #print('test acc: ', score[1])
    print(model.metrics_names,score)

if __name__ == '__main__':
    main()
