from abc import ABC, abstractmethod
from typing import Dict
import re
class Corpus(ABC):
    def __init__(self,file_mame,name):
        self.file_name=file_mame
        self.name=name 
    @abstractmethod
    def load_data(self,file_name):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self) -> Dict[str,str]:
        pass

class CranCorpus(Corpus):
    def __init__(self, file_mame):
        super().__init__(file_mame,"carn")
        self.documents=self.load_data()
        
    def get_raw_docs(self):
        file=open(self.file_name,'r')
        corpusLines=file.readlines()
        document_idx=[i for i,line in enumerate(corpusLines) if re.match(r".I \d",line) is not None]
        return ["".join(corpusLines[document_idx[i-1]:document_idx[i]]) for i in range(1,len(document_idx))]
        
    def load_data(self):
        corpus_raw_documents=self.get_raw_docs()
        documents=[]
        for i,doc in enumerate(corpus_raw_documents):
            match=re.match(r"\.I (\d+)\n\.T((.|\n)*)\.A((.|\n)*)\.B((.|\n)*)\.W((.|\n)*)",doc)
            assert match is not None ,"Error parsing the file on document "+str(i)
            res={"idx":int(match.groups()[0].replace("\n",'')),"title":match.groups()[1].replace("\n",''),"author":match.groups()[3].replace("\n",''),"bib":match.groups()[5].replace("\n",''),"text":match.groups()[7].replace("\n",' ')}
            if(self.match_not_empty(res)):
                documents.append(res)
            else:
                print('found empty document at index ',res['idx'])
        return documents

    def match_not_empty(self,match):
        return match['text'] is not ''
        
    def __len__(self):
        return len(self.documents)

    def __getitem__(self,idx) -> Dict[str, str]:
        return self.documents[idx]

class CranQueryCorpus(Corpus):
    def __init__(self, file_mame):
        super().__init__(file_mame,'cran_query')
        self.documents=self.load_data()
        [document.update({'_id':i})  for i,document in enumerate(self.documents)]
    def get_raw_docs(self):
        file=open(self.file_name,'r')
        corpusLines=file.readlines()
        document_idx=[i for i,line in enumerate(corpusLines) if re.match(r".I \d",line) is not None]
        return ["".join(corpusLines[document_idx[i-1]:document_idx[i]]) for i in range(1,len(document_idx))]
    
    def load_data(self):
        corpus_raw_documents=self.get_raw_docs()
        documents=[]
        for i,doc in enumerate(corpus_raw_documents):
            match=re.match(r"\.I (\d+)\n\.W((.|\n)*)",doc)
            assert match is not None ,"Error parsing the file on document "+str(i)
            documents.append({"idx":int(match.groups()[0].replace("\n",'')),"text":match.groups()[1].replace("\n",' ')})
        return documents
            
    def __len__(self):
        return len(self.documents)

    def __getitem__(self,idx) -> Dict[str, str]:
        return self.documents[idx]

if __name__=="__main__":
    CCorpus=CranQueryCorpus("Datasets/Cran/cran.qry")
    
    print(CCorpus[1])
    


    #   print(re.match(r"\.I \d+\n\.T((.|\n)*)\.A((.|\n)*)\.B((.|\n)*)\.W((.|\n)*)",data[410]))
# 0 idx
# 1 title
# 3 author 
# 5 bib
# 7 text