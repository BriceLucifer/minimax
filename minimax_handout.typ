// Compile: typst compile minimax_handout.typ output/pdf/minimax_handout.pdf
// First compilation downloads CeTZ from Typst Universe.
#import "@preview/cetz:0.5.2"
#let ink = rgb("253448")
#let muted = rgb("657080")
#let min-red = rgb("E23D45")
#let max-blue = rgb("246BEB")
#let game-name = [#text(fill: min-red)[Mini]#text(fill: max-blue)[max]]
#set document(title: "Week 7 Tutorial | Games, Adversarial Search", author: "Trible L")
#set page(paper: "a4", margin: (x: 18mm, y: 16mm),
  footer: context [#text(size: 8pt, fill: luma(90))[COMPSCI 761 · ADVERSARIAL SEARCH] #h(1fr) #counter(page).display("1 / 1", both: true)])
#set text(font: "Libertinus Serif", size: 11pt, fill: ink)
#set par(leading: 0.55em)
#show "MAX": set text(fill: max-blue)
#show "MIN": set text(fill: min-red)
#show "α": set text(fill: max-blue)
#show "β": set text(fill: min-red)
#set heading(numbering: none)
#show heading.where(level: 1): set text(font: "Libertinus Serif", size: 20pt, weight: "bold", fill: ink)
#show heading.where(level: 2): it => block(above: 4mm, below: 2mm)[#text(font: "Libertinus Serif", size: 12pt, weight: "bold", fill: ink, it.body)]
#let rule = line(length: 100%, stroke: 0.5pt + luma(150))
#let blank = box(width: 20mm, baseline: 2pt, line(length: 20mm, stroke: 0.5pt))
#let leaves = (3, 5, 6, 9, 1, 2, 8, 7, 4, 6, 3, 8)
#let tree() = block(width: 100%, inset: (x: 3mm, top: 0mm, bottom: 2mm), fill: white)[
  #text(font: "Libertinus Serif", size: 8pt, fill: muted)[#text(fill: max-blue)[△ MAX] #h(5mm) #text(fill: min-red)[▽ MIN]]
  #v(0mm)
  #align(center, cetz.canvas(length: 1mm, {
    import cetz.draw: *
    // Fixed level spacing keeps the full balanced tree easy to annotate.
    let xs = (13, 39, 65, 91, 117, 143)
    let letters = "abcdefghijklmnopqrstu".clusters()
    let edge(a, b, label) = {
      line(a, b, stroke: 0.8pt + rgb("8B95A3"))
      content(((a.at(0) + b.at(0)) / 2, (a.at(1) + b.at(1)) / 2),
        box(fill: white, inset: (x: 1.2pt, y: 0.4pt),
          text(font: "Libertinus Serif", size: 8pt, fill: ink, label)))
    }
    for (i, x) in (26, 78, 130).enumerate() { edge((78, 0), (x, -22), letters.at(i)) }
    for (i, x) in (26, 78, 130).enumerate() {
      for (j, xx) in (x - 13, x + 13).enumerate() { edge((x, -22), (xx, -44), letters.at(3 + 2 * i + j)) }
    }
    for (i, x) in xs.enumerate() {
      for (j, xx) in (x - 6.5, x + 6.5).enumerate() { edge((x, -44), (xx, -66), letters.at(9 + 2 * i + j)) }
    }
    let decision(x, y, name, is-min: false) = {
      let d = if is-min { -1 } else { 1 }
      let node-color = if is-min { min-red } else { max-blue }
      line((x, y + d * 7), (x - 9, y - d * 5), (x + 9, y - d * 5),
        close: true, fill: white, stroke: 1pt + node-color)
      line((x - 3.8, y - d * 1.7), (x + 3.8, y - d * 1.7), stroke: 0.45pt + muted)
      content((x + 10.5, y + 2.5), anchor: "west", text(font: "Libertinus Serif", size: 8pt, weight: "bold", fill: node-color, name))
    }
    decision(78, 0, "Root")
    for (i, name) in ("A", "B", "C").enumerate() { decision(26 + i * 52, -22, name, is-min: true) }
    for (i, name) in ("A1", "A2", "B1", "B2", "C1", "C2").enumerate() { decision(xs.at(i), -44, name) }
    for (i, value) in leaves.enumerate() {
      let x = 6.5 + i * 13
      circle((x, -66), radius: 3.3, fill: white, stroke: 0.6pt + rgb("A5AEBA"))
      content((x, -66), text(font: "Libertinus Serif", size: 10pt, weight: "bold", fill: ink, str(value)))
    }
  }))
]

#let masthead(title, student: false) = block(width: 100%, below: 4mm)[
  #text(size: 16pt, weight: "bold", title)
  #v(3mm)
  #if student [
    #grid(columns: (1fr, auto, auto), column-gutter: 12mm, align: bottom,
      grid(columns: (auto, 1fr), column-gutter: 2mm, align: bottom,
        text(size: 10pt)[Name], line(length: 100%, stroke: 0.4pt + luma(150))),
      text(size: 10pt)[Week 7],
      text(size: 10pt, fill: muted)[Team name: *Trible L*],
    )
  ] else [
    #text(size: 10pt, fill: muted)[Team name: *Trible L*]
  ]
]
#masthead([Week 7 Tutorial | Games, Adversarial Search], student: true)

== (a) #game-name
Fill in *all internal node values* on the tree, working from the leaves upward. State the root value and the best root action (a, b or c).

#v(-1mm)
#tree()
#v(2mm)
Root value: #blank #h(12mm) Best root action: #blank

== (b) α–β pruning
Start a *fresh search*, visiting children *from left to right*, with $alpha = -infinity$ and $beta = +infinity$ at the root. Do not use values calculated in (a) to skip ahead.

Cross out every unvisited part of the tree. At each cutoff, label the node and the current $alpha$ and $beta$. Count only leaves actually evaluated.

#v(3mm)
Cutoff 1: #blank #h(5mm) $alpha =$ #blank #h(5mm) $beta =$ #blank

#v(3mm)
Cutoff 2: #blank #h(5mm) $alpha =$ #blank #h(5mm) $beta =$ #blank

#v(2mm)
Leaves evaluated: #blank / 12

== (c) Chance nodes
Replace A, B and C with *CHANCE* nodes. Each chooses its two MAX children with probability $1/2$ each. Keep the root and the lower MAX nodes unchanged. Use the *full tree*: recalculate the three values and the root's best action(s).

$V(A) =$ #blank #h(4mm) $V(B) =$ #blank #h(4mm) $V(C) =$ #blank

Best root action(s): #blank #h(6mm) Does the choice change? #blank

#pagebreak()
#masthead([Answers])

== (a) #game-name
#table(columns: (1fr, 1fr, 1fr), inset: 7pt, stroke: (x: none, top: none, bottom: 0.5pt + rgb("D9DFE6")), fill: (x, y) => if y == 0 { rgb("E8EDF3") } else if y == 3 { rgb("F5F7FA") } else { none },
  table.header([*Node A · action a*], [*Node B · action b*], [*Node C · action c*]),
  [$"A1" = max(3, 5) = 5$], [$"B1" = max(1, 2) = 2$], [$"C1" = max(4, 6) = 6$],
  [$"A2" = max(6, 9) = 9$], [$"B2" = max(8, 7) = 8$], [$"C2" = max(3, 8) = 8$],
  [*$A = min(5, 9) = 5$*], [*$B = min(2, 8) = 2$*], [*$C = min(6, 8) = 6$*],
)
The root value is $max(5, 2, 6) = bold(6)$. MAX chooses action *c* (leading to C).

== (b) α–β pruning
*1. Cutoff at A2 (MAX).* A1 returns 5, so A passes $beta = 5$ to A2. After A2 reads its first leaf, 6, its bound is $alpha = 6$. Since $alpha >= beta$ ($6 >= 5$), skip the leaf *9*. A already has an alternative worth 5 and will not choose A2, whose value is at least 6.

*2. Cutoff at B (MIN).* A returns 5, so the root passes $alpha = 5$ to B. B1 returns 2, making $beta = 2$ at B. Since $beta <= alpha$ ($2 <= 5$), skip *all of B2*, including leaves *8 and 7*. B can offer at most 2, so it cannot improve the root's current choice.

*Finish C.* C1 returns 6; C2 reads 3 and then 8. Both leaves are visited, so no additional leaves are pruned. C returns 6, so *c* becomes the best root action.

#block(fill: luma(245), inset: 9pt, width: 100%)[
  *Visited, in order:* 3, 5, 6, 1, 2, 4, 6, 3, 8. \
  *Total: 9 / 12 leaves evaluated; 3 leaves pruned.* Root value: *6*, action: *c*.
]
The cutoff at A2 establishes a *lower bound* of 6, not its exact minimax value of 9. B2 is never evaluated. α–β can select the correct root action without finding every internal node's exact value.

Changing visit order can change the amount of pruning, but not the root minimax value. It may change which equally good action is selected when there is a tie.

== (c) Chance nodes
The lower MAX values stay the same. At each CHANCE node, take the probability-weighted average:
$ V(A) = 1/2 (5) + 1/2 (9) = 7, quad
   V(B) = 1/2 (2) + 1/2 (8) = 5, quad
   V(C) = 1/2 (6) + 1/2 (8) = 7. $
The root value is *7*: actions *a and c tie* (nodes A and C). Action c is still optimal, but it is no longer the unique best action.

*MIN* models an opponent choosing the worst branch for MAX. *CHANCE* models an outcome drawn according to given probabilities, so we take an expectation. This modified tree is *expectimax*; a tree containing MAX, MIN and CHANCE nodes uses *expectiminimax*.

The earlier cutoffs relied on MIN's choice. Do not reuse them for this chance calculation: the skipped branches contribute to the expectation.

