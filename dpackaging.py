from vpython import *
import math

scene = canvas(
    title='Hierarchical DNA Packaging',
    width=1400,
    height=900,
    background=color.black
)

scene.camera.pos = vector(0,-20,120)

# =========================================================
# DNA DOUBLE HELIX
# =========================================================

dna_objects = []

radius = 2
pitch = 0.25
turns = 180

prev1 = None
prev2 = None

for i in range(turns):

    t = i * 0.22
    y = i * pitch

    p1 = vector(
        radius * math.cos(t),
        y,
        radius * math.sin(t)
    )

    p2 = vector(
        radius * math.cos(t + math.pi),
        y,
        radius * math.sin(t + math.pi)
    )

    s1 = sphere(pos=p1, radius=0.18, color=color.cyan)
    s2 = sphere(pos=p2, radius=0.18, color=color.orange)

    dna_objects.extend([s1,s2])

    # backbone
    if prev1:
        dna_objects.append(
            cylinder(
                pos=prev1,
                axis=p1-prev1,
                radius=0.05,
                color=color.cyan
            )
        )

    if prev2:
        dna_objects.append(
            cylinder(
                pos=prev2,
                axis=p2-prev2,
                radius=0.05,
                color=color.orange
            )
        )

    # base pairs
    if i % 4 == 0:
        dna_objects.append(
            cylinder(
                pos=p1,
                axis=p2-p1,
                radius=0.04,
                color=color.white
            )
        )

    prev1 = p1
    prev2 = p2

label(
    pos=vector(0,50,0),
    text='DNA Double Helix (2 nm)',
    box=False,
    height=18,
    color=color.white
)

# =========================================================
# NUCLEOSOMES
# =========================================================

nucleosomes = []

base_y = -20

for n in range(8):

    cx = -28 + n*8

    histone = sphere(
        pos=vector(cx,base_y,0),
        radius=1.6,
        color=color.red,
        opacity=0.9
    )

    nucleosomes.append(histone)

    prev = None

    for j in range(120):

        theta = j * 0.18

        p = vector(
            cx + 2.4*math.cos(theta),
            base_y + 0.02*j,
            2.4*math.sin(theta)
        )

        s = sphere(
            pos=p,
            radius=0.07,
            color=color.yellow
        )

        if prev:
            cylinder(
                pos=prev,
                axis=p-prev,
                radius=0.03,
                color=color.yellow
            )

        prev = p

label(
    pos=vector(0,-8,0),
    text='Nucleosome Fiber (10 nm)',
    box=False,
    height=18,
    color=color.white
)

# =========================================================
# 30 nm CHROMATIN FIBER
# =========================================================

fiber = []

for i in range(220):

    t = i * 0.18

    p = vector(
        12*math.cos(t),
        -55 + i*0.18,
        12*math.sin(t)
    )

    fiber.append(
        sphere(
            pos=p,
            radius=0.7,
            color=color.green
        )
    )

label(
    pos=vector(0,-25,0),
    text='30 nm Chromatin Fiber',
    box=False,
    height=18,
    color=color.white
)

# =========================================================
# LOOPED DOMAINS
# =========================================================

loops = []

for i in range(10):

    x = -36 + i*8

    r = ring(
        pos=vector(x,-95,0),
        axis=vector(0,1,0),
        radius=3,
        thickness=0.35,
        color=color.magenta
    )

    loops.append(r)

label(
    pos=vector(0,-82,0),
    text='Looped Chromatin Domains',
    box=False,
    height=18,
    color=color.white
)

# =========================================================
# METAPHASE CHROMOSOME
# =========================================================

chromosome = []

for i in range(120):

    y = -155 + i*0.9

    center_factor = abs(i-60)/60

    width = 5*(1-center_factor**1.5)+0.8

    left = sphere(
        pos=vector(-6-width*0.2,y,0),
        radius=width*0.22,
        color=color.blue
    )

    right = sphere(
        pos=vector(6+width*0.2,y,0),
        radius=width*0.22,
        color=color.blue
    )

    chromosome.extend([left,right])

label(
    pos=vector(0,-120,0),
    text='Metaphase Chromosome',
    box=False,
    height=20,
    color=color.white
)

# =========================================================
# ANIMATION
# =========================================================

theta = 0

while True:

    rate(40)

    theta += 0.03

    # rotate DNA
    for obj in dna_objects:

        obj.rotate(
            angle=0.008,
            axis=vector(0,1,0),
            origin=vector(0,20,0)
        )

    # nucleosome breathing
    for i,n in enumerate(nucleosomes):

        n.radius = 1.6 + 0.08*math.sin(theta*3+i)

    # loop oscillation
    for i,l in enumerate(loops):

        l.radius = 3 + 0.2*math.sin(theta+i)
