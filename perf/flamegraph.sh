#!/bin/bash -e
# frequency (-F) * sleep time ~= 20000 won't break browsers
# much more than that will (depending on --minwidth, higher is safer).

F=$((21000 / $2))
if [[ $F == 0 ]]; then
   F=1
fi

echo $3: recording process $1 for $2 seconds at $F samples per second


PERF_FILE=perf/perf-record-$3.perf
PERF_TEMP=/tmp/out-$3.perf
PERF_TEMP_FOLDED=/tmp/out-folded-$3.perf
FLAME_FILE=perf/$3.svg
ICICLE_FILE=perf/rev-$3.svg


sudo perf record -F $F -p $1 -g -o $PERF_FILE  -- sleep $2
sudo perf script -i $PERF_FILE > $PERF_TEMP

~/src/FlameGraph/stackcollapse-perf.pl $PERF_TEMP > $PERF_TEMP_FOLDED

~/src/FlameGraph/flamegraph.pl --title="$3" --minwidth 0.2 --width 1060  $PERF_TEMP_FOLDED > $FLAME_FILE
~/src/FlameGraph/flamegraph.pl  --title="$3 reverse" --reverse --inverted -colors=chain --minwidth 0.3 --width 1060 $PERF_TEMP_FOLDED > $ICICLE_FILE
