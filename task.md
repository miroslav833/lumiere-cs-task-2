# Current attempt: 5 (four links, ratio of the largest 80 percent message size to the smallest)

Status: NOT YET RUN.

Instructions for the extension run:

1. Replace image.png on the form with this image.png. It has four links now.
2. Replace the prompt on the form with the prompt under "## Step 4. Prompt", exactly.
3. Wait for both blocks, log them as feedback/006.md in the usual layout. Both must be wrong. If
   either is right, stop and report.
4. Steps 7 to 11 will be written after both blocks fail. Do not press submit.

Why attempt 5 exists: attempt 4 (archive/attempt-4.md) ran twice on the same figure and question.
First run both models wrong, rerun with the reworded prompt one model right. Six critical readings
give about even odds per run. This attempt keeps the question type, keeps links A and B unchanged,
and adds a fourth link and a ranking, so the answer needs every link worked out and the readings
that decide it go from six to ten.

| Field | Value |
|---|---|
| Subdomain | Computer Systems |
| Where did the image(s) come from | Original - internal lab image |
| Source URL or DOI | N/A |
| License | Original - internal lab image |
| Reference material | N/A |
| Publication venue | N/A |
| Reference licence | N/A |
| Image | image.png |

---

## Step 4. Prompt

Image 1 is a log-log plot showing the effective bandwidth of four interconnect links, measured using a ping-pong microbenchmark, as a function of message size. The name of each link is indicated in the legend. Each measured data point is marked, and markers for the same link are connected by straight lines.

Calculate the ratio of the largest "$80\%$ message size" among the four links to the smallest "$80\%$ message size" among them. Here, a link's "$80\%$ message size" is defined as the minimum message size at which the link achieves exactly $80\%$ of its asymptotic bandwidth.

Follow these rules: A link's asymptotic bandwidth is defined as the bandwidth observed at the largest message size shown on the graph. Since every marker is located at the intersection of two grid lines, the values at these intersections are to be read and treated as exact. Because the curve between two adjacent markers appears as a straight line segment on the logarithmic axes of the plot, perform linear interpolation based on the logarithms of the message size and the bandwidth. The message size on the horizontal axis doubles with each grid line crossed, and $1 \, \text{KB}$ is calculated as $1024 \, \text{B}$.

The answer is a dimensionless ratio. Report your final answer as a 3 significant figure number without units. Any intermediate calculations should be carried out to 6 significant figures.

---

## Step 6. GTFA

21.6

---

## Checkboxes

| Statement | Answer |
|---|---|
| I've double checked my spelling and grammar. | True |
| My prompt is not duplicative, plagiarized, or LLM-generated. | Box 2 is mine, leave it |
| My prompt is self-contained and fully solvable without external resources. | True |
| The prompt can only be solved with the information in the image. | True |

Checker note: NON_FOUNDATIONAL_REFERENCE is a known false positive on every image task, record it
and continue. If GRAMMAR flags "3 significant figure number", dispute it, that sentence is the
project's mandated boilerplate.

---

## Ground truth

Four 80 percent sizes, then the largest over the smallest.

| link | plateau | target | bracket | t | 80 percent size |
|---|---|---|---|---|---|
| A | 90 | 72 | 64 KB (60) to 256 KB (80) | 0.633761 | 154.078 KB |
| B | 8 | 6.4 | 4 KB (6) to 16 KB (7) | 0.418672 | 7.14703 KB |
| C | 60 | 48 | 64 KB (40) to 256 KB (60) | 0.449660 | 119.372 KB |
| D | 7 | 5.6 | 4 KB (5) to 16 KB (6) | 0.621488 | 9.46872 KB |

Largest is A, smallest is B. Ratio = 154.078 / 7.14703 = 21.5584, so 21.6. Same value as attempt 4
by construction: links A and B are unchanged, and the model has to establish that A and B are the
extremes by working out C and D as well.

Axes. Horizontal: message size, 1 B to 1 MB, one vertical gridline per power of two, labels at
every power of four. Vertical: bandwidth in Gb/s, 0.001 to 100, only the decades labelled, minor
gridlines at 2 to 9 in each decade. Markers at every power of four only, radius 3.6 px at 1x.

| link | marker | 1 B | 4 B | 16 B | 64 B | 256 B | 1 KB | 4 KB | 16 KB | 64 KB | 256 KB | 1 MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | filled circle | 0.008 | 0.03 | 0.1 | 0.5 | 2 | 8 | 30 | 50 | 60 | 80 | 90 |
| B | open square | 0.005 | 0.02 | 0.08 | 0.3 | 1 | 3 | 6 | 7 | 8 | 8 | 8 |
| C | filled diamond | 0.003 | 0.01 | 0.05 | 0.2 | 0.8 | 2 | 9 | 30 | 40 | 60 | 60 |
| D | open circle | 0.004 | 0.007 | 0.04 | 0.4 | 0.6 | 4 | 5 | 6 | 7 | 7 | 7 |

Image is 3000 x 2000, rendered from SVG at 2x. Every marker centre was matched by script to the
gridline crossing for its value, all 44 within one pixel (tools/decode.py). No two links share a
crossing, and the closest pair of markers in one column is one minor line apart at the 7 to 8
spacing, where the marker edges are clear of each other.

## Where the levers are

1. Ten readings decide the answer instead of six. A (60, 80, 90) and B (6, 7, 8) as before, plus
   C's plateau at 60 and its 64 KB and 256 KB markers, and D's 4 KB, 16 KB and plateau markers.
   Every one of those slips by one minor line changes the answer by 6 percent or more.
2. B and D run parallel one minor line apart from 4 KB to 1 MB in the packed 5 to 8 band, open
   square over open circle. B's markers were misread in three of the four model runs on attempt 4.
3. C's plateau at 60 sits in the top decade next to A's 60 at 64 KB. Reading it as 70 makes C the
   largest link and moves the answer 31 percent.
4. The ranking is not visible by eye: C and A are both in the 100 to 160 KB range, B and D both
   in the 7 to 10 KB range.

## Wrong readings and where they land

Every single-marker slip to a neighbouring minor line was computed (tools/numbers.py). None lands
inside 2 percent. The ones that change the answer:

| slip | answer | off by |
|---|---|---|
| A 64 KB read as 50 or 70 | 26.3 or 16.7 | +22 or -23 percent |
| A 256 KB read as 70 or 90 | 41.8 or 16.7 | +94 or -23 percent |
| A plateau read as 80 or 100 | 16.7 or 35.8 | -23 or +66 percent |
| B 4 KB read as 5 or 7 | 16.3 or 44.6 | -25 or +107 percent |
| B 16 KB read as 6 or 8 | 16.3 or 28.2 | -25 or +31 percent |
| B plateau read as 7 or 9 | 44.2 or 16.3 | +105 or -25 percent |
| C 64 KB read as 30 | 22.9 | +6.3 percent |
| C 256 KB read as 50 | 27.8 | +29 percent |
| C plateau read as 70 | 28.3 | +31 percent |
| D 4 KB read as 6 | 48.8 | +126 percent |
| D 16 KB read as 7 | 24.1 | +12 percent |
| D plateau read as 6 | 49.6 | +130 percent |
| linear interpolation instead of log-log, a method error | 20.4 | -5.5 percent |

Slips on C and D in the other direction leave the ranking and the answer unchanged; they are listed
in the numbers.py output.
