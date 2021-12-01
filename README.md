# domydrafter
A program for drafting nations for the Dominions 5 game.

## Installation

## Using domydrafter

domydrafter is built around three data structures: picks, pools and booster
boxes. Data is specified in human-readable yaml files.

domydrafter makes use of _pyyaml_ to consume properly structured yaml files
and convert their data into objects it can use. A core part of this
comes from yaml tags. Picks are tagged as _!Pick_, pools as _!Pool_, and
booster boxes as _!BoosterBox_.

The basic building block of yaml is the document. A yaml file can
contain multiple documents, each starting with three dashes '---'.
For your convenience we recommend putting all of your objects in
separate documents (they can be in the same file though don't worry).

### Pick

A "pick" is something you can pick out of a booster pack. Think of it like
an individual card in a trading card game. Picks have an id, a name, and
may have optional attributes and tags.

| Field | Type | Use |
| --- | --- | ---
| id | string | unique identifying id of the pick |
| name | string | name of the pick |
| attr | dict | key/value pairs of attributes for this pick |
| tags | list | list of tags for this pick |

An empty pick looks like this:

```yaml
---
!Pick
id:
name:
attr:
tags:
---
```

A sample pick with some actual data could look like this:

```yaml
---
!Pick
id: u2469
name: fir bolg druid
attr:
  nation:
    - early_tirnnanog
    - early_fomoria
  paths:
    - a1
    - (wen)1
tags:
  - mage
---
```

Many picks come prepopulated with the program. Note the 'u' before the
unit's actual id. Picks can be anything, not just units. Unfortunately,
the game uses the same id numbers for different things depending on context.
So our solution to logically separate entities with the same id number in the
game is to prefix them with a letter. We used the following prefixes as
convention when populating the data:

| Prefix | Pick type |
|--- | --- |
| u | unit |
| n | nation |
| i | item |
| e | event |
| m | magic site |
| s | spell |

### Pool

A pool groups picks together. The program draws from pools to generate
booster packs. Pools can contain picks, specified by their id. They
can also refer to other pools that are then merged together. Finally,
if you want to import picks from other pools but would like to leave
some of them out, you can do so using the _remove_ field.

| Field | Type | Use |
| --- | --- | --- |
| name | str | Name of the pool. Should be unique. |
| picks | list | List of pick ids to include in the pool. |
| merge | list | List of pool names to merge into this pool |
| remove | list | List of pick ids to remove from this pool |

An empty pool looks like this:

```yaml
---
!Pool
name:
picks:
merge:
remove:
---
```

A sample pool might look like this:

```yaml
---
!Pool
name: my_elven_mages
picks:
  # Hangadrott
  - u847
  # Dis
  - u1507
merge:
  - early_vanheim_mages
  - middle_yis_mages
remove:
  # Dwarven Smith; Not an elf
  - u323
---
```

### BoosterBox

The booster box is the entity from which booster packs are generated. A
booster box specifies a list of pools, each with a number indicating how many
picks to draw from this pool. Picks are guaranteed to be unique for a given
pool in a given booster pack. The booster box is how hosts can specify a
specific "format" for their drafts.

| Field | Type | Use |
| --- | --- | --- |
| name | string | Name of the booster box |
| pools | list | List of key/value pairs indicating pools and number of picks|

An empty booster box looks like this:

```yaml
---
!BoosterBox
name:
pools:
---
```

A sample booster box could look like this:

```yaml
---
!BoosterBox
name: elves_bonanza
pools:
  - my_elven_troops: 4
  - my_elven_commanders: 3
  - my_elven_mages: 2
---
```

This booster box would generate boosters containing a total of 9 picks drawn
from their respective pools.