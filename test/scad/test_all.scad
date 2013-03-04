/*
The OpenTRV project licenses this file to you
under the Apache Licence, Version 2.0 (the "Licence");
you may not use this file except in compliance
with the Licence. You may obtain a copy of the Licence at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the Licence is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the Licence for the
specific language governing permissions and limitations
under the Licence.

Author(s) / Copyright (s): Bruno Girin 2013
*/

use <test.scad>;
use <../scad/iso261.scad>;

translate([-40,0,0])
test1(6);

translate([-30,0,0])
difference() {
	M10(6, slices=100);
	translate([0,0,-0.25])
		cube(size=6.5);
}

translate([-20,0,0])
difference() {
	M1x0_25(4, slices=200);
	translate([0,0,-0.25])
		cube(size=6.5);
}

translate([-10,0,0]) {
difference() {
    M5_ext(6, slices=500);
    translate([0,0,-0.25])
        cube(size=6.5);
}
difference() {
    difference() {
        translate([0,0,0.25])
            cylinder(r=4, h=4);
        M5_int(4.5, slices=500);
    }
    translate([0,0,-0.25])
        cube(size=6.5);
}
}

ramp(6);
