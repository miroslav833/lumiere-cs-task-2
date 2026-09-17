# lumiere-cs-task-2

Lumiere task 2, Computer Systems. `task.md` and `image.png` on `main` are the current attempt, in
the layout of `lumiere-cs-task`. Model logs go to `feedback/`, questions to `ASKS.md`.

Attempt 4 (current, PASS): one-panel log-log plot of effective bandwidth against message size for
three links, question is the ratio of the 80 percent message size of link A to that of link B,
GTFA 21.6. Both models wrong (16.3 and 7.75). Six critical readings, three in the packed 60 to 90
band of the top decade with link C crossing link A twice there, three in the packed 6 to 8 band of
the 1 to 10 decade. Log in `feedback/004.md`. Form filled on Handshake up to the submit button.

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
