import json
from flashtext import KeywordProcessor
from collections import defaultdict
import re
import logging
from janome.tokenizer import Tokenizer

with_category=re.compile("[^#]*#[^#]+")
good_noun=["一般","固有名詞"]

class entity:
    def __init__(self,name,num_referenced):
        self.name=name
        self.num_referenced=num_referenced


class entity_store:
    def load(self,filename):
        with open(filename,encoding="utf-8") as f:
            terms=json.load(f)
            self.entities=defaultdict(list)
            #count=0
            for k,v in terms.items():
                new_entity=entity(k,sum(v.values()))
                for key in v.keys():
                    if v[key]<5 or len(key)<2 or with_category.match(key):
                        continue
                    self.entities[key].append(new_entity)
                # count+=1
                # if count>100:
                #     break
            del terms

                
    def get(self,name):
        return max(self.entities[name],key=lambda x:x.num_referenced)
    
    def get_all(self,name):
         return [(entity.name,entity.num_referenced) for entity in self.entities[name]]
        
    def get_all_terms(self):
        return self.entities.keys()

class entity_extractor:
    def __init__(self,store):
        self.store=store
        self.t=Tokenizer()
    
    def build(self):
        self.kp=KeywordProcessor()
        [self.kp.add_keyword(word) for word in self.store.get_all_terms()]
    
        
    def extract(self,text):
        #[(term1,begin,end),(term2,begin,end)...]
        extracted=self.kp.extract_keywords(text,span_info=True)
        filtered=self.nlp_filter(text,extracted)
        return [self.store.get(e[0]).name for e in filtered ]
    
    def nlp_filter(self,text,extracted):
        tokens=self.t.tokenize(text)
        starToToken={}
        endToToken={}
        offset=0
        for token in tokens:
            starToToken[offset]=token
            offset+=len(token.surface)
            endToToken[offset]=token
            token.part_of_speech
        filterd=[]
        for t in extracted:
            if t[1] in starToToken.keys() and t[2] in endToToken.keys():
                if starToToken[t[1]]==endToToken[t[2]]:
                    if not starToToken[t[1]].part_of_speech.startswith("名詞"):
                        continue
                    elif starToToken[t[1]].part_of_speech.split(",")[1] not in good_noun:
                        continue
                filterd.append(t)
        return filterd

def load(wikijson):
    logging.info("Loading entity extractor")
    es=entity_store()
    es.load(wikijson)
    logging.info("{} words are loaded".format(len(es.entities)))
    extractor=entity_extractor(es)
    extractor.build()
    logging.info("Complete to load entity extractor")
    return extractor

if __name__=="__main__":
    extractor=load("result.json")
    print(extractor.extract("ラ・サール高校は鹿児島県にある高校です"))
    print(extractor.extract("マツコ・デラックスと有吉の番組は面白い"))