# Supp
> TODO: PEG Parser

```txt
exp := a -> b       # (a and b)     [sequence]
exp := a -| b       # (a or b)      [alternative]
exp := a -^ b       # (a if predicate b)  [conditional]
# 
exp := > -> a       # (skip and a)  [jump]
exp := > -| a       # (skip or a)   [optional]
exp := > -^ a       # (skip if predicate a) [constrained skip]
# 
exp := > -> a <     # (skip and a {n} times) [repition]
exp := > -| a <     # (skip or a {n} times) [zero or more]
exp := > -^ a <     # (skip if predicate a {n} times) [skip if predicate repeated a]
# 
exp := a -> a <     # (a and a {n} times) [one or more greedy]
exp := a -| a <     # (a or a {n} times) [one or more non greedy]
exp := a -^ a <     # (a if predicate a {n} times) [match if only once]
```