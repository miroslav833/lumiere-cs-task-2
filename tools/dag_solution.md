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