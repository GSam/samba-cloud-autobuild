#!/bin/bash
# frequency (-F) * sleep time ~= 10000 won't break browsers
# much more than that will.

F=$((14000 / $2))
if [[ $F == 0 ]]; then
   F=1
fi

echo $F

#exit

sudo perf record -F $F -p $1 -g -- sleep $2
sudo perf script > out.perf

~/src/FlameGraph/stackcollapse-perf.pl out.perf > out.folded

~/src/FlameGraph/flamegraph.pl --minwidth 0.1 --width 1060  out.folded > $3
~/src/FlameGraph/flamegraph.pl --reverse --inverted -colors=chain --minwidth 0.3 --width 1060  out.folded > rev-$3
