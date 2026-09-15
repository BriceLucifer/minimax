# Week 7 Tutorial | Games and Adversarial Search

**Team: Trible L**

Give students page 1 of the handout and keep page 2, which contains the answers. The English script below can be read aloud as written; the remaining text contains presentation cues. There is no need to ask questions or wait for students to respond.

## 0–5 Minutes: Set the Exercise

> We’re Team Trible L. The blue triangles are MAX nodes; the red triangles are MIN nodes.
>
> For part (a), work upward from the leaves. Fill in the internal values and choose the best root action.
>
> For part (b), restart from the root and search left to right. Mark the cutoffs, record alpha and beta, and count the leaves you visit.
>
> Spend about five minutes on these two parts. We’ll do part (c) together.

Let the students work on the exercise. If they get stuck, prompt them with: “MAX takes the larger value; MIN takes the smaller value.”

## 5–7 Minutes: Minimax

Select **(a) Minimax** in the visualizer and back up the values step by step.

> Start with the six lower MAX nodes. Their values are 5, 9, 2, 8, 6 and 8.
>
> At the MIN level, A takes the smaller of 5 and 9: 5. B takes the smaller of 2 and 8: 2. C takes the smaller of 6 and 8: 6.
>
> The root takes the largest of 5, 2 and 6. Its value is 6, so we choose action c, leading to C.

## 7–9 Minutes: Prune A2

Switch to **(b) Alpha-beta** and demonstrate from the beginning through **Step 12**, the first cutoff.

> Start with alpha at negative infinity and beta at positive infinity.
>
> A1 returns 5. A is MIN, so its beta becomes 5. A2 inherits this bound.
>
> A2 reads 6. As a MAX node, its value is now at least 6. A already has an option worth 5, so it will not choose A2.
>
> Alpha is 6 and beta is 5. Since alpha is greater than or equal to beta, we skip the leaf 9.
>
> We know only that A2 is at least 6. We have not calculated its exact value in this search.

Point to A2: **α = 6, β = 5**. Cross out branch **m**.

## 9–11 Minutes: Prune B

Continue through **Step 23**, the second cutoff.

> A returns 5, so the root’s alpha becomes 5. B inherits that bound.
>
> B1 reads 1 and 2, then returns 2. B is MIN, so its beta becomes 2. B can now offer at most 2.
>
> The root already has 5, so B cannot improve its choice. Alpha is 5 and beta is 2: we skip all of B2, including leaves 8 and 7.

Point to B: **α = 5, β = 2**. Cross out the B2 subtree under branch **g**.

## 11–12 Minutes: Complete the Search

Continue through **Step 42**, the end of the search.

> C1 returns 6. C2 reads 3 and 8, then returns 8. C returns the smaller value, 6.
>
> The root chooses action c, just as in minimax.
>
> We visited 9 of 12 leaves. We skipped one leaf under A2 and two under B2. A different visit order may change the amount of pruning, but not the root value.

## 12–15 Minutes: Chance Nodes

Switch to **(c) Chance**. Keep the lower-level MAX values and change A, B and C into circular chance nodes.

> Replace A, B and C with CHANCE nodes. Each child has probability one half, so we average the two child values.
>
> A becomes the average of 5 and 9: 7. B becomes the average of 2 and 8: 5. C becomes the average of 6 and 8: 7.
>
> The root still takes the maximum. Actions a and c now tie at 7. Action c is still optimal, but it is no longer the only best action.
>
> MIN chooses the worst outcome for MAX. CHANCE takes a probability-weighted average. The skipped branches matter again because they contribute to the expectation.
>
> This tree uses expectimax. A tree with MAX, MIN and CHANCE nodes uses expectiminimax.

After explaining each level or cutoff, pause for two or three seconds so students can fill in their handouts. If time is short, cover only these points for chance nodes: **7, 5, 7; a and c tie as the optimal actions; take the expected value instead of the minimum**.

## Answer Key

| Item | Result |
| --- | --- |
| Lower-level MAX | A1 = 5, A2 = 9, B1 = 2, B2 = 8, C1 = 6, C2 = 8 |
| MIN | A = 5, B = 2, C = 6 |
| Root value/action | 6/c |
| A2 cutoff | α = 6, β = 5; skip 9 (m) |
| B cutoff | α = 5, β = 2; skip B2 (g) |
| Visit order | 3, 5, 6, 1, 2, 4, 6, 3, 8; 9/12 total |
| CHANCE/root action | A = 7, B = 5, C = 7; a and c tie as the optimal actions |

## Interactive Demonstration

[minimax_visualizer.py](minimax_visualizer.py) is both a marimo notebook and an executable Python file. After selecting a problem, click **Next** to advance one step, **Previous** to go back and **Restart** to return to the beginning. Switching problems resets the progress. The original leaf scores remain visible at all times, but only leaves actually read by the search count as visited.

Create a local environment and start the visualizer from the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install "marimo==0.24.2"
.venv/bin/marimo run minimax_visualizer.py
```

To start it with uv on another computer (marimo will be downloaded the first time):

```sh
uvx marimo run --sandbox minimax_visualizer.py
```

To edit the notebook:

```sh
uvx marimo edit --sandbox minimax_visualizer.py
```

## Handout

- [PDF](output/pdf/minimax_handout.pdf): questions on page 1 and answers on page 2.
- [Typst source](minimax_handout.typ): diagrams drawn with CeTZ.

```sh
typst c minimax_handout.typ output/pdf/minimax_handout.pdf
```

For more information about marimo, see [Running notebooks](https://docs.marimo.io/guides/apps/) and [Button UI element](https://docs.marimo.io/api/inputs/button/).

## Testing

[The test report](TEST_REPORT.md) contains the step-by-step browser checks and algorithm verification results. Run the regression tests with:

```sh
.venv/bin/marimo check minimax_visualizer.py
.venv/bin/python -m unittest discover -s tests -v
```

## GitHub Actions and GitHub Pages

Workflow: [.github/workflows/pages.yml](.github/workflows/pages.yml).

- Pull requests check the notebook, run six regression tests and export the interactive web page without deploying it.
- Pushes to `main` automatically deploy to GitHub Pages after the checks pass.
- On the Actions page, you can also select `main` and click **Run workflow** to trigger the workflow manually.
- The workflow is pinned to Python 3.13 and marimo 0.24.2. When upgrading marimo, update both the dependency version in the Python file and the workflow.

For the initial setup, go to **Settings → Pages → Build and deployment → Source** in the GitHub repository, select **GitHub Actions** and push to `main`. No personal token is required. After a successful deployment, the website link is available in the `github-pages` deployment on the Actions page.

When creating a new repository, place the contents of this directory at the **new repository root**, including the hidden `.github/` directory. GitHub only recognizes `.github/workflows` at the repository root. The configuration also supports placing the notebook in a `tutorial/` subdirectory.

Commit the Python file, `tests/`, the workflow and the required `layouts/` files. Do not commit `.venv`, `__marimo__` or `output/web`; the web page is exported again by CI. Saved Slides layouts affect the export, so confirm that the local layout is correct before uploading it.

Implementation references: [Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [Exporting marimo notebooks to WebAssembly](https://docs.marimo.io/guides/exporting/webassembly_html/).
