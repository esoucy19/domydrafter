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

    picks: ClassVar[Dict[str, Any]] = {}

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
    picks: List[str] = field(default_factory=list)
    merge: List[str] = field(default_factory=list)
    remove: List[str] = field(default_factory=list)
    _picks: Dict[str, Pick] = field(default_factory=dict, repr=False)

    pools: ClassVar[Dict[str, Any]] = {}

    def __post_init__(self):
        for i, pick in enumerate(self.picks):
            if type(pick) == str or type(pick) == int:
                self._picks[str(pick)] = Pick.picks[str(pick)]
            elif type(pick) == dict:
                self.picks[i] = pick['id']
                self._picks[pick['id']] = Pick(**pick)
            elif type(pick) == Pick:
                self.picks[i] = pick.id
                self._picks[pick.id] = pick
        for pool in self.merge:
            if pool in Pool.pools:
                self._picks.update(Pool.pools[pool]._picks)
        for pick in self.remove:
            if pick in self._picks:
                del(self._picks[pick])
        Pool.pools[self.name] = self


def pool_constructor(loader, node):
    args = loader.construct_mapping(node, deep=True)
    return Pool(**args)


yaml.add_constructor('!Pool', pool_constructor)


def pool_representer(dumper, data):
    ddict = asdict(data)
    ddict.pop('_picks')
    return dumper.represent_mapping('!Pool', ddict)


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
                name = pool[0]
                num_picks = pool[1]
                self.pools[i] = (Pool.pools[name], num_picks)
            BoosterBox.boxes[self.name] = self

    def new_booster(self):
        booster = []
        for pool in self.pools:
            pool_draws = set()
            picks = list(pool[0]._picks.values())
            num_picks = pool[1]
            new_size = len(pool_draws) + num_picks
            while len(pool_draws) != new_size:
                pool_draws.add(picks[random.randrange(len(picks))].id)
            pool_picks = [Pick.picks[id] for id in pool_draws]
            booster += pool_picks
        return booster


def boosterbox_constructor(loader, node):
    args = loader.construct_mapping(node, deep=True)
    return BoosterBox(**args)


yaml.add_constructor('!BoosterBox', boosterbox_constructor)


def boosterbox_representer(dumper, data):
    return dumper.represent_mapping('!BoosterBox', asdict(data))


yaml.add_representer(BoosterBox, boosterbox_representer)