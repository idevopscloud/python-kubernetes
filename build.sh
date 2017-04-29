#!/bin/bash
#
# output:
#   target/python-kubernetes.tar.gz
#

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

usage()
{
    echo "build.sh"
}

workdir=$DIR/target/workdir
outdir=$DIR/target

if [ -d $outdir ]; then
    rm -rf $outdir/*
fi

mkdir -p $outdir 2>&1>/dev/null
mkdir -p $workdir 2>&1>/dev/null
cp -r kubernetes $workdir
cd $workdir
python -m compileall kubernetes
rm kubernetes/*.py
tar czvf $outdir/python-kubernetes.tar.gz kubernetes
rm -r $workdir

