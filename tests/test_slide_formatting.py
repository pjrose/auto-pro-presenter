"""Regression checks for theme effects and mixed-size presentations."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import service_builder as builder
from striprtf.striprtf import rtf_to_text

ROOT = Path(__file__).resolve().parents[1]


def theme(name):
    return builder.Template.Document.FromString((ROOT / 'themes' / name / 'Theme').read_bytes())


class SlideFormattingTests(unittest.TestCase):
    def setUp(self):
        self.template = next(s.base_slide for s in theme('Lyrics Centered').slides
                             if s.name == 'Top Third - White')
        self.prototype = builder.Presentation.FromString((ROOT / 'templates/starter.pro').read_bytes())
        self.cue = next(c for c in self.prototype.cues if any(a.HasField('slide') for a in c.actions))
        self.action = next(a for a in self.cue.actions if a.HasField('slide'))

    def test_lyric_style_survives_new_text_and_round_trip(self):
        slide = builder.fresh_slide(self.template)
        element = slide.elements[0]
        original = self.template.elements[0].element
        builder.set_template_text(element, 'Señor fiel\nCorazón {y} \\ amor')
        doc = builder.Presentation()
        doc.cues.add().CopyFrom(builder.make_cue(self.cue, self.action, slide))
        parsed = builder.Presentation.FromString(doc.SerializeToString())
        actual = parsed.cues[0].actions[0].slide.presentation.base_slide.elements[0].element
        self.assertEqual(rtf_to_text(actual.text.rtf_data.decode()), 'SEÑOR FIEL\nCORAZÓN {Y} \\ AMOR')
        self.assertIn(b'\\strokewidth40', actual.text.rtf_data)
        self.assertIn(b'\\strokec2', actual.text.rtf_data)
        self.assertEqual(actual.fill, original.fill)
        self.assertEqual(actual.text_line_mask, original.text_line_mask)
        self.assertEqual(actual.text.attributes.stroke_color, original.text.attributes.stroke_color)
        self.assertEqual(actual.text.attributes.stroke_width, original.text.attributes.stroke_width)
        self.assertFalse(actual.text.attributes.custom_attributes)
        self.assertNotIn(b'Que todo', actual.text.rtf_data)

    def test_full_hd_scales_bounds_without_mutating_theme(self):
        old = self.template.SerializeToString()
        slide = builder.fresh_slide(self.template)
        self.assertEqual((slide.size.width, slide.size.height), (1920, 1080))
        self.assertAlmostEqual(slide.elements[0].element.bounds.size.height,
                               self.template.elements[0].element.bounds.size.height * 1080 / self.template.size.height)
        self.assertEqual(old, self.template.SerializeToString())
        once = slide.SerializeToString()
        builder.normalize_slide_size(slide)
        self.assertEqual(once, slide.SerializeToString())

    def test_reused_song_resizes_first_and_all_other_cues_preserving_structure(self):
        doc = copy.deepcopy(self.prototype)
        doc.ClearField('cues')
        for text in ('', 'Señor fiel', 'Corazón'):
            slide = copy.deepcopy(self.template)
            builder.set_template_text(slide.elements[0], text)
            doc.cues.add().CopyFrom(builder.make_cue(self.cue, self.action, slide))
        doc.cues[0].actions.add().media.SetInParent()
        ids = [c.uuid.string for c in doc.cues]
        arrangements = [a.SerializeToString() for a in doc.arrangements]
        media = doc.cues[0].actions[-1].SerializeToString()
        builder.format_song(doc, self.template)
        self.assertEqual(ids, [c.uuid.string for c in doc.cues])
        self.assertEqual(arrangements, [a.SerializeToString() for a in doc.arrangements])
        self.assertEqual(media, doc.cues[0].actions[-1].SerializeToString())
        for cue in doc.cues:
            slide = cue.actions[0].slide.presentation.base_slide
            self.assertEqual((slide.size.width, slide.size.height), (1920, 1080))
        self.assertEqual(rtf_to_text(doc.cues[0].actions[0].slide.presentation.base_slide.elements[0].element.text.rtf_data.decode()), '')

    def test_sermon_title_point_and_verse_are_full_hd(self):
        bible = next(s for s in theme('Plain Text').slides if s.name == 'Central Bible Format')
        manifest = {'sermon_name': 'Practice', 'sermon_title': ['Practice'], 'sermon_slides': [
            {'type': 'point', 'text': 'Example'},
            {'type': 'verse', 'text': 'Example text', 'reference': 'Example 1:1'}]}
        doc = builder.make_sermon(manifest, self.prototype, self.cue, self.action, theme('Black'), bible)
        self.assertEqual(len(doc.cues), 3)
        for cue in doc.cues:
            slide = cue.actions[0].slide.presentation.base_slide
            self.assertEqual((slide.size.width, slide.size.height), (1920, 1080))

    def test_new_song_retains_repeated_sections_and_blank_background(self):
        song = {'name': 'Practice', 'source_pptx': 'unused.pptx', 'sections': [
            {'name': 'Chorus', 'slides': [1]}, {'name': 'Chorus', 'slides': [2]}]}
        with patch.object(builder, 'pptx_slide_texts', return_value=['Señor fiel', 'Señor fiel']):
            doc = builder.make_lyrics(song, ROOT, self.prototype, self.cue, self.action, self.template)
        builder.format_song(doc, self.template)
        self.assertEqual(len(doc.cues), 2)
        order = doc.arrangements[0].group_identifiers
        self.assertEqual(len(order), 3)
        self.assertEqual(order[1], order[2])
        for cue, expected in zip(doc.cues, ['', 'SEÑOR FIEL']):
            slide = cue.actions[0].slide.presentation.base_slide
            self.assertEqual((slide.size.width, slide.size.height), (1920, 1080))
            self.assertEqual(rtf_to_text(slide.elements[0].element.text.rtf_data.decode()), expected)

    def test_unknown_rtf_and_invalid_canvas_fail_explicitly(self):
        slide = copy.deepcopy(self.template)
        slide.elements[0].element.text.rtf_data = b'{unrecognized}'
        with self.assertRaisesRegex(ValueError, 'Unrecognized themed RTF'):
            builder.set_template_text(slide.elements[0], 'Example')
        slide.size.height = 0
        with self.assertRaisesRegex(ValueError, 'invalid dimensions'):
            builder.normalize_slide_size(slide)


if __name__ == '__main__':
    unittest.main()
