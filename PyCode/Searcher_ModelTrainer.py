# -*- coding: utf-8 -*-
"""
Created on Fri May 19 13:00:16 2023

@author: Li Chao
"""

from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import layers
from transformers import TFBertModel

class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1, 
                 name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.rate = rate
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)
        

    def get_config(self):
        config = super().get_config()
        config.update({
            'embed_dim': self.embed_dim,
            'num_heads': self.num_heads,
            'ff_dim': self.ff_dim,
            'rate': self.rate
        })
        return config    

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)


class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim, 
                 name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions

def getTransformerModelBert(maxlen = 60, 
                            num_heads = 8, ff_dim = 32, y_categories = 2,
                            *args, **kwargs):
    """
    

    Parameters
    ----------
    vocab_size : TYPE, optional
        DESCRIPTION. The default is 20000.
    maxlen : TYPE, optional
        DESCRIPTION. The default is 60.
    embed_dim : TYPE, optional
        DESCRIPTION. The default is 32.
    num_heads : TYPE, optional
        DESCRIPTION. The default is 8.
    ff_dim : TYPE, optional
        DESCRIPTION. The default is 32.

    Returns
    -------
    model : Model object
        A transformer model to labal the text.

    """
    model_name = 'bert-base-uncased'
    #tokenizer = BertTokenizer.from_pretrained(model_name)
    bert_model = TFBertModel.from_pretrained(model_name)
    bert_model.trainable = False
    
    input_ids = layers.Input(shape=(maxlen,), dtype=tf.int32, name='input_ids')
    embeddings = bert_model(input_ids)[0]
    embed_dim = bert_model.config.hidden_size
    transformer_block = TransformerBlock(embed_dim, num_heads, ff_dim)
    x = transformer_block(embeddings)
    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dropout(0.1)(x)
    x = layers.Dense(20, activation="relu")(x)
    x = layers.Dropout(0.1)(x)
    outputs = layers.Dense(y_categories, activation="softmax")(x)

    model = keras.Model(inputs=input_ids, outputs=outputs)
    model.summary()
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model

def Searcher_ModelTrainer(DataX, DataY, maxlen = 60, 
                          num_heads = 8, ff_dim = 32, y_categories = 2,
                          loss = "sparse_categorical_crossentropy",
                          train_test_split_rate = 0.1, 
                          batch_size=32, epochs=20, patience=5, verbose = 1,
                          *args, **kwargs):
    """
    

    Parameters
    ----------
    DataX : list
        input X dataset to train model.
    DataY : list
        input Y dataset to train model.
    maxlen : TYPE, optional
        DESCRIPTION. The default is 60.
    num_heads : TYPE, optional
        DESCRIPTION. The default is 8.
    ff_dim : TYPE, optional
        DESCRIPTION. The default is 32.
    train_test_split_rate : TYPE, optional
        DESCRIPTION. The default is 0.1.
    batch_size : TYPE, optional
        DESCRIPTION. The default is 32.
    epochs : TYPE, optional
        DESCRIPTION. The default is 20.
    patience : TYPE, optional
        patience for model training. The default is 5.

    Returns
    -------
    model : Model object
        this is the trained model.

    """
    X_train, X_val, y_train, y_val = train_test_split(DataX, DataY, 
                                                      test_size=train_test_split_rate, 
                                                      random_state=42)
    model = getTransformerModelBert( maxlen = maxlen, num_heads = num_heads,
                                    ff_dim = ff_dim, y_categories = y_categories,
                                    *args, **kwargs)
    model.compile(optimizer="adam", loss=loss, metrics=["accuracy"])
    early_stop = EarlyStopping(monitor='val_loss', patience=patience, verbose=1,
                               mode='min', restore_best_weights=True)
    model.fit(
        X_train, y_train, batch_size=batch_size, epochs=epochs,
        validation_data=(X_val, y_val), callbacks=[early_stop], 
        verbose = verbose
    )
    return model