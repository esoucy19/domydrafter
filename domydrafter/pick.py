import random
import yaml

from dataclasses import dataclass, field, asdict
from collections import namedtuple
from enum import Enum, auto
from typing import Dict, List, Tuple, ClassVar, Set, Any


@dataclass
class Pick:
    id: str
    name: str = ''
    attr: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)

    picks: ClassVar[Dict[int, Any]] = {}

    def __post_init__(self):
        if self.id in Pick.picks:
            self.update()
        else:
            Pick.picks[self.id] = self

    def update(self):
        id = self.id
        name = self.name
        attr = self.attr
        tags = self.tags
        self = Pick.picks[id]
        if name != '':
            self.name = name
        if attr:
            for key in attr:
                self.attr[key] = attr[key]
        if tags:
            for tag in tags:
                if tag[0] == '-':
                    tag_to_del = tag[1:]
                    self.tags.discard(tag_to_del)
                else:
                    self.tags.add(tag)


def pick_constructor(loader, node):
    args = loader.construct_mapping(node, deep=True)
    return Pick(**args)


yaml.add_constructor('!Pick', pick_constructor)


def pick_representer(dumper, data):
    return dumper.represent_mapping('!Pick', asdict(data))


yaml.add_representer(Pick, pick_representer)


@dataclass
class Pool():
    name: str
    picks: List[Pick] = field(default_factory=list)
    merge: List[str] = field(default_factory=list)

    pools: ClassVar[Dict[str, Any]] = {}

    def __post_init__(self):
        for i, pick in enumerate(self.picks):
            if type(pick) == str or type(pick) == int:
                self.picks[i] = Pick.picks[str(pick)]
            elif type(pick) == dict:
                self.picks[i] = Pick(**pick)
        for pool in self.merge:
            if pool in Pool.pools:
                self.picks += Pool.pools[pool].picks
        Pool.pools[self.name] = self


def pool_constructor(loader, node):
    args = loader.construct_mapping(node, deep=True)
    return Pool(**args)


yaml.add_constructor('!Pool', pool_constructor)


def pool_representer(dumper, data):
    return dumper.represent_mapping('!Pool', asdict(data))


yaml.add_representer(Pool, pool_representer)


@dataclass
class BoosterBox:
    name: str
    pools: List[Tuple[Pool, int]] = field(default_factory=list)

    boxes: ClassVar[Dict[str, Any]] = {}

    def __post_init__(self):
        for i, pool in enumerate(self.pools):
            if type(pool) == dict:
                for key in pool:
                    name = key
                    num_picks = pool[key]
                    self.pools[i] = (Pool.pools[name], num_picks)
            if type(pool) == list:
                print(pool)
                name = pool[0]
                num_picks = pool[1]
                self.pools[i] = (Pool.pools[name], num_picks)
            BoosterBox.boxes[self.name] = self

    def new_booster(self):
        booster = set()
        for pool in self.pools:
            picks = pool[0].picks
            num_picks = pool[1]
            new_size = len(booster) + num_picks
            while len(booster) != new_size:
                booster.add(picks[random.randrange(len(picks))].id)
        booster = list(booster)
        for i, id in enumerate(booster):
            booster[i] = Pick.picks[id]
        return booster


def boosterbox_constructor(loader, node):
    args = loader.construct_mapping(node, deep=True)
    return BoosterBox(**args)


yaml.add_constructor('!BoosterBox', boosterbox_constructor)


def boosterbox_representer(dumper, data):
    return dumper.represent_mapping('!BoosterBox', asdict(data))


yaml.add_representer(BoosterBox, boosterbox_representer)