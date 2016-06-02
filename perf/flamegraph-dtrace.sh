#!/bin/bash -e
# frequency (-F) * sleep time ~= 20000 won't break browsers
# much more than that will (depending on --minwidth, higher is safer).

F=$((21000 / $2))
if [[ $F == 0 ]]; then
   F=1
fi

echo $3: recording process $1 for $2 seconds at $F samples per second


DTRACE_FILE=perf/perf-record-$3.dtrace
FLAME_FILE=perf/$3.svg
ICICLE_FILE=perf/rev-$3.svg

dtrace -x ustackframes=100 -n 'profile-97 /pid == '$1'/ { @[ustack()] = count(); } tick-60s { exit(0); }' -o $DTRACE_FILE


~/src/FlameGraph/stackcollapse.pl $DTRACE_FILE > out.kern_folded

sudo perf record -F $F -p $1 -g -o $PERF_FILE  -- sleep $2
sudo perf script -i $PERF_FILE > $PERF_TEMP

~/src/FlameGraph/stackcollapse-perf.pl $PERF_TEMP > $PERF_TEMP_FOLDED

~/src/FlameGraph/flamegraph.pl --title="$3" --minwidth 0.2 --width 1060  $PERF_TEMP_FOLDED > $FLAME_FILE
~/src/FlameGraph/flamegraph.pl  --title="$3 reverse" --reverse --inverted -colors=chain --minwidth 0.3 --width 1060 $PERF_TEMP_FOLDED > $ICICLE_FILE



