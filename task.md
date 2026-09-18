# Attempt 7: task graph, static list scheduling on four processors, total communication cost

Status: NOT YET RUN on the form. Built 2026-09-18 after attempts 5 and 6 were both rejected with
"did not meet the required difficulty level and failed the Pass@2 check". GTFA 105.

Why the change of approach: attempts 1 to 6 all put the difficulty in reading packed gridlines on a
log-log plot. The two form models get a downscaled image and misread them; the reviewer's Pass@2
check evidently sees the figure at full resolution and does not, so adding more markers (9, then
17) did nothing there. Attempt 7 moves the difficulty to two places that do not depend on image
resolution: extracting a dense dependency graph (20 tasks, 35 arrows, 59 crossings, each arrow with
its own delay label) and then simulating static list scheduling with communication delays on four
processors, where the answer is the total communication cost of the schedule. Sensitivity
(tools/dag.py): dropping any one of 34 of the 35 arrows changes the answer, adding a spurious arrow
changes it 83 percent of the time, a one-off misread of a delay label changes it 77 percent of the
time, a one-off misread of an execution time changes it 31 of 40 times.

Instructions for the run:

1. On the form, edit the prompt step: replace image.png with the new image.png (task graph) and the
   prompt with the text under "## Step 4. Prompt", exactly. Editing the prompt step deletes every
   later answer and regenerates both blocks.
2. Wait for both blocks. Log them as feedback/008.md. Both must be wrong. If either is right, stop
   and report.
3. Fill steps 6 to 11 from this file. Replace two of the distractors with the models' wrong answers.
4. Do not press Submit.

| Field | Value |
|---|---|
| Subdomain | Computer Systems |
| Where did the image(s) come from | Original - internal lab image |
| Source URL or DOI | N/A |
| License | Original - internal lab image |
| Reference material | N/A |
| Publication venue | N/A |
| Reference licence | N/A |
| Image | image.png (sha256 0f66464d...) |

---

## Step 4. Prompt

Image 1 shows the task graph of a parallel program. Every node is a task; the text inside the node gives the task name and, under it, the execution time of the task in cycles. Every arrow is a data dependency from the task at its tail to the task at its head, and the number in the small box on an arrow is the communication delay of that dependency in cycles.

The program is to be scheduled on four identical processors, numbered P1 to P4, by static list scheduling with the following rules. The priority of a task is its bottom level: the largest sum of execution times along any path that starts at the task and ends at a task with no outgoing arrows, counting the task itself and every task on the path, and counting no communication delays. Tasks are placed one at a time in order of decreasing bottom level; when several tasks share the same bottom level, the one with the smaller task number is placed first. Every task is placed on the processor on which it can start earliest; if two or more processors allow the same earliest start, the processor with the smaller number is used. On a given processor, a task can start no earlier than the finish time of the task placed on that processor before it, and no earlier than the arrival of the data from each of its predecessors: data from a predecessor placed on the same processor arrive the moment that predecessor finishes, and data from a predecessor placed on a different processor arrive when the communication delay of that arrow has elapsed after the predecessor finishes. Tasks are appended to a processor in the order in which they are placed and are never inserted in front of a task placed earlier. Time starts at cycle 0, a task without predecessors may start at cycle 0, and every task runs without interruption once started.

Calculate the total communication cost of the resulting schedule, defined as the sum of the communication delays of all arrows whose two tasks are placed on different processors. Report your final answer as an integer number of cycles, without units.

---

## Step 6. GTFA

105

---

## Checkboxes

| Statement | Answer |
|---|---|
| I've double checked my spelling and grammar. | True |
| My prompt is not duplicative, plagiarized, or LLM-generated. | Box 2 is mine, leave it |
| My prompt is self-contained and fully solvable without external resources. | True |
| The prompt can only be solved with the information in the image. | True |

Checker note: NON_FOUNDATIONAL_REFERENCE is a known false positive on every image task, record it
and continue. The Science Judge on this task reads the wrong field as the prompt; dispute through
the Feedback panel (Disagree control on the card, write the reason, submit).

---

## Ground truth

Graph: tools/dag.py, seed 359, four processors. Execution times T1..T20: 3, 8, 9, 6, 8, 2, 3, 3,
5, 2, 2, 9, 4, 2, 5, 8, 5, 5, 8, 7. Arrows (tail to head, delay): see Step 1 of the golden solution.

Bottom levels: T3 34, T2 28, T5 25, T1 20, T7 20, T9 20, T11 19, T12 17, T13 17, T4 16, T16 15,
T6 13, T18 13, T15 12, T17 12, T8 11, T10 10, T14 10, T19 8, T20 7.

Schedule (processor, start, finish): P1: T3 0-9, T5 9-17, T12 23-32, T19 33-41. P2: T2 0-8,
T7 8-11, T9 13-18, T16 19-27, T10 29-31. P3: T1 0-3, T11 13-15, T4 15-21, T15 21-26, T8 26-29,
T14 29-31. P4: T13 14-18, T6 18-20, T18 20-25, T17 25-30, T20 34-41. Makespan 41.

Same-processor arrows (cost 0): T2-T7, T3-T5, T5-T12, T9-T16, T12-T19, T13-T18, T13-T20, T17-T20.
The other 27 arrows cross processors; their delays sum to 105.

Verified by two independent implementations (tools/dag.py and tools/dag_solution.py).

## Where the levers are

1. Graph extraction: 35 arrows with 59 crossings, several spanning two or three rows, each with a
   one-digit delay box. A single missed, added or misattached arrow changes the answer almost always.
2. The schedule itself: 20 placements, each comparing four candidate start times that mix processor
   availability with per-predecessor arrival times (same processor 0, other processor the delay).
   Ties on bottom level (T1, T7, T9 at 20; T12, T13 at 17; T6, T18 at 13; T15, T17 at 12; T10, T14
   at 10) and ties on start time (T3, T2, T1, T9, T11, T10) all have to be broken the stated way.
3. The answer depends on every placement, not only on the critical path, so a slip anywhere shows.

## Wrong answers and where they land

| mistake | answer |
|---|---|
| sum of every delay, ignoring placement | 152 |
| bottom-level ties broken toward the larger task number | 97 |
| task sent to the first free processor instead of the earliest start | 85 |
| tasks inserted into idle gaps instead of appended | 84 |
| makespan reported instead of the communication cost | 41 |
| three processors instead of four | 67 |

---

## Step 7. Image description

Image 1 is a self-authored schematic figure on a plain white background at $3000 \times 2000$ pixels, drawn in black. It is a directed acyclic task graph, not a photograph or a data plot, so there is no modality, magnification or axis to report.

The graph has twenty circular nodes arranged in six rows. Inside each circle the task name is printed in bold and its execution time in cycles is printed underneath. Row 1, at the top, left to right: T2 with execution time 8, T1 with execution time 3, T3 with execution time 9. Row 2: T7 with 3, T4 with 6, T6 with 2, T5 with 8. Row 3: T11 with 2, T8 with 3, T9 with 5, T10 with 2. Row 4: T13 with 4, T12 with 9, T15 with 5, T14 with 2. Row 5: T17 with 5, T18 with 5, T16 with 8. Row 6, at the bottom: T19 with 8, T20 with 7.

There are thirty five straight arrows, every one pointing downward from a task in a higher row to a task in a lower row. Each arrow carries a small white box with a single digit, the communication delay of that dependency in cycles. Listed by the task at the tail, with the head task and the delay in brackets: from T1 to T6 (3) and to T13 (4). From T2 to T4 (4), to T6 (6), to T7 (6), to T11 (5) and to T15 (5). From T3 to T5 (2) and to T9 (4). From T4 to T10 (8). From T5 to T12 (8), to T14 (1) and to T16 (2). From T6 to T8 (6), to T10 (2) and to T14 (1). From T7 to T12 (5), to T13 (3) and to T14 (8). From T8 to T19 (2). From T9 to T16 (9), to T17 (1) and to T19 (4). From T10 to T19 (1). From T11 to T12 (8) and to T17 (3). From T12 to T19 (4). From T13 to T18 (7) and to T20 (3). From T14 to T19 (2) and to T20 (3). From T15 to T20 (5). From T16 to T20 (7). From T17 to T20 (8). From T18 to T19 (2). T1, T2 and T3 have no incoming arrows; T19 and T20 have no outgoing arrows.

Many arrows cross one another, and several span two or three rows, but no arrow passes through a node and every delay box sits clear of the other arrows and nodes. A caption line under the graph reads "Task graph: node = task (name, execution time in cycles); arrow = data dependency (label = communication delay in cycles)". There is no colour, shading, highlight or other annotation.

---

## Step 8. Model failure mode

Fill after the blocks return. Expected: "Connectivity / topology error" (arrow attached to the
wrong node, arrow missed or invented) or "Data extraction error" (delay label read from the wrong
arrow). A pure simulation slip with a correctly read graph would be a reasoning error; justify from
the actual response.

---

## Step 9. Step-by-step solution

Step 1. Read the graph. The twenty tasks and their execution times are T1: 3, T2: 8, T3: 9, T4: 6, T5: 8, T6: 2, T7: 3, T8: 3, T9: 5, T10: 2, T11: 2, T12: 9, T13: 4, T14: 2, T15: 5, T16: 8, T17: 5, T18: 5, T19: 8, T20: 7. The thirty five dependency arrows, written as tail to head with the communication delay in brackets, are T1 to T6 (3), T1 to T13 (4), T2 to T4 (4), T2 to T6 (6), T2 to T7 (6), T2 to T11 (5), T2 to T15 (5), T3 to T5 (2), T3 to T9 (4), T4 to T10 (8), T5 to T12 (8), T5 to T14 (1), T5 to T16 (2), T6 to T8 (6), T6 to T10 (2), T6 to T14 (1), T7 to T12 (5), T7 to T13 (3), T7 to T14 (8), T8 to T19 (2), T9 to T16 (9), T9 to T17 (1), T9 to T19 (4), T10 to T19 (1), T11 to T12 (8), T11 to T17 (3), T12 to T19 (4), T13 to T18 (7), T13 to T20 (3), T14 to T19 (2), T14 to T20 (3), T15 to T20 (5), T16 to T20 (7), T17 to T20 (8), T18 to T19 (2).

Step 2. Compute the bottom level of every task, working from the exit tasks upward: a task's bottom level is its execution time plus the largest bottom level among its successors. T20: 7 (no successors); T19: 8 (no successors); T18: 5 + max(8) = 13; T17: 5 + max(7) = 12; T16: 8 + max(7) = 15; T15: 5 + max(7) = 12; T14: 2 + max(8, 7) = 10; T13: 4 + max(13, 7) = 17; T12: 9 + max(8) = 17; T11: 2 + max(17, 12) = 19; T10: 2 + max(8) = 10; T9: 5 + max(15, 12, 8) = 20; T8: 3 + max(8) = 11; T7: 3 + max(17, 17, 10) = 20; T6: 2 + max(11, 10, 10) = 13; T5: 8 + max(17, 10, 15) = 25; T4: 6 + max(10) = 16; T3: 9 + max(25, 20) = 34; T2: 8 + max(16, 13, 20, 19, 12) = 28; T1: 3 + max(13, 17) = 20.

Step 3. Order the tasks by decreasing bottom level, smaller task number first among equals: T3 (34), T2 (28), T5 (25), T1 (20), T7 (20), T9 (20), T11 (19), T12 (17), T13 (17), T4 (16), T16 (15), T6 (13), T18 (13), T15 (12), T17 (12), T8 (11), T10 (10), T14 (10), T19 (8), T20 (7).

Step 4. Place T3 (execution time 9). P1: free at 0, start 0; P2: free at 0, start 0; P3: free at 0, start 0; P4: free at 0, start 0. Earliest start is 0 on P1 (tie, smaller processor number), so T3 runs on P1 from 0 to 9.

Step 5. Place T2 (execution time 8). P1: free at 9, start 9; P2: free at 0, start 0; P3: free at 0, start 0; P4: free at 0, start 0. Earliest start is 0 on P2 (tie, smaller processor number), so T2 runs on P2 from 0 to 8.

Step 6. Place T5 (execution time 8). P1: free at 9, data T3 at 9 (same processor), start 9; P2: free at 8, data T3 at 11 (9 + 2), start 11; P3: free at 0, data T3 at 11 (9 + 2), start 11; P4: free at 0, data T3 at 11 (9 + 2), start 11. Earliest start is 9 on P1, so T5 runs on P1 from 9 to 17.

Step 7. Place T1 (execution time 3). P1: free at 17, start 17; P2: free at 8, start 8; P3: free at 0, start 0; P4: free at 0, start 0. Earliest start is 0 on P3 (tie, smaller processor number), so T1 runs on P3 from 0 to 3.

Step 8. Place T7 (execution time 3). P1: free at 17, data T2 at 14 (8 + 6), start 17; P2: free at 8, data T2 at 8 (same processor), start 8; P3: free at 3, data T2 at 14 (8 + 6), start 14; P4: free at 0, data T2 at 14 (8 + 6), start 14. Earliest start is 8 on P2, so T7 runs on P2 from 8 to 11.

Step 9. Place T9 (execution time 5). P1: free at 17, data T3 at 9 (same processor), start 17; P2: free at 11, data T3 at 13 (9 + 4), start 13; P3: free at 3, data T3 at 13 (9 + 4), start 13; P4: free at 0, data T3 at 13 (9 + 4), start 13. Earliest start is 13 on P2 (tie, smaller processor number), so T9 runs on P2 from 13 to 18.

Step 10. Place T11 (execution time 2). P1: free at 17, data T2 at 13 (8 + 5), start 17; P2: free at 18, data T2 at 8 (same processor), start 18; P3: free at 3, data T2 at 13 (8 + 5), start 13; P4: free at 0, data T2 at 13 (8 + 5), start 13. Earliest start is 13 on P3 (tie, smaller processor number), so T11 runs on P3 from 13 to 15.

Step 11. Place T12 (execution time 9). P1: free at 17, data T5 at 17 (same processor), T7 at 16 (11 + 5), T11 at 23 (15 + 8), start 23; P2: free at 18, data T5 at 25 (17 + 8), T7 at 11 (same processor), T11 at 23 (15 + 8), start 25; P3: free at 15, data T5 at 25 (17 + 8), T7 at 16 (11 + 5), T11 at 15 (same processor), start 25; P4: free at 0, data T5 at 25 (17 + 8), T7 at 16 (11 + 5), T11 at 23 (15 + 8), start 25. Earliest start is 23 on P1, so T12 runs on P1 from 23 to 32.

Step 12. Place T13 (execution time 4). P1: free at 32, data T1 at 7 (3 + 4), T7 at 14 (11 + 3), start 32; P2: free at 18, data T1 at 7 (3 + 4), T7 at 11 (same processor), start 18; P3: free at 15, data T1 at 3 (same processor), T7 at 14 (11 + 3), start 15; P4: free at 0, data T1 at 7 (3 + 4), T7 at 14 (11 + 3), start 14. Earliest start is 14 on P4, so T13 runs on P4 from 14 to 18.

Step 13. Place T4 (execution time 6). P1: free at 32, data T2 at 12 (8 + 4), start 32; P2: free at 18, data T2 at 8 (same processor), start 18; P3: free at 15, data T2 at 12 (8 + 4), start 15; P4: free at 18, data T2 at 12 (8 + 4), start 18. Earliest start is 15 on P3, so T4 runs on P3 from 15 to 21.

Step 14. Place T16 (execution time 8). P1: free at 32, data T5 at 17 (same processor), T9 at 27 (18 + 9), start 32; P2: free at 18, data T5 at 19 (17 + 2), T9 at 18 (same processor), start 19; P3: free at 21, data T5 at 19 (17 + 2), T9 at 27 (18 + 9), start 27; P4: free at 18, data T5 at 19 (17 + 2), T9 at 27 (18 + 9), start 27. Earliest start is 19 on P2, so T16 runs on P2 from 19 to 27.

Step 15. Place T6 (execution time 2). P1: free at 32, data T1 at 6 (3 + 3), T2 at 14 (8 + 6), start 32; P2: free at 27, data T1 at 6 (3 + 3), T2 at 8 (same processor), start 27; P3: free at 21, data T1 at 3 (same processor), T2 at 14 (8 + 6), start 21; P4: free at 18, data T1 at 6 (3 + 3), T2 at 14 (8 + 6), start 18. Earliest start is 18 on P4, so T6 runs on P4 from 18 to 20.

Step 16. Place T18 (execution time 5). P1: free at 32, data T13 at 25 (18 + 7), start 32; P2: free at 27, data T13 at 25 (18 + 7), start 27; P3: free at 21, data T13 at 25 (18 + 7), start 25; P4: free at 20, data T13 at 18 (same processor), start 20. Earliest start is 20 on P4, so T18 runs on P4 from 20 to 25.

Step 17. Place T15 (execution time 5). P1: free at 32, data T2 at 13 (8 + 5), start 32; P2: free at 27, data T2 at 8 (same processor), start 27; P3: free at 21, data T2 at 13 (8 + 5), start 21; P4: free at 25, data T2 at 13 (8 + 5), start 25. Earliest start is 21 on P3, so T15 runs on P3 from 21 to 26.

Step 18. Place T17 (execution time 5). P1: free at 32, data T9 at 19 (18 + 1), T11 at 18 (15 + 3), start 32; P2: free at 27, data T9 at 18 (same processor), T11 at 18 (15 + 3), start 27; P3: free at 26, data T9 at 19 (18 + 1), T11 at 15 (same processor), start 26; P4: free at 25, data T9 at 19 (18 + 1), T11 at 18 (15 + 3), start 25. Earliest start is 25 on P4, so T17 runs on P4 from 25 to 30.

Step 19. Place T8 (execution time 3). P1: free at 32, data T6 at 26 (20 + 6), start 32; P2: free at 27, data T6 at 26 (20 + 6), start 27; P3: free at 26, data T6 at 26 (20 + 6), start 26; P4: free at 30, data T6 at 20 (same processor), start 30. Earliest start is 26 on P3, so T8 runs on P3 from 26 to 29.

Step 20. Place T10 (execution time 2). P1: free at 32, data T4 at 29 (21 + 8), T6 at 22 (20 + 2), start 32; P2: free at 27, data T4 at 29 (21 + 8), T6 at 22 (20 + 2), start 29; P3: free at 29, data T4 at 21 (same processor), T6 at 22 (20 + 2), start 29; P4: free at 30, data T4 at 29 (21 + 8), T6 at 20 (same processor), start 30. Earliest start is 29 on P2 (tie, smaller processor number), so T10 runs on P2 from 29 to 31.

Step 21. Place T14 (execution time 2). P1: free at 32, data T5 at 17 (same processor), T6 at 21 (20 + 1), T7 at 19 (11 + 8), start 32; P2: free at 31, data T5 at 18 (17 + 1), T6 at 21 (20 + 1), T7 at 11 (same processor), start 31; P3: free at 29, data T5 at 18 (17 + 1), T6 at 21 (20 + 1), T7 at 19 (11 + 8), start 29; P4: free at 30, data T5 at 18 (17 + 1), T6 at 20 (same processor), T7 at 19 (11 + 8), start 30. Earliest start is 29 on P3, so T14 runs on P3 from 29 to 31.

Step 22. Place T19 (execution time 8). P1: free at 32, data T8 at 31 (29 + 2), T9 at 22 (18 + 4), T10 at 32 (31 + 1), T12 at 32 (same processor), T14 at 33 (31 + 2), T18 at 27 (25 + 2), start 33; P2: free at 31, data T8 at 31 (29 + 2), T9 at 18 (same processor), T10 at 31 (same processor), T12 at 36 (32 + 4), T14 at 33 (31 + 2), T18 at 27 (25 + 2), start 36; P3: free at 31, data T8 at 29 (same processor), T9 at 22 (18 + 4), T10 at 32 (31 + 1), T12 at 36 (32 + 4), T14 at 31 (same processor), T18 at 27 (25 + 2), start 36; P4: free at 30, data T8 at 31 (29 + 2), T9 at 22 (18 + 4), T10 at 32 (31 + 1), T12 at 36 (32 + 4), T14 at 33 (31 + 2), T18 at 25 (same processor), start 36. Earliest start is 33 on P1, so T19 runs on P1 from 33 to 41.

Step 23. Place T20 (execution time 7). P1: free at 41, data T13 at 21 (18 + 3), T14 at 34 (31 + 3), T15 at 31 (26 + 5), T16 at 34 (27 + 7), T17 at 38 (30 + 8), start 41; P2: free at 31, data T13 at 21 (18 + 3), T14 at 34 (31 + 3), T15 at 31 (26 + 5), T16 at 27 (same processor), T17 at 38 (30 + 8), start 38; P3: free at 31, data T13 at 21 (18 + 3), T14 at 31 (same processor), T15 at 26 (same processor), T16 at 34 (27 + 7), T17 at 38 (30 + 8), start 38; P4: free at 30, data T13 at 18 (same processor), T14 at 34 (31 + 3), T15 at 31 (26 + 5), T16 at 34 (27 + 7), T17 at 30 (same processor), start 34. Earliest start is 34 on P4, so T20 runs on P4 from 34 to 41.

Step 24. Final placement: P1: T3 [0, 9], T5 [9, 17], T12 [23, 32], T19 [33, 41]; P2: T2 [0, 8], T7 [8, 11], T9 [13, 18], T16 [19, 27], T10 [29, 31]; P3: T1 [0, 3], T11 [13, 15], T4 [15, 21], T15 [21, 26], T8 [26, 29], T14 [29, 31]; P4: T13 [14, 18], T6 [18, 20], T18 [20, 25], T17 [25, 30], T20 [34, 41]. Makespan 41.

Step 25. List the arrows whose two tasks are on the same processor, which cost nothing: T2 to T7, T3 to T5, T5 to T12, T9 to T16, T12 to T19, T13 to T18, T13 to T20, T17 to T20.

Step 26. Add the delays of the remaining arrows, whose two tasks are on different processors: 3 + 4 + 4 + 6 + 5 + 5 + 4 + 8 + 1 + 2 + 6 + 2 + 1 + 5 + 3 + 8 + 2 + 1 + 4 + 1 + 8 + 3 + 2 + 3 + 5 + 7 + 2 = 105.


Final answer: 105

---

## Step 10. Distractors

Replace the first two with the models' wrong answers once the blocks return.

1. 152 (sum of every delay, placement ignored)
2. 85 (task sent to the first free processor)
3. 97 (bottom-level ties broken the other way)
4. 84 (insertion into idle gaps)
5. 41 (the makespan)

---

## Step 11. Answer format and tolerance

Integer, 105, no units. Exact match; every listed mistake lands at least 8 away.
