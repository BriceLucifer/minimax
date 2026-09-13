"""Regression checks for the fixed Week 7 tree; run with unittest discovery."""
import re
import unittest
import xml.etree.ElementTree as ET

import minimax_visualizer


class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.defs = minimax_visualizer.app.run()
        cls.traces = {mode: cls.defs['build_trace'](mode)
                      for mode in ('minimax', 'alphabeta', 'chance')}

    def test_handout_answers_and_cutoffs(self):
        self.assertEqual(self.defs['verify_demo'](),
                         {'minimax': 11, 'alphabeta': 43, 'chance': 5})

    def test_no_evaluated_leaf_is_pruned_and_visits_only_grow(self):
        leaves = self.defs['utilities']
        for mode, frames in self.traces.items():
            old_seen, old_pruned = [], set()
            for frame in frames:
                with self.subTest(mode=mode, event=frame['event']):
                    self.assertEqual(frame['seen'][:len(old_seen)], old_seen)
                    self.assertEqual(len(set(frame['seen'])), len(frame['seen']))
                    self.assertLessEqual(set(frame['seen']), set(leaves))
                    self.assertTrue(old_pruned <= frame['pruned'])
                    self.assertFalse(set(frame['seen']) & frame['pruned'])
                old_seen, old_pruned = frame['seen'], frame['pruned']

    def test_bounds_enclose_true_minimax_values(self):
        children, leaves = self.defs['children'], self.defs['utilities']
        def oracle(node):
            if node in leaves:
                return leaves[node]
            values = [oracle(child) for child in children[node]]
            return min(values) if node in ('A', 'B', 'C') else max(values)
        for frame in self.traces['alphabeta']:
            for node, label in frame['values'].items():
                actual = oracle(node)
                if label.startswith('≥'):
                    self.assertGreaterEqual(actual, float(label[1:]))
                elif label.startswith('≤'):
                    self.assertLessEqual(actual, float(label[1:]))
                else:
                    self.assertEqual(actual, float(label))

    def test_switching_modes_builds_fresh_state(self):
        for mode in self.traces:
            fresh = self.defs['build_trace'](mode)
            self.assertEqual(fresh, self.traces[mode])
            self.assertFalse(fresh[0]['seen'])
            self.assertFalse(fresh[0]['pruned'])
            self.assertFalse(fresh[0]['best'])
        self.assertEqual(set(self.traces['chance'][0]['values']),
                         set(self.defs['lower_nodes']))
        self.assertFalse(self.traces['alphabeta'][0]['values'])

    def test_revisiting_frames_does_not_change_state(self):
        for mode, frames in self.traces.items():
            first = self.defs['render_frame'](frames[0], mode, 0, len(frames)-1)
            for i in reversed(range(len(frames))):
                self.defs['render_frame'](frames[i], mode, i, len(frames)-1)
            self.assertEqual(first, self.defs['render_frame'](frames[0], mode, 0, len(frames)-1))
            self.assertIsNot(frames[0]['values'], frames[-1]['values'])

    def test_every_frame_has_valid_svg_and_correct_node_shapes(self):
        ns = {'s': 'http://www.w3.org/2000/svg'}
        for mode, frames in self.traces.items():
            for i, frame in enumerate(frames):
                with self.subTest(mode=mode, step=i):
                    html = self.defs['render_frame'](frame, mode, i, len(frames)-1)
                    svg = ET.fromstring(re.search(r'<svg\b.*?</svg>', html, re.S).group())
                    self.assertEqual(len(svg.findall('s:g', ns)), 22)
                    self.assertEqual(len(svg.findall('.//s:polygon', ns)), 7 if mode == 'chance' else 10)
                    self.assertEqual(len(svg.findall('.//s:circle', ns)), 15 if mode == 'chance' else 12)
                    self.assertNotIn('None', html)


if __name__ == '__main__':
    unittest.main()
