# lumiere-cs-task-2

Lumiere task 2, Computer Systems. `task.md` and `image.png` on `main` are the current attempt, in
the layout of `lumiere-cs-task`. Model logs go to `feedback/`, questions to `ASKS.md`.

Attempt 7 (current, task.md): a task graph (20 tasks, 35 dependency arrows with delay labels, 59
crossings) scheduled by static list scheduling on four processors; the answer is the total
communication cost of the schedule, GTFA 105. Built after attempts 5 and 6 were both rejected on the
Pass@2 check: the reviewer's model reads the log-log figures at full resolution, so gridline packing
is not a lever there. Difficulty now sits in graph extraction plus a 20-step scheduling simulation. Both form models
wrong (90 and 78, `feedback/008.md`); form filled on Handshake to the submit button.
Tools: `tools/dag.py` (graph, scheduler, sensitivity; `python3 tools/dag.py search` scans seeds),
`tools/make_dag_fig.py` (annealed layout, render), `tools/dag_solution.py` (independent
re-derivation, writes the golden solution). Run them with `PYTHONSAFEPATH=1`.

Attempt 6 (archive/attempt-6-four-links-two-levels.md): four links, product over the links of the
ratio of the 80 percent message size to the 50 percent message size, GTFA 859, seventeen readings.
Both form models wrong (792 and 233, `feedback/007.md`), submitted, rejected on the Pass@2 check.

Attempt 5 (archive/attempt-5-product-ratio.md): three-link figure from attempt 3, product of the
ratio of link A's 80 percent message size to link B's and the ratio of link C's to link B's, GTFA
69.5, nine readings. Both form models wrong (3.29 and 15.0, `feedback/006.md`), submitted, rejected
on the Pass@2 check.

Attempt 4 (archive/attempt-4.md): three links, ratio of link A's 80 percent size to link B's, GTFA
21.6. First run both models wrong (`feedback/004.md`), rerun with the hand-reworded prompt one model
right (`feedback/005.md`). A four-link variant prepared for attempt 5 and not run is in
archive/attempt-5-four-links.md.

Earlier attempts, each solved by exactly one model: 1 (half-power point of link A, 8.73,
`feedback/001.md`), 2 (80 percent point of link A with readings in the 60 to 90 band, 85.7,
`feedback/002.md`), 3 (same with link C crossing link A twice, 154, `feedback/003.md`). The lesson
across them: each model misreads about one packed-band marker per run, so the lever is the number
of critical readings, not the tightness of any one of them.

`tools/` holds the figure generator and the decoder that checks every marker against its gridline
crossing: `CHROME=<chrome binary> python3 tools/make_fig.py`, then the same with `MARKERS_ONLY=1`
for the marker render, then `PYTHONSAFEPATH=1 python3 tools/decode.py`.

Retired before running: the branch predictor attempt (three panel figure, GTFA 1.79) at commit
54faa82 reused the task 1 figure template. Reference only, do not run it and do not rebuild it.
