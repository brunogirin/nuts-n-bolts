#!/bin/bash

# The Nuts'n'bolts project licenses this file to you
# under the Apache Licence, Version 2.0 (the "Licence");
# you may not use this file except in compliance
# with the Licence. You may obtain a copy of the Licence at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the Licence is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Licence for the
# specific language governing permissions and limitations
# under the Licence.
#
# Author(s) / Copyright (s): Bruno Girin 2013

clean() {
    if [ -d "$base/build" ]; then
        rm -rf $base/build
    fi
}

mk_build() {
    mkdir $base/build
    mkdir $base/build/scad
    mkdir $base/build/test
}

mk_files() {
    for f in $(ls "$1"); do
        b=${f%.*}
        c="$base/py/$b.py"
        if [ -x "$c" ]; then
            echo "Processing $c -l $base/license-header.scad $1/$f $2/$b.scad"
            $c -l $base/license-header.scad "$1/$f" "$2/$b.scad"
        else
            if [ -n "$3" ]; then
                opt="-i $3"
            else
                opt=""
            fi
            echo "Processing $base/py/screw.py $opt -l $base/license-header.scad $1/$f $2/$b.scad"
            $base/py/screw.py $opt -l $base/license-header.scad "$1/$f" "$2/$b.scad"
        fi
    done
}

mk_tree() {
    cp $1/scad/*.scad "$2"
    for f in $(ls "$1" | grep -v 'scad'); do
        if [ -d "$1/$f" ]; then
            mk_files "$1/$f" "$2" "$3"
        fi
    done
}

build() {
    mk_build
    mk_tree $base/src $base/build/scad
    mk_tree $base/test $base/build/test ../scad
}

base=$(dirname $0)
clean
build

