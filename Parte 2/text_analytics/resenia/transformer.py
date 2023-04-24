from sklearn.base import BaseEstimator, TransformerMixin
# Detectar el lenguaje en el que está escrito
from langdetect import detect

# Instalación de librerias
import pandas as pd
from joblib import dump, load

# Estadística descriptiva
from scipy import stats as st

# Procesamiento de texto
import re
import unicodedata
from nltk import word_tokenize
from nltk.corpus import stopwords
from num2words import num2words
import spacy




class TextPreProcessing(BaseEstimator, TransformerMixin):
    lista_data = {}

    def __init__(self):
        print('Preprocesamiento')

    # =========================== Pre Procesamiento con los datos =========================== #
    def delete_null(self, df: pd.DataFrame):
        """
        Función que elimina los datos nulos 

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame al que se le realizan los cambios

        Returns
        -------
            DtaFrame: DataFrame transformado 
        """
        reviews = []
        df = df[df['review_es'].notna()]
        df = df.reset_index(drop=True)
        df_ = df.apply(lambda x: x.str.strip())

        for i in range(len(df_['review_es'])):
            if (df_['review_es'][i] == ''):
                df_ = df_.drop(df_.index[[i]])
            else:
                pass
        df_ = df_.reset_index(drop=True)
        df = df_

        return df

    def duplicates(self, df: pd.DataFrame):
        """
        Función que elimina los duplicados 

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame al que se le realizan los cambios

        Returns
        -------
            DtaFrame: DataFrame transformado 
        """
        if (df.duplicated(subset='review_es', keep=False).sum() != 0):
            df = df.drop_duplicates(
                subset='review_es', keep='first', inplace=True)
        return df

    def deleteDiferents(self, df: pd.DataFrame, lan: str):
        """
        Función que elimina los valores que no estén en el idioma indicado 

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame al que se le realizan los cambios

        Returns
        -------
            DtaFrame: DataFrame transformado 
        """
        return df[df['Language'] == lan]

    # =========================== Transformación de los datos =========================== #
    def remove_non_ascii(self, words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode(
                'ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    def to_lowercase(self, words):
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

    def remove_punctuation(self, words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', ' ', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def replace_numbers(self, words):
        """Replace all interger occurrences in list of tokenized words with textual representation"""
        new_words = []

        for word in words:
            new_word = re.findall('(\d+)', word)
            if new_word == []:
                new_words.append(word)
            else:
                new_word = new_word[0]
                new_word = num2words(int(new_word), lang='es')
                new_words.append(new_word)

        return new_words

    def remove_stopwords(self, words):
        """Remove stop words from list of tokenized words"""
        stop_words = set(stopwords.words('spanish'))
        new_words = []
        for word in words:
            if (word not in stop_words):
                new_words.append(word)
        return new_words

    def remove_blank_space(self, words):
        new_words = []
        for word in words:
            if (word != " "):
                new_words.append(word)
            else:
                None
        return new_words

    def preprocessing(self, words):
        words = self.to_lowercase(words)
        words = self.replace_numbers(words)
        words = self.remove_punctuation(words)
        words = self.remove_non_ascii(words)
        words = self.remove_blank_space(words)
        words = self.remove_stopwords(words)
        return words

    def stem_lematizer_words(self, words):
        new_words = []

        spl = spacy.load("es_core_news_sm")

        new_word = spl(words)
        for token in new_word:
            new_words.append(token.lemma_)

        return new_words

    def fit(self, df, y=None, lista_data=lista_data):
        print('Descripción del conjunto de datos')
        print('Filas: {}'.format(df.shape[0]))
        lista_data['filas']=df.shape[0]
        lista_data['columnas'] = df.shape[1]
        return self

    def transform(self, df, lista_data=lista_data):

        print(
            '\n' + '\033[1m' + 'Paso 1: Comprobar que no se tengan columnas nulas o sin contenido' + '\033[0m')
        print(
            str((df.isnull().sum() / df.shape[0]).sort_values(ascending=False)) + '\n')
        lista_data['nulos'] = (df.isnull().sum().to_list()[0])
        # Preprocesamiento
        print('\033[1m' + 'Paso 2: Eliminar filas con reseñas nulas' + '\033[0m')
        df = self.delete_null(df)
        print(
            str((df.isnull().sum() / df.shape[0]).sort_values(ascending=False)) + '\n')
        print(
            '\033[1m' + 'Paso 3: Comprobar que no se tengan duplicados' + '\033[0m')
        print('Se tienen {} duplicados '.format(
            df.duplicated(subset='review_es', keep=False).sum()) + '\n')
        lista_data['duplicados']=(df.duplicated(subset='review_es', keep=False).sum())
        print(
            '\033[1m' + 'Paso 4: Eliminar las reseñas que se encuentren duplicadas' + '\033[0m')
        df = self.duplicates(df)
        print(
            '\033[1m' + 'Paso 5: Identificar los idiomas que se encuentran en el conujnto de reseñas' + '\033[0m')
        df['Language'] = [detect(x) for x in df['review_es']]
        lista_data['idiomas'] = (df['Language'].value_counts().to_dict())
        print(str(df['Language'].value_counts()) + '\n')
        print(
            '\033[1m' + 'Paso 6: Seleccionar las filas que contiene las reseñas en español' + '\033[0m')
        df = self.deleteDiferents(df, 'es')
        print(str(df['Language'].value_counts()) + '\n')

        # Transformación de las palabras
        print('\033[1m' + 'Paso 7: Tokenización' + '\033[0m')
        # Crear columna con palabras tokenizadas
        df['palabras'] = df['review_es'].apply(
            word_tokenize).apply(self.preprocessing)
        df['Tokenizado'] = df['palabras']
        print('\033[1m' + 'Paso 8: Lematización' + '\033[0m')
        df['palabras'] = df['palabras'].apply(lambda x: ' '.join(map(str, x)))
        df['palabras'] = df['palabras'].apply(self.stem_lematizer_words)
        print('\033[1m' + 'Paso 9: Arreglo final de datos' + '\033[0m')
        df['palabras'] = df['palabras'].apply(self.remove_stopwords)
        df['palabras'] = df['palabras'].apply(lambda x: ' '.join(map(str, x)))
        df['palabras'] = df['palabras'].apply(
            word_tokenize).apply(self.remove_stopwords)
        df['palabras'] = df['palabras'].apply(lambda x: ' '.join(map(str, x)))
        return [df['palabras'], lista_data]


def applyModel(filename: str, data):

    model = load(filename)
    y_predict = model.predict(data)
    df = pd.DataFrame({'review_es': data,
                       'Sentimiento': y_predict})
    df.loc[df['Sentimiento'] == 0, 'Sentimiento'] = 'Positiva'
    df.loc[df['Sentimiento'] == 1, 'Sentimiento'] = 'Negativa'
    df.to_csv('./resultados.csv', index=False)
    return df