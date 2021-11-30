import random
import yaml

from dataclasses import dataclass, field
from collections import namedtuple
from enum import Enum, auto
from typing import Dict, List, Tuple

class Pick:
    picks = dict()
    def __init__(self, id, name = '', attr = [], tags = dict()):
        self.id = id
        self.name = name
        self.attr = attr
        self.tags = tags
        if id in Pick.picks:
            self.update(id, name, attr, tags)
        else:
            Pick.picks[id] = self
    def __repr__(self):
        return "%s(id=%r, name=%r, attr=%r, tags=%r)" % (
            self.__class__.__name__, self.id, self.name, self.attr, self.tags)
    def update(self, id, name, attr, tags):
        self = Pick.picks[id]
        if name != '':
            self.name = name
        if attr != None:
            for key in attr:
                self.attr[key] = attr[k]
        if tags != None:
            for tag in tags:
                if tag[0] == '-':
                    tag_to_del = tag[1:]
                    self.tags.discard(tag_to_del)
                else:
                    self.add(tag)
                    
def pick_constructor(loader, node):
    args = loader.construct_mapping(node)
    return Pick(**args)
    
yaml.add_constructor('!Pick', pick_constructor)
    

class Pool():
    pools = dict()
    def __init__(self, name = '', picks = set()):
        self.name = name
        self.picks = set()
        for pick in picks:
            if type(pick) == Pick:
                self.picks.add(pick)
            elif pick in Pick.picks:
                self.picks.add(Pick.picks[pick])
            else:
                new_pick = Pick(pick)
                self.picks.add(new_pick)
        if name in Pool.pools:
            temp_picks = self.picks
            self = Pool.pools[name]
            self.picks = self.picks.union(temp_picks)
        Pool.pools[name] = self
    def __repr__(self):
        return "%s(name=%r, picks=%r)" % (
            self.__class__.__name__, self.name, self.picks)     

def pool_constructor(loader, node):
    args = loader.construct_mapping(node, deep=True)
    return Pool(**args)
    
yaml.add_constructor('!Pool', pool_constructor)

class BoosterBox:
    yaml_tag = u'!BoosterBox'
    boxes = dict()
    def __init__(self, name, pools = []):
        self.name = name
        self.pools = pools
        
    def new_booster(self):
        booster = set()
        for pool in self.pools:
            picks = pool[0].picks
            numPicks = pool[1]
            new_size = len(booster) + numPicks
            while(len(booster) != new_size):
                booster.add(picks[random.randrange(len(picks))])
        return booster
