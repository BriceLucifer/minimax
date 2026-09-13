# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo==0.24.2"]
# ///
"""Week 7 teaching demo. Run: marimo run minimax_visualizer.py."""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="full", app_title="Week 7 · Adversarial Search")


@app.cell
def _():
    import marimo as mo
    from copy import deepcopy
    from html import escape
    from math import inf

    return deepcopy, escape, inf, mo


@app.cell
def _(deepcopy, inf):
    # One source of truth, matching the handout exactly.
    children = {
        "Root": ["A", "B", "C"],
        "A": ["A1", "A2"], "B": ["B1", "B2"], "C": ["C1", "C2"],
        "A1": ["j", "k"], "A2": ["l", "m"],
        "B1": ["n", "o"], "B2": ["p", "q"],
        "C1": ["r", "s"], "C2": ["t", "u"],
    }
    utilities = dict(zip("jklmnopqrstu", [3, 5, 6, 9, 1, 2, 8, 7, 4, 6, 3, 8]))
    lower_nodes = ["A1", "A2", "B1", "B2", "C1", "C2"]
    middle_nodes = ["A", "B", "C"]
    edges = [(parent, child) for parent, kids in children.items() for child in kids]
    edge_labels = dict(zip(edges, "abcdefghijklmnopqrstu"))

    def format_number(value):
        return "−∞" if value == -inf else "+∞" if value == inf else f"{value:g}"

    def interval_label(low, high):
        if low == high:
            return format_number(low)
        if high == inf:
            return "≥" + format_number(low)
        if low == -inf:
            return "≤" + format_number(high)
        return f"[{low:g}, {high:g}]"

    def build_trace(mode):
        frames = []
        state = dict(values={}, seen=[], pruned=set(), active="Root", bounds=None,
                     best=[], cuts=[], event="Ready", message="", equation="")

        def emit(event, active, message, equation="", bounds=None):
            state.update(event=event, active=active, message=message,
                         equation=equation, bounds=bounds)
            frames.append(deepcopy(state))

        def descendants(node):
            return {node}.union(*(descendants(c) for c in children.get(node, [])))

        if mode == "minimax":
            emit("Start at the leaves", None, "Fill the six lower MAX nodes, then A, B, C, then the root.")
            for node in lower_nodes + middle_nodes + ["Root"]:
                kids = children[node]
                vals = [utilities[k] if k in utilities else int(state["values"][k]) for k in kids]
                is_min = node in middle_nodes
                value = min(vals) if is_min else max(vals)
                state["values"][node] = str(value)
                state["seen"].extend(k for k in kids if k in utilities)
                if node == "Root":
                    state["best"] = ["c"]
                emit(f"Back up {node}", node,
                     "MIN takes the smaller value." if is_min else "MAX takes the largest child value.",
                     f"{node} = {'min' if is_min else 'max'}({', '.join(map(str, vals))}) = {value}")
            return frames

        if mode == "chance":
            for node in lower_nodes:
                state["values"][node] = str(max(utilities[k] for k in children[node]))
            emit("Replace MIN with CHANCE", None,
                 "Keep the six lower MAX values. Use the full tree; each chance edge has probability ½.")
            for node in middle_nodes:
                vals = [int(state["values"][k]) for k in children[node]]
                value = sum(vals) / 2
                state["values"][node] = format_number(value)
                emit(f"Average at {node}", node, "CHANCE takes the probability-weighted average.",
                     f"{node} = ½ × {vals[0]} + ½ × {vals[1]} = {value:g}")
            state["values"]["Root"] = "7"
            state["best"] = ["a", "c"]
            emit("Two optimal actions", "Root", "a and c tie. c is still optimal, but it is no longer unique.",
                 "Root = max(7, 5, 7) = 7")
            return frames

        if mode != "alphabeta":
            raise ValueError(f"Unknown mode: {mode}")
        emit("Restart the search", "Root", "Search left to right. No internal values are carried over from part (a).",
             bounds=(-inf, inf))

        def visit(node, alpha, beta):
            if node in utilities:
                state["seen"].append(node)
                value = utilities[node]
                emit(f"Read leaf {node}", node, f"Evaluate {value}. This leaf now counts as visited.",
                     bounds=(alpha, beta))
                return value, value, value
            is_min = node in middle_nodes
            value = inf if is_min else -inf
            intervals = []
            kids = children[node]
            emit(f"Enter {node}", node, "Inherit the search bounds from the parent.", bounds=(alpha, beta))
            for index, child in enumerate(kids):
                result, low, high = visit(child, alpha, beta)
                intervals.append((low, high))
                value = min(value, result) if is_min else max(value, result)
                if is_min:
                    beta = min(beta, value)
                else:
                    alpha = max(alpha, value)
                remaining = kids[index + 1:]
                if alpha >= beta and remaining:
                    for skipped in remaining:
                        state["pruned"].update(descendants(skipped))
                        intervals.append((-inf, inf))
                    state["cuts"].append((node, alpha, beta))
                    lo = min(i[0] for i in intervals) if is_min else max(i[0] for i in intervals)
                    hi = min(i[1] for i in intervals) if is_min else max(i[1] for i in intervals)
                    state["values"][node] = interval_label(lo, hi)
                    explanation = ("A already has 5. A2 can only be 6 or higher: skip leaf m (9)."
                                   if node == "A2" else
                                   "The root already has 5. B can offer at most 2: skip B2, including 8 and 7.")
                    emit(f"Cutoff at {node}", node, explanation,
                         f"α = {format_number(alpha)} ≥ β = {format_number(beta)}", (alpha, beta))
                    return value, lo, hi
                emit(f"Update {node}", node,
                     f"{child} returns {format_number(result)}. Update {'β' if is_min else 'α'} at {node}.",
                     f"Current best at {node}: {format_number(value)}", (alpha, beta))
            lo = min(i[0] for i in intervals) if is_min else max(i[0] for i in intervals)
            hi = min(i[1] for i in intervals) if is_min else max(i[1] for i in intervals)
            state["values"][node] = interval_label(lo, hi)
            if node == "Root":
                state["best"] = ["c"]
            emit(f"Return from {node}", node,
                 "Choose c. 9 of 12 leaves evaluated; 3 pruned." if node == "Root"
                 else f"Return {format_number(value)} to the parent.",
                 f"{node}: {state['values'][node]}", (alpha, beta))
            return value, lo, hi

        visit("Root", -inf, inf)
        return frames

    def verify_demo():
        """Check conclusions, cutoff windows, and absence of leaked exact values."""
        mm, ab, ch = (build_trace(m) for m in ("minimax", "alphabeta", "chance"))
        assert mm[-1]["values"] == dict(zip(lower_nodes + middle_nodes + ["Root"],
                                               map(str, [5, 9, 2, 8, 6, 8, 5, 2, 6, 6])))
        assert ab[-1]["cuts"] == [("A2", 6, 5), ("B", 5, 2)]
        assert ab[-1]["seen"] == list("jklnorstu")
        assert ab[-1]["pruned"] == {"m", "B2", "p", "q"}
        assert ab[-1]["values"]["Root"] == "6"
        assert ab[-1]["values"]["A2"] == "≥6"
        assert ab[-1]["values"]["B"] == "≤2"
        assert all("B2" not in f["values"] for f in ab)
        assert all(set(f["seen"]).isdisjoint(f["pruned"]) for f in ab)
        assert [ch[-1]["values"][n] for n in middle_nodes + ["Root"]] == ["7", "5", "7", "7"]
        assert ch[-1]["best"] == ["a", "c"]
        assert all(not f["pruned"] for f in ch)
        return {"minimax": len(mm), "alphabeta": len(ab), "chance": len(ch)}

    return (
        build_trace,
        edge_labels,
        edges,
        format_number,
        lower_nodes,
        middle_nodes,
        utilities,
    )


@app.cell
def _(
    edge_labels,
    edges,
    escape,
    format_number,
    lower_nodes,
    middle_nodes,
    utilities,
):
    def render_frame(frame, mode, index, total):
        blue, red, ink, grey = "#246BEB", "#E23D45", "#253448", "#8B95A3"
        pos = {"Root": (465, 70), "A": (145, 215), "B": (465, 215), "C": (785, 215)}
        pos.update({n: (65 + i * 160, 360) for i, n in enumerate(lower_nodes)})
        pos.update({n: (25 + i * 80, 490) for i, n in enumerate(utilities)})
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-15 0 990 545" '
               'role="img" aria-label="Game tree showing the current calculation" '
               'style="width:100%;height:auto;display:block;font-family:Georgia,serif">']
        for parent, child in edges:
            x, y = pos[parent]
            xx, yy = pos[child]
            label = edge_labels[parent, child]
            skipped = child in frame["pruned"]
            winning = parent == "Root" and label in frame["best"]
            color = blue if winning else "#B8BEC6" if skipped else grey
            dash = 'stroke-dasharray="6 5"' if skipped else ""
            svg.append(f'<line x1="{x}" y1="{y}" x2="{xx}" y2="{yy}" '
                       f'stroke="{color}" stroke-width="{3 if winning else 1.6}" {dash}/>')
            lx, ly = (x + xx) / 2, (y + yy) / 2
            label = f"{label} · ½" if mode == "chance" and parent in middle_nodes else label
            svg.append(f'<rect x="{lx-23}" y="{ly-10}" width="46" height="21" fill="white"/>')
            svg.append(f'<text x="{lx}" y="{ly+5}" text-anchor="middle" font-size="15" fill="{color}">{label}</text>')
            if skipped:
                svg.append(f'<path d="M {lx-7} {ly-8} l 14 16 M {lx+7} {ly-8} l -14 16" stroke="{red}" stroke-width="2"/>')
        for node, (x, y) in pos.items():
            is_leaf, is_min = node in utilities, node in middle_nodes
            chance = is_min and mode == "chance"
            color = "#997016" if chance else red if is_min else grey if is_leaf else blue
            skipped, active = node in frame["pruned"], frame["active"] == node
            fill = "#FFF5D6" if active else "white"
            opacity = "0.4" if skipped else "1"
            svg.append(f'<g opacity="{opacity}">')
            if is_leaf or chance:
                radius = 19 if is_leaf else 35
                if is_leaf and node in frame["seen"]:
                    fill = "#EBF2FF" if not active else fill
                svg.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{color}" stroke-width="{3 if active else 1.8}"/>')
            else:
                d = -1 if is_min else 1
                svg.append(f'<polygon points="{x},{y-d*39} {x-45},{y+d*29} {x+45},{y+d*29}" '
                           f'fill="{fill}" stroke="{color}" stroke-width="{3 if active else 1.8}"/>')
            value = str(utilities[node]) if is_leaf else frame["values"].get(node, "—")
            text_y = y + 6 if chance or is_leaf else y + (9 if not is_min else -3)
            svg.append(f'<text x="{x}" y="{text_y}" text-anchor="middle" font-size="{20 if is_leaf else 22}" fill="{ink}">{escape(value)}</text>')
            if not is_leaf:
                svg.append(f'<text x="{x+49}" y="{y-10}" font-size="16" font-weight="bold" fill="{color}">{node}</text>')
            elif node in frame["seen"]:
                order = frame["seen"].index(node) + 1
                svg.append(f'<text x="{x}" y="{y+38}" text-anchor="middle" font-size="12" fill="{blue}">#{order}</text>')
            svg.append('</g>')
        svg.append('</svg>')
        bounds = frame["bounds"]
        bound_html = (f'<div class="bounds"><span style="color:{blue}">α = {format_number(bounds[0])}</span>'
                      f'<span style="color:{red}">β = {format_number(bounds[1])}</span></div>' if bounds else "")
        sequence = " → ".join(f"{n}({utilities[n]})" for n in frame["seen"]) or "—"
        cut_count = len(frame["pruned"].intersection(utilities))
        stats = ("Lower MAX values retained · p = ½" if mode == "chance" else
                 f'{len(frame["seen"])} / 12 leaves evaluated · {cut_count} pruned')
        outcome = f'<p class="outcome">Best action: {" or ".join(frame["best"])} · Root value: {frame["values"]["Root"]}</p>' if frame["best"] else ""
        history = "".join(f'<li>{n}: α={format_number(a)}, β={format_number(b)}</li>' for n, a, b in frame["cuts"])
        return f'''<div class="demo-frame">
          <div class="tree">{''.join(svg)}</div>
          <aside class="explanation">
            <div class="step-label">STEP {index} / {total}</div>
            <h2>{escape(frame['event'])}</h2>
            {bound_html}
            <p>{escape(frame['message'])}</p>
            <p class="equation">{escape(frame['equation'])}</p>
            {outcome}
            <div class="stats">{stats}</div>
            {f'<p class="sequence">Visit order: {sequence}</p>' if mode != 'chance' else ''}
            {f'<ul class="cutoffs">{history}</ul>' if history else ''}
          </aside>
        </div>'''

    return (render_frame,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html('''<style>
    body {background:white !important;}
    .marimo {--monospace-font: ui-monospace, monospace; --text-font: Georgia,"Times New Roman",serif;}
    marimo-button button,marimo-radio label {font-family:Georgia,"Times New Roman",serif !important;font-size:16px;}
    marimo-button button {min-height:38px;padding:8px 16px;}
    .nav-count {font:15px Georgia,"Times New Roman",serif;color:#657080;margin-left:10px;}
    .marimo [role="radiogroup"] {font:16px Georgia,"Times New Roman",serif;}
    .demo-header,.demo-frame {font-family:Georgia,"Times New Roman",serif;color:#253448;}
    .demo-header {display:flex;justify-content:space-between;align-items:baseline;gap:20px;margin:8px 0 12px;}
    .demo-header h1 {font-size:28px;margin:0;font-weight:600;letter-spacing:-.025em;}
    .demo-header span {font-size:15px;white-space:nowrap;color:#657080;}
    .demo-frame {display:grid;grid-template-columns:minmax(0,2.5fr) minmax(245px,1fr);gap:30px;align-items:start;}
    .tree {min-width:0;}
    .explanation {padding:22px 0 0;font-size:18px;line-height:1.65;}
    .step-label {font:13px Georgia,serif;color:#657080;letter-spacing:.07em;}
    .explanation h2 {font-size:26px;line-height:1.2;margin:12px 0 18px;letter-spacing:-.02em;}
    .bounds {display:flex;gap:24px;font-size:23px;}
    .equation {font-size:20px;font-weight:600;min-height:30px;}
    .stats {font:16px Georgia,serif;margin-top:22px;}
    .sequence,.cutoffs {font-size:15px;color:#657080;overflow-wrap:anywhere;}
    .cutoffs {padding-left:18px;}
    .outcome {color:#246BEB;font-weight:bold;}
    .legend {font:15px Georgia,serif;color:#657080;margin:0 0 6px;}
    @media(max-width:850px){.demo-frame{grid-template-columns:1fr;gap:4px}.explanation{padding-top:0}.demo-header{display:block}.demo-header h1{font-size:22px}}
    </style><header class="demo-header"><h1>Week 7 Tutorial | Games, Adversarial Search</h1><span>Team: Trible L</span></header>''')
    return


@app.cell(hide_code=True)
def _(mo):
    mode = mo.ui.radio(
        options={"(a) Minimax": "minimax", "(b) Alpha-beta": "alphabeta", "(c) Chance": "chance"},
        value="(a) Minimax", inline=True,
    )
    mode
    return (mode,)


@app.cell
def _(build_trace, mo, mode):
    frames = build_trace(mode.value)
    get_step, set_step = mo.state(0, allow_self_loops=True)
    return frames, get_step, set_step


@app.cell(hide_code=True)
def _(frames, get_step, mo, set_step):
    _index = get_step()
    _last = len(frames) - 1
    previous_button = mo.ui.button(
        label="← Previous", disabled=_index == 0,
        on_click=lambda _: set_step(max(0, get_step() - 1)),
    )
    next_button = mo.ui.button(
        label="Next →", disabled=_index == _last, kind="success",
        on_click=lambda _: set_step(min(_last, get_step() + 1)),
    )
    restart_button = mo.ui.button(label="Restart", disabled=_index == 0,
                            on_click=lambda _: set_step(0))
    mo.hstack([previous_button, next_button, restart_button,
               mo.Html(f'<span class="nav-count">Step {_index} of {_last}</span>')],
              justify="start", align="center", gap=1).style({"margin": "4px 0 14px"})
    return


@app.cell(hide_code=True)
def _(frames, get_step, mo, mode, render_frame):
    mo.vstack([
        mo.Html('<div class="legend"><span style="color:#246BEB">△ MAX / α</span> &nbsp; '
                '<span style="color:#E23D45">▽ MIN / β</span> &nbsp; '
                '<span style="color:#997016">○ CHANCE</span> &nbsp; · Gold fill: current node · ×: pruned</div>'),
        mo.Html(render_frame(frames[get_step()], mode.value, get_step(), len(frames)-1)),
    ])
    return


if __name__ == "__main__":
    app.run()
