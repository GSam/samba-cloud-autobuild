#!/bin/bash -e 
# frequency (-F) * sleep time ~= 20000 won't break browsers
# much more than that will (depending on --minwidth, higher is safer).
set -x
tag=$1
freq=$2
shift
shift
echo $tag: recording all processes at ${freq}Hz

PERF_FILE=perf/perf-record-$tag.perf
PERF_TEMP=/tmp/out-$tag.perf
PERF_TEMP_FOLDED=/tmp/out-folded-$tag.perf
FLAME_FILE=perf/$tag.svg
ICICLE_FILE=perf/rev-$tag.svg

USER=`whoami`

sudo perf record -F $freq -a  -g -o $PERF_FILE  -- sudo -u $USER $@
sudo perf script -i $PERF_FILE > $PERF_TEMP

~/src/FlameGraph/stackcollapse-perf.pl $PERF_TEMP > $PERF_TEMP_FOLDED

~/src/FlameGraph/flamegraph.pl --minwidth 0.2 --width 1060  $PERF_TEMP_FOLDED > $FLAME_FILE
~/src/FlameGraph/flamegraph.pl --reverse --inverted -colors=chain --minwidth 0.3 --width 1060 $PERF_TEMP_FOLDED > $ICICLE_FILE
