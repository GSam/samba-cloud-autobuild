#!/bin/bash -x
# frequency (-F) * sleep time ~= 20000 won't break browsers
# much more than that will (depending on --minwidth, higher is safer).

echo $2: recording off CPU for $1 seconds

FLAMEGRAPH_PL=~/src/FlameGraph/flamegraph.pl
STACK_COLLAPSE=~/src/FlameGraph/stackcollapse-perf.pl

PERF_FILE=perf/perf-record-$2.perf
PERF_TEMP=/tmp/out-$2.perf
PERF_TEMP_FOLDED=/tmp/out-folded-$2.perf
FLAME_FILE=perf/$2.svg
ICICLE_FILE=perf/rev-$2.svg

OFF_CPU_PERF_DATA=perf/off-cpu-perf.data.raw

sudo perf record -e sched:sched_stat_sleep -e sched:sched_switch -e sched:sched_process_exit -a -g -o $PERF_FILE sleep $1

sudo perf inject -v -s -i $PERF_FILE -o $PERF_TEMP

sudo perf script -i $PERF_TEMP -f comm,pid,tid,cpu,time,period,event,ip,sym,dso,trace | awk '
    NF > 4 { exec = $1; period_ms = int($5 / 1000000) }
    NF > 1 && NF <= 4 && period_ms > 0 { print $2 }
    NF < 2 && period_ms > 0 { printf "%s\n%d\n\n", exec, period_ms }' | \
    $STACKCOLLAPSE | \
    $FLAMEGRAPH_PL --countname=ms --minwidth 0.3 --width 1060  --title="$2 Off-CPU Time Flame Graph" --colors=io > $FLAME.svg
echo 4
