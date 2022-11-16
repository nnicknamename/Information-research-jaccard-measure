from Data import *



if __name__=="__main__":
    corpus=CranCorpus("C:/Users/pc/Documents/programming/RI_TP/Datasets/Cran/cran.all.1400")
    
    indexer=Indexer(corpus)
    print(indexer.calculate_Tf_Idf())
