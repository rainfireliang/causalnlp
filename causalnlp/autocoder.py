# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_autocoder.ipynb (unless otherwise specified).

__all__ = ['Autocoder']

# Cell
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 500)
from .analyzers import ZeroShotClassifier

class Autocoder:
    """
    Autocodes text fields
    """
    def __init__(self, verbose=1):
        """
        Instantiates the Autocoder instance.
        """
        self.v = verbose
        self.zsl = ZeroShotClassifier()


    def _format_to_df(self, results, df):
        d = {}
        for e in results:
            if isinstance(e, dict): e = e.items()
            for tup in e:
                label = tup[0]
                prob = tup[1]
                lst = d.get(label, [])
                lst.append(prob)
                d[label] = lst
        new_df = df.join(pd.DataFrame(d, index=df.index))
        return new_df

    def _binarize_df(self, df, colnames, threshold=0.5):
        """
        Binarizes each column in `colnames` based on threshold.
        """
        for col in colnames:
            df[col] = (df[col] >= threshold).astype(int)
        return df

    def _check_columns(self, labels, df):
        """check columns"""
        cols = df.columns.values
        for l in labels:
            if l in cols:
                raise ValueError('There is already a column named %s in your DataFrame.' % (l))


    def code_sentiment(self, docs, df, batch_size=8, binarize=False, threshold=0.5):
        """
        Autocodes text for positive or negative sentiment
        """
        labels = ['negative', 'positive']
        self._check_columns(labels, df)

        results = self.zsl.predict(docs, labels=labels, include_labels=True, multilabel=False,
                              batch_size=batch_size,
                              nli_template="The sentiment of this movie review is {}.")
        df= self._format_to_df(results, df)
        if binarize: df = self._binarize_df(df, labels, threshold=threshold)
        return df

    def code_emotion(self, docs, df, batch_size=8, binarize=False, threshold=0.5):
        """
        Autocodes text for emotion
        """
        labels = ['joy', 'anger', 'fear', 'sadness']
        self._check_columns(labels, df)

        results = self.zsl.predict(docs, labels=labels, include_labels=True, multilabel=False,
                              batch_size=batch_size,
                              nli_template="The emotion of this text is {}.")
        df= self._format_to_df(results, df)
        if binarize: df = self._binarize_df(df, labels, threshold=threshold)
        return df

    def code_custom_topics(self, docs, df, labels, batch_size=8, binarize=False, threshold=0.5):
        """
        Autocodes text for user-specified topics.
        The `label` field is the name of the topic as a string (or a list of them.)
        """
        self._check_columns(labels, df)

        results = self.zsl.predict(docs, labels=labels, include_labels=True, batch_size=8)
        df = self._format_to_df(results, df)
        if binarize: df = self._binarize_df(df, labels, threshold=threshold)
        return df

    def code_callable(self, docs, df, fn):
        """
        Autocodes text for any user-specified function
        The `fn` parameter must be a Callable and return a dictionary for each
        text in `docs` where the keys are desired column names and values are scores
        or probabilities.
        """

        results = self.zsl.predict(docs, labels=labels, include_labels=True, batch_size=8)
        df = self._format_to_df(results, df)
        if binarize: df = self._binarize_df(df, labels, threshold=threshold)
        return df


