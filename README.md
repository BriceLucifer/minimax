# Week 7 Tutorial | Games, Adversarial Search

**Team: Trible L**

给学生发 handout 第 1 页；第 2 页答案由你保留。下面英文可直接照读，中文只提示操作。不需要提问或等学生回答。

## 0–5 分钟：布置练习

> We’re Team Trible L. The blue triangles are MAX nodes; the red triangles are MIN nodes.
>
> For part (a), work upward from the leaves. Fill in the internal values and choose the best root action.
>
> For part (b), restart from the root and search left to right. Mark the cutoffs, record alpha and beta, and count the leaves you visit.
>
> Spend about five minutes on these two parts. We’ll do part (c) together.

学生做题。若卡住，提示“MAX takes the larger value; MIN takes the smaller value.”

## 5–7 分钟：minimax

演示选择 **(a) Minimax**，逐步回传。

> Start with the six lower MAX nodes. Their values are 5, 9, 2, 8, 6 and 8.
>
> At the MIN level, A takes the smaller of 5 and 9: 5. B takes the smaller of 2 and 8: 2. C takes the smaller of 6 and 8: 6.
>
> The root takes the largest of 5, 2 and 6. Its value is 6, so we choose action c, leading to C.

## 7–9 分钟：A2 剪枝

切到 **(b) Alpha-beta**，从头演示到 **Step 12**（第一次剪枝）。

> Start with alpha at negative infinity and beta at positive infinity.
>
> A1 returns 5. A is MIN, so its beta becomes 5. A2 inherits this bound.
>
> A2 reads 6. As a MAX node, its value is now at least 6. A already has an option worth 5, so it will not choose A2.
>
> Alpha is 6 and beta is 5. Since alpha is greater than or equal to beta, we skip the leaf 9.
>
> We know only that A2 is at least 6. We have not calculated its exact value in this search.

指向 A2：**α＝6、β＝5**；划掉分支 **m**。

## 9–11 分钟：B 剪枝

继续到 **Step 23**（第二次剪枝）。

> A returns 5, so the root’s alpha becomes 5. B inherits that bound.
>
> B1 reads 1 and 2, then returns 2. B is MIN, so its beta becomes 2. B can now offer at most 2.
>
> The root already has 5, so B cannot improve its choice. Alpha is 5 and beta is 2: we skip all of B2, including leaves 8 and 7.

指向 B：**α＝5、β＝2**；划掉分支 **g** 下的 B2 子树。

## 11–12 分钟：完成搜索

继续到 **Step 42**（搜索结束）。

> C1 returns 6. C2 reads 3 and 8, then returns 8. C returns the smaller value, 6.
>
> The root chooses action c, just as in minimax.
>
> We visited 9 of 12 leaves. We skipped one leaf under A2 and two under B2. A different visit order may change the amount of pruning, but not the root value.

## 12–15 分钟：chance

切到 **(c) Chance**。下层 MAX 值保留，A、B、C 改成圆形随机节点。

> Replace A, B and C with CHANCE nodes. Each child has probability one half, so we average the two child values.
>
> A becomes the average of 5 and 9: 7. B becomes the average of 2 and 8: 5. C becomes the average of 6 and 8: 7.
>
> The root still takes the maximum. Actions a and c now tie at 7. Action c is still optimal, but it is no longer the only best action.
>
> MIN chooses the worst outcome for MAX. CHANCE takes a probability-weighted average. The skipped branches matter again because they contribute to the expectation.
>
> This tree uses expectimax. A tree with MAX, MIN and CHANCE nodes uses expectiminimax.

讲完一层或一个剪枝点，留两三秒给学生补写。若时间紧，chance 只讲 **7、5、7；a 和 c 并列最优；取期望代替取最小值**。

## 答案速查

| 项目 | 结果 |
| --- | --- |
| 下层 MAX | A1＝5，A2＝9，B1＝2，B2＝8，C1＝6，C2＝8 |
| MIN | A＝5，B＝2，C＝6 |
| 根值／动作 | 6／c |
| A2 剪枝 | α＝6，β＝5；跳过 9（m） |
| B 剪枝 | α＝5，β＝2；跳过 B2（g） |
| 访问顺序 | 3、5、6、1、2、4、6、3、8，共 9/12 |
| CHANCE／根动作 | A＝7，B＝5，C＝7；a、c 并列最优 |

## 交互演示

[minimax_visualizer.py](minimax_visualizer.py) 是 marimo notebook，也是可运行的 Python 文件。选择题目后，点击 **Next** 前进一步，**Previous** 返回，**Restart** 从头开始。切换题目会重置进度。叶子原始分数始终可见，只有搜索实际读到的叶子才计入访问量。

在仓库根目录创建本地环境并启动：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install "marimo==0.24.2"
.venv/bin/marimo run minimax_visualizer.py
```

在其他电脑上用 uv 启动（首次需下载 marimo）：

```sh
uvx marimo run --sandbox minimax_visualizer.py
```

编辑 notebook：

```sh
uvx marimo edit --sandbox minimax_visualizer.py
```

## Handout

- [PDF](output/pdf/minimax_handout.pdf)：第 1 页题目，第 2 页答案。
- [Typst 源码](minimax_handout.typ)：CeTZ 绘图。

```sh
typst c minimax_handout.typ output/pdf/minimax_handout.pdf
```

marimo 用法参考：[运行 notebook](https://docs.marimo.io/guides/apps/)、[交互按钮](https://docs.marimo.io/api/inputs/button/)。

## 测试

[测试报告](TEST_REPORT.md) 包含浏览器逐步操作与算法检查结果。运行回归测试：

```sh
.venv/bin/marimo check minimax_visualizer.py
.venv/bin/python -m unittest discover -s tests -v
```

## GitHub Actions / GitHub Pages

工作流：[.github/workflows/pages.yml](.github/workflows/pages.yml)。

- Pull request：检查 notebook、运行 6 项回归测试、导出交互网页；不部署。
- 推送到 `main`：检查通过后自动部署 GitHub Pages。
- Actions 页面也可以手动选择 `main`，点击 **Run workflow**。
- 固定使用 Python 3.13 和 marimo 0.24.2；以后升级 marimo 时同步修改 Python 文件内的依赖版本与 workflow。

首次设置：在 GitHub 仓库的 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**，然后推送到 `main`。无需填写个人 token。成功后可在 Actions 的 `github-pages` deployment 找到网站链接。

新建仓库后，把本目录的内容放在**新仓库根目录**，包括隐藏的 `.github/` 文件夹。GitHub 只识别仓库根目录下的 `.github/workflows`。配置也兼容 notebook 放在 `tutorial/` 子目录的情况。

提交 Python 文件、`tests/`、workflow 和所需的 `layouts/` 文件。不要提交 `.venv`、`__marimo__` 或 `output/web`；网页由 CI 重新导出。保存的 Slides 布局会影响导出，因此上传前先确认本地布局正确。

实现依据：[GitHub Pages 官方工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)、[marimo WebAssembly 导出](https://docs.marimo.io/guides/exporting/webassembly_html/)。
