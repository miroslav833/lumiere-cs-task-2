# Current attempt: 4 (log-log bandwidth against message size, ratio of the 80 percent sizes of links A and B)

Status: RUN, PASS. Both models wrong (Block 1: 16.3, Block 2: 7.75). Log in feedback/004.md. Form
completed on Handshake up to the submit button: final answer 21.6, format Decimal, image description,
model failure (both), justification of Block 1 (data extraction error), golden solution, references
N/A, five distractors (16.3, 7.75, 20.4, 26.3, 35.8), Science Judge disputed (it read the checkbox
text as the prompt). Not submitted, left for the human.

Attempts 1 to 3 were each solved by exactly one of the two models (logs in feedback/). Every run had
one misread marker in one model and none in the other. With three critical readings, one model
survives. Attempt 4 keeps the attempt 3 figure unchanged and asks for a ratio that needs six
critical readings, three in the packed 60 to 90 band of the top decade (link A, with link C crossing
it twice there) and three in the packed 6 to 8 band of the 1 to 10 decade (link B).

| Field | Value |
|---|---|
| Subdomain | Computer Systems |
| Where did the image(s) come from | Original - internal lab image |
| Source URL or DOI | N/A |
| License | Original - internal lab image |
| Reference material | N/A |
| Publication venue | N/A |
| Reference licence | N/A |
| Image | image.png (unchanged from attempt 3) |

---

## Step 4. Prompt

Image 1 is a log-log plot of the effective bandwidth of three interconnect links against message size, measured with a ping-pong microbenchmark. The links are named in the legend. Each measured point is drawn as a marker, and the markers of one link are joined by straight segments.

Find the ratio of the $80$ percent message size of link A to the $80$ percent message size of link B. The $80$ percent message size of a link is the smallest message size at which the link delivers exactly $80$ percent of its asymptotic bandwidth.

Use the following conventions. The asymptotic bandwidth of a link is its bandwidth at the largest message size on the plot. Every marker sits on a crossing of two gridlines, so take the reading of each marker at that crossing and treat the reading as exact. Between two neighbouring markers the curve is the straight segment drawn on the logarithmic axes of the figure, so interpolate linearly in the logarithm of message size and in the logarithm of bandwidth. Message sizes on the horizontal axis double from one gridline to the next, and $1 \, \text{KB}$ is $1024 \, \text{B}$.

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

Six readings on two curves, plus the legend, plus telling link A's filled circles from link C's
filled diamonds where the two cross.

| reading | value |
|---|---|
| link A at 1 MB, the asymptotic bandwidth | 90 Gb/s |
| link A at 64 KB | 60 Gb/s |
| link A at 256 KB | 80 Gb/s |
| link B at 1 MB, the asymptotic bandwidth | 8 Gb/s |
| link B at 4 KB | 6 Gb/s |
| link B at 16 KB | 7 Gb/s |

Link A: 80 percent of 90 is 72, between 64 KB (60) and 256 KB (80).
t = ln(72/60) / ln(80/60) = 0.182322 / 0.287682 = 0.633761; size = 64 x 4^t = 154.078 KB.
Link B: 80 percent of 8 is 6.4, between 4 KB (6) and 16 KB (7).
t = ln(6.4/6) / ln(7/6) = 0.0645385 / 0.154151 = 0.418672; size = 4 x 4^t = 7.14703 KB.
Ratio = 154.078 / 7.14703 = 21.5584, so 21.6.

Link C is not needed, but its curve runs through link A's two bracketing markers: at 64 KB the
circle (60) and the diamond (80) are two minor lines apart, at 256 KB the circle (80) and the
diamond (60) likewise. Link C's 80 percent size, for the record, is 23.04 KB.

Axes. Horizontal: message size, 1 B to 1 MB, one vertical gridline per power of two, labels at
every power of four. Vertical: bandwidth in Gb/s, 0.001 to 100, only the decades labelled, minor
gridlines at 2 to 9 in each decade. Markers at every power of four only.

| link | marker | 1 B | 4 B | 16 B | 64 B | 256 B | 1 KB | 4 KB | 16 KB | 64 KB | 256 KB | 1 MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | filled circle | 0.008 | 0.03 | 0.1 | 0.5 | 2 | 8 | 30 | 50 | 60 | 80 | 90 |
| B | open square | 0.005 | 0.02 | 0.08 | 0.3 | 1 | 3 | 6 | 7 | 8 | 8 | 8 |
| C | filled diamond | 0.003 | 0.01 | 0.05 | 0.2 | 0.8 | 2 | 9 | 40 | 80 | 60 | 60 |

Image is 3000 x 2000, rendered from SVG at 2x. Every marker centre was matched by script to the
gridline crossing for its value, all 33 within one pixel (tools/decode.py, PYTHONSAFEPATH=1).

## Where the levers are

1. Six critical readings instead of three. In attempts 1 to 3 each model misread about one packed-band
   marker per run; the chance that a model gets six clean is far lower than three.
2. Link B's three readings (6, 7, 8) sit in the 6 to 8 band of the 1 to 10 decade, 23 to 27 px between
   minor lines, none labelled, with link C's 9 at 4 KB one line above B's 6 region and link A's 8 at
   1 KB one line under B's plateau.
3. Link A's three readings (60, 80, 90) sit in the 60 to 90 band with link C crossing through both
   bracketing markers.
4. A ratio amplifies link B's slips: reading B's plateau as 9 or 7, or its 4 KB marker as 5 or 7,
   moves the ratio by 35 to 107 percent.
5. Habit trap: computing half-power sizes by reflex gives 6.76.
6. Linear interpolation lands at 20.4, which is wrong at 3 significant figures.

## Wrong readings and where they land

| slip | answer | off by |
|---|---|---|
| A: 64 KB marker taken from link C (80) | 6.56 | -70 percent |
| A: 256 KB marker taken from link C (60) | 66.8 | +210 percent |
| A: asymptotic bandwidth read as 100 | 35.8 | +66 percent |
| A: 64 KB marker read as 50 | 26.3 | +22 percent |
| B: asymptotic bandwidth read as 9 | 7.19 | -67 percent |
| B: asymptotic bandwidth read as 7 | 44.2 | +105 percent |
| B: 4 KB marker read as 5 | 13.9 | -35 percent |
| B: 4 KB marker read as 7 | 44.6 | +107 percent |
| B: 16 KB marker read as 8 | 28.2 | +31 percent |
| linear interpolation on both links, a method error | 20.4 | -5.5 percent |
| half-power sizes by habit | 6.76 | -69 percent |
