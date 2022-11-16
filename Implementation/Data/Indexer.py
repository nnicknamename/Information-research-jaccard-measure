from  Data.Corpus import *
import spacy 
import pandas as pd
import re
import pickle
import numpy as np
class Indexer:
    def __init__(self,corpus:Corpus=None,file_name:str=None):
        assert corpus is not None or file_name is not None ,"a corpus or a file should be provided"
        self.en_mod=spacy.load('en_core_web_sm')
        if(file_name is not None):
            self.load(file_name)
        else:
            self.corpus=corpus

            self.corpus_tokens=self.pre_process(self.corpus)
            self.term_frequencys,self.terms =self.calculate_term_frequencys()
            self.words_in_doc= self.calculate_words_in_doc()
            self.nb_docs_with_word=self.calculate_nb_docs_with_word()
            self.tf_idf=self.calculate_Tf_Idf(self.words_in_doc,self.nb_docs_with_word)

    def save(self,filename):
        file=open(filename,'wb')
        pickle.dump(self.get_corpus_tokens(),file)
        pickle.dump(self.term_frequencys,file)
        pickle.dump(self.nb_docs_with_word,file)
        pickle.dump(self.terms,file)
        pickle.dump(self.tf_idf,file)
        file.close()
    def load(self,filename):
        file=open(filename,'rb')
        self.corpus_tokens=pickle.load(file)
        self.term_frequencys=pickle.load(file)
        self.nb_docs_with_word=pickle.load(file)
        self.terms=pickle.load(file)
        self.tf_idf=pickle.load(file)
        file.close()
    def pre_process(self,corpus:Corpus):
        corpus_tokens=[]
        for doc in corpus:
            text=re.sub(r"[^a-zA-Z, ]",' ',doc['text'])
            tokens=pd.DataFrame([word.lemma_  for word in self.en_mod(text) if not word.is_punct and not word.is_stop and not word.is_space and not word.is_digit])
            corpus_tokens.append(tokens)
        return corpus_tokens

    def get_corpus_tokens(self):
        return self.corpus_tokens

    def get_term_frequencys(self):
        return self.term_frequencys

    def index(self,query,binary=True):
        text=re.sub(r"[^a-zA-Z, ]",' ',query)
        tokens=pd.DataFrame([word.lemma_  for word in self.en_mod(text) if not word.is_punct and not word.is_stop and not word.is_space and not word.is_digit])
        if not binary:
            return np.in1d(self.terms,tokens).astype(int)/tokens.size* np.log(self.term_frequencys.shape[0] / self.nb_docs_with_word)
        else:
            return np.in1d(self.terms,tokens).astype(int)

    def calculate_term_frequencys(self):
        frec=pd.concat([doc.value_counts()for doc in self.corpus_tokens],axis=1,)
        term_frequencys=frec.fillna(0).to_numpy().transpose()
        terms= np.array([term[0]  for term in frec.transpose().keys().to_numpy()])
        return term_frequencys,terms

    def calculate_words_in_doc(self):
        return np.sum((self.term_frequencys>0),axis=1)

    def calculate_nb_docs_with_word(self):
        return np.count_nonzero((self.term_frequencys>0),axis=0)

    def calculate_Tf_Idf(self,words_in_doc,nb_docs_with_word):
        return (self.term_frequencys / words_in_doc[:,None]) * np.log(self.term_frequencys.shape[0] / nb_docs_with_word)

    def get_tf_idf(self):
        return self.tf_idf

    def get_docs_with_jaccard(self,query):
        q=self.index(query)
        binary_index=((self.term_frequencys>0).astype(int))
        similaritys=np.logical_and(q,binary_index).sum(axis=1)/np.logical_or(q,binary_index).sum(axis=1)
        return np.where(np.flip(np.sort(similaritys))==similaritys)

    def get_docs_with_jaccard_01(self,query):

        q=self.index(query,binary=False)

        c=np.repeat([q],self.get_tf_idf().shape[0],axis=0)*self.get_tf_idf()
        return c.sum(axis=1)/((q**2).sum()+(self.get_tf_idf()**2).sum(axis=1)-c.sum(axis=1))

    def get_terms(self):
        return self.terms
        
    def __len__(self):
        return len(self.corpus_tokens)
 
    def __getitem__(self,idx):
        return self.corpus_tokens[idx]