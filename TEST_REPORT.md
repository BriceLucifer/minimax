# Marimo Demonstration Test Report

Test date: 2026-09-13. Environment: macOS, Chrome, Python 3.14 and marimo 0.24.2.

## Conclusion

All checks in this test run passed, and no issues that would prevent the classroom demonstration were found. The previous issue that prevented **Next** from updating the display has been fixed and regression-tested through actual browser interactions.

## Browser Interactions

| Check | Result |
| --- | --- |
| Minimax: click Next repeatedly from 0 to 10 | Passed; root value 6, action c |
| Minimax: click Previous repeatedly from 10 to 0 | Passed |
| Alpha-beta: click Next repeatedly from 0 to 42 | Passed |
| Alpha-beta: click Previous repeatedly from 42 to 0 | Passed |
| Chance: click Next repeatedly from 0 to 4, then step back to 0 | Passed; root value 7, actions a and c tie |
| Restart in all three modes | Passed; returned to the initial state |
| Switch modes | Passed; progress reset with no answers carried over from the previous mode |
| Previous and Restart disabled in the initial state | Passed |
| Next disabled at the final state in all three modes | Passed |
| Browser error log | No errors found |
| Visual inspection of the desktop page | Tree, text and controls were visible with no obvious overlap |

The test completed 56 forward steps and 56 backward steps, for a total of 112 step transitions. Restarting and switching modes were also checked.

## Algorithm and Presentation

- Step 12 prunes A2 with **α = 6, β = 5**. Leaf m (9) is not visited, and A2 displays **≥6**.
- Step 23 prunes B with **α = 5, β = 2**. The leaves 8 and 7 under B2 are not visited, and B displays **≤2**.
- Alpha-beta ultimately visits j, k, l, n, o, r, s, t and u, corresponding to 3, 5, 6, 1, 2, 4, 6, 3 and 8: 9 of 12 leaves in total.
- B2 never displays a prematurely calculated exact value during the alpha-beta search.
- Chance mode uses the full tree and retains the lower-level MAX values: A = 7, B = 5 and C = 7.
- Every displayed alpha-beta node value or bound agrees with the exact value from an independent minimax calculation.

## Reproducible Automated Tests

[tests/test_minimax_visualizer.py](tests/test_minimax_visualizer.py) adds **six tests, all passing**, that cover answers and pruning, visited and pruned sets, bound correctness, mode-state isolation, stable state history, and the SVG structure and node shapes across all 59 frames.

```sh
.venv/bin/marimo check minimax_visualizer.py
.venv/bin/python -m unittest discover -s tests -v
```

The static notebook check passed. The automated tests cover the computation and rendering data; browser button interactions were verified through actual clicks during this test run and were not presented as unit tests.

## Test Scope

This test run covered the current fixed problem and desktop Chrome. Other browsers, mobile devices and first-time offline installation were not tested. An external step change occurred on the shared demonstration page partway through testing, so the complete alpha-beta flow was subsequently run again on an isolated test page and passed.
