######################################################################

# *** DISCLAIMER ***
# This file contains all the basic components that make up Kerouac's
# fundamentals. In the future, search functionalities will be added
# to the database, as well as perhaps improvements to the suggester.
# However, the functions already programmed are perfectly finished
# and will remain unchanged.

# *** Update ***
# To my surprise, I implemented the updates shortly after writing the
# disclaimer and was able to integrate them in time for deployment via
# pynstaller.

# -------------------------------------------------------------------
#  FUNCTIONALITIES 
# -------------------------------------------------------------------

# Database.build() [necessary to begin]
# Database.find(title) [finds a Node]
# Database.(e/y)Suggester(title) >> [creates a Suggester]
# Database.get() [gets a random node]
# Database.add_node(title) [adds a new node with empty fields]
# Database.delete_node(title) [obvious]
# Database.save() [deletes redundancies and empty attributes]

# Database.intersection(batch, reqmin) [searches]

# Node.add(synonym=[...], semantic=[...], observation=[...])
# Node.delete(synonym=[...], semantic=[...], observation=[...])
# Node.(un)pin() [either pins or unpins the node]

# Suggester.suggest() >> title

###############################################################

import utils
import random
import cdifflib
from collections import Counter

class Database :

    # Extra Functionalities

    @classmethod
    def ySuggester(cls, title):
        return Suggester.synonyms(title)
    @classmethod
    def eSuggester(cls, title):
        return Suggester.semantics(title)

    @classmethod
    def get(cls):
        return random.choice(cls.nodes)
    
    @classmethod
    def intersection(cls, batch, reqmin = 2): # basically, a search.
        sems = [cls.find(title).semantics for title in batch]
        counters = [Counter(lst) for lst in sems]
        merged_counter = sum(counters, Counter())
        return list({element for element, count in merged_counter.items() if count >= reqmin})

    # Basic Functionalities

    @classmethod
    def build(cls):
        database_raw_lines = utils.extract_data_from_txt()
        cls.nodes = [Node._from_line(line) for line in database_raw_lines]
    
    @classmethod
    def find(cls, title):

        low = 0
        high = len(cls.nodes) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_title = cls.nodes[mid].title
 
            if mid_title == title:
                return cls.nodes[mid]
            elif mid_title < title:
                low = mid + 1
            else:
                high = mid - 1

        return None  # No se encontró el nodo con el título buscado.
    
    @classmethod
    def add_node(cls, title):
        if not cls.find(title): # If it does not yet exist
            cls.nodes.append(Node._empty(title)) # It does now
        cls.nodes.sort(key=lambda node:node.title)

    @classmethod
    def delete_node(cls, title):
        if cls.find(title):
            for synonym in cls.find(title).synonyms:
                cls.find(synonym).delete(synonym=title) # Deletes the other end connexion for each synonymous attribute
            for semantic in cls.find(title).semantics:
                cls.find(semantic).delete(semantic=title) # Deletes the other end connexion for each semantical attribute
            cls.nodes.remove(cls.find(title)) # Finally, the node is deleted.
        cls.nodes.sort(key=lambda node:node.title)
    
    @classmethod
    def save(cls):
        cls.nodes.sort(key=lambda node:node.title)
        lines = ['|||'.join([node.title,
                             '0' if not node.pinned else '1',
                             '/'.join([_ for _ in list(set(node.synonyms)) if _]),
                             '/'.join([_ for _ in list(set(node.semantics)) if _]),
                             '/'.join([_ for _ in list(set(node.observations)) if _])]) for node in cls.nodes]
        utils.save_data_to_txt(lines, mode="w")
    
    # Advanced functionalities

    @classmethod
    def intelisearch(cls,trg,k=0.85):
        outputs = []
        for target in [trg[0].upper()+trg[1:], trg[0].lower()+trg[1:],trg.lower()]:
            for node in cls.nodes:
                ratios = []
                objects = [obj.strip() for obj in node.title.split(' ') if obj]
                for obj in objects:
                    ratios.append(cdifflib.CSequenceMatcher(None, target, obj).ratio())
                if max(ratios)>k:
                    outputs.append(node.title)
        res = sorted(set(outputs),key=len)
        return res[:3]+list(set(res[3:]))

###############################################################################

class Node :

    def __init__(self, title, pinned, synonyms, semantics, observations):
        self.title = title
        self.pinned = pinned
        self.synonyms, self.semantics = synonyms, semantics
        self.observations = observations
    
    def add(self, synonym=None, semantic=None, observation=None):
        if synonym:
            if not (synonym in self.synonyms or synonym == self.title): # Checks that not already inserted and different to entry itself
                self.synonyms.append(synonym) # Previsibly adds the synonym
                if not Database.find(synonym): 
                    Database.add_node(synonym) # Makes sure that the attribute is in the base
                if self.title not in Database.find(synonym).synonyms: # If the conneixon was not yet mutual 
                    Database.find(synonym).synonyms.append(self.title) # It makes it mutual
        if semantic:
            if not (semantic in self.semantics or semantic == self.title): # Checks that not already inserted and different to entry itself
                self.semantics.append(semantic) # Previsibly adds the synonym
                if not Database.find(semantic):
                    Database.add_node(semantic) # Makes sure that the attribute is in the base
                if self.title not in Database.find(semantic).semantics: # If the conneixon was not yet mutual 
                    Database.find(semantic).semantics.append(self.title) # It makes it mutual
        if observation:
            self.observations.append(observation) # Simply adds the observation
    
    def delete(self, synonym=None, semantic=None, observation=None):
        if synonym in self.synonyms:
            self.synonyms.remove(synonym) # Removes the attribute from the node
            Database.find(synonym).synonyms.remove(self.title) # Also removes the other end of the connexion
        if semantic in self.semantics:
            self.semantics.remove(semantic) # Removes the attribute from the node
            Database.find(semantic).semantics.remove(self.title) # Also removes the other end of the connexion
        if observation in self.observations:
            self.observations.remove(observation) # Removes the attribute from the node
    
    def pin(self):
        self.pinned = True
    def unpin(self):
        self.pinned = False
    
    @classmethod
    def _empty(cls,title):
        return cls(title=title, pinned=0, synonyms=[], semantics=[], observations=[])

    @classmethod
    def _from_line(cls,line):
        title, pinned, synonyms, semantics, observations = line.strip().split('|||')
        synonyms = synonyms.split('/') if synonyms.split('/') != [''] else []
        semantics = semantics.split('/') if semantics.split('/') != [''] else []
        observations = observations.split('/') if observations.split('/') != [''] else []
       
        return cls(title, pinned == "1", synonyms, semantics, observations)

################################################################################################################

class Suggester :

    def __init__ (self, keys, weights):
        self.keys, self.weights= keys, weights
        
    def suggest (self):
        # Randomly choices a result, as a function of its frequency index
        if self.keys == []:
            return None
        return random.choices(self.keys,weights=self.weights,k=1)[0]
    
    @classmethod
    def synonyms (cls, title):
        # This snippet is provisional
        distribution = {}
        for synonym_1 in Database.find(title).synonyms:
            for synonym_2 in Database.find(synonym_1).synonyms:
                distribution.setdefault(synonym_2,0)
                distribution[synonym_2] += 1 # Basically, collects the frequency index for each attribute up to the second level of depth 
        results = [item for item in distribution.items() if item[0] not in Database.find(title).synonyms and item[0] != title] # Filters impossible fits
        keys, weights = [item[0] for item in results], [item[1]**2.4 for item in results]
        return cls(keys, weights)

    @classmethod
    def semantics (cls, title):
        # This snippet is provisional
        distribution = {}
        for semantic_1 in Database.find(title).semantics:
            for semantic_2 in Database.find(semantic_1).semantics+Database.find(semantic_1).synonyms:
                distribution.setdefault(semantic_2,0)
                distribution[semantic_2] += 1 # Basically, collects the frequency index for each attribute up to the second level of depth 
        results = [item for item in distribution.items() if item[0] not in Database.find(title).semantics and item[0] != title] # Filters impossible fits
        keys, weights = [item[0] for item in results], [item[1]**2.4 for item in results]
        return cls(keys, weights)