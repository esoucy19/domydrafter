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

### Pick

A "pick" is something you can pick out of a booster pack. Think of it like
an individual card in a trading card game. Picks have an id, a name, and
may have optional attributes and tags. An empty pick looks like this:

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
|--- | --- | --- |
| u | unit |
| n | nation |
| i | item |
| e | event |
| m | magic site |
| s | spell |