// ROBOSKIN original removable bench fixture. Units: mm.
// This geometry has not been printed, structurally qualified, or fitted to a robot.
// Example: openscad -D 'part="carrier"' -D columns=3 -D rows=2 -o carrier.stl removable_carrier.scad
part="carrier"; // "carrier", "strain_relief", or "both"
columns=2;
rows=2;
pitch=25;
seal_margin=3;
rim=3;
thickness=1.5;
strap_width=10;
strap_slot=2;
ear_extension=7;
tail_slot_width=0; // Set to measured tail width + assembly clearance before live-panel use.
length=columns*pitch+2*seal_margin;
width=rows*pitch+2*seal_margin;
$fn=40;

assert(columns==2 && rows==2 || columns==3 && rows==2 || columns==7 && rows==4,
       "Use an explicitly supported channel profile");
assert(part=="carrier" || part=="strain_relief" || part=="both", "Unknown part");
assert(pitch>0 && seal_margin>0 && rim>0 && thickness>0 && strap_width>0 && strap_slot>0);
assert(tail_slot_width>=0 && tail_slot_width<width-2*seal_margin, "Invalid sensor-tail opening");

module rounded_rectangle(l,w,r=3) {
    hull() for(x=[-l/2+r,l/2-r]) for(y=[-w/2+r,w/2-r]) translate([x,y]) circle(r=r);
}
module carrier() {
    linear_extrude(thickness) difference() {
        union() {
            rounded_rectangle(length+2*rim,width+2*rim);
            // Two independent lateral straps; do not preload the sensing field.
            for(x=[-length/3,length/3]) for(s=[-1,1])
                translate([x,s*(width/2+rim+ear_extension/2-.5)]) square([strap_width+4,ear_extension+1],center=true);
        }
        rounded_rectangle(length-2*seal_margin,width-2*seal_margin,r=2);
        for(x=[-length/3,length/3]) for(s=[-1,1])
            translate([x,s*(width/2+rim+ear_extension/2)]) square([strap_width,strap_slot],center=true);
        // Optional opening in the +x rim. Its dimensions follow the actual sensor tail.
        // Keep the tail clear of the straps and avoid clamping its copper/printed traces.
        if(tail_slot_width>0)
            translate([length/2,0]) square([2*(rim+seal_margin+1),tail_slot_width],center=true);
    }
}
module cable_strain_relief() {
    // Tie a soft sleeve, not bare insulation. Mount on the same rigid body as the controller.
    difference() {
        linear_extrude(2) rounded_rectangle(30,16,r=3);
        for(x=[-9,9]) translate([x,0,-.1]) linear_extrude(2.2) square([2,10],center=true);
    }
}
if(part=="carrier" || part=="both") carrier();
if(part=="strain_relief") cable_strain_relief();
if(part=="both") translate([length/2+25,0,0]) cable_strain_relief();
