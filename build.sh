#!/bin/bash

# The OpenTRV project licenses this file to you
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
    if [ -d "./build" ]; then
        rm -rf build
    fi
}

mk_build() {
    mkdir build
    mkdir build/scad
    mkdir build/test
}

mk_files() {
    for f in $(ls "$1"); do
        b=${f%.*}
        c="./py/$b.py"
        if [ -x "$c" ]; then
            echo "Processing $c -l ./license-header.scad $1/$f $2/$b.scad"
            $c -l ./license-header.scad "$1/$f" "$2/$b.scad"
        else
            if [ -n "$3" ]; then
                opt="-i $3"
            else
                opt=""
            fi
            echo "Processing ./py/screw.py $opt -l ./license-header.scad $1/$f $2/$b.scad"
            ./py/screw.py $opt -l ./license-header.scad "$1/$f" "$2/$b.scad"
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
    mk_tree ./src ./build/scad
    mk_tree ./test ./build/test ../scad
}

clean
build

