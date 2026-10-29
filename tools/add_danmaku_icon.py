"""Add the Macast speech-bubble glyph to ModernZ's bundled icon font.

This is an asset authoring tool, not a build-time requirement. Requires
fontTools. The generated font remains a derivative of ModernZ's icon font.
"""

from pathlib import Path
import sys

from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont


FONT = Path(__file__).resolve().parents[1] / 'mpv_ui/fonts/modernz-icons.ttf'
CODEPOINT = 0xF100
GLYPH_NAME = 'macast_danmaku'


def build(font_path=FONT):
    font = TTFont(font_path)
    if any(CODEPOINT in table.cmap for table in font['cmap'].tables if table.isUnicode()):
        raise RuntimeError('Macast danmaku glyph already present')

    # Match ModernZ's 1024-unit, 1024-advance Fluent buttons. In particular,
    # ordinary subtitles occupy x=85..939, y=107..789. The bubble uses the
    # same outer bounds, so ASS can align it on the same center and baseline.
    pen = TTGlyphPen(None)
    pen.moveTo((190, 789))
    pen.lineTo((834, 789))
    pen.qCurveTo((939, 789), (939, 684))
    pen.lineTo((939, 285))
    pen.qCurveTo((939, 180), (834, 180))
    pen.lineTo((456, 180))
    pen.lineTo((315, 107))
    pen.lineTo((340, 180))
    pen.lineTo((190, 180))
    pen.qCurveTo((85, 180), (85, 285))
    pen.lineTo((85, 684))
    pen.qCurveTo((85, 789), (190, 789))
    pen.closePath()

    # Counterclockwise interior makes a light outline like Fluent subtitles.
    pen.moveTo((190, 285))
    pen.qCurveTo((190, 272), (203, 272))
    pen.lineTo((796, 272))
    pen.qCurveTo((834, 272), (834, 310))
    pen.lineTo((834, 659))
    pen.qCurveTo((834, 697), (796, 697))
    pen.lineTo((228, 697))
    pen.qCurveTo((190, 697), (190, 659))
    pen.closePath()

    glyphs = font.getGlyphOrder() + [GLYPH_NAME]
    font.setGlyphOrder(glyphs)
    font['glyf'][GLYPH_NAME] = pen.glyph()
    font['hmtx'][GLYPH_NAME] = (1024, 85)
    for table in font['cmap'].tables:
        if table.isUnicode():
            table.cmap[CODEPOINT] = GLYPH_NAME
    font['maxp'].numGlyphs = len(glyphs)
    font.save(font_path)


if __name__ == '__main__':
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else FONT)
