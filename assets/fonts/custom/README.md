## This folder include fonts that are created specifically for the app.
### Fonts available
- NotoSans (only certain characters).ttf.
    
    This font includes:
    - Characters from `NotoSans-Regular.ttf` includes `., 0123456789VXд﷼€៛cEe₹čHN₨ДmGx₱wMuбƒнyjlOв₦qzуA₫S$Iа₩еDvfsar£м؋RZ¥CłJhL₭dPnBUл₪/.okK₡₴р฿ptiWbTFQg₮¢иY`
    - Characters from `NotoSansSC-Regular.ttf` includes `百千万亿`
    - Characters from `IBMPlexSerif-Regular.ttf` include `฿`
    - Characters from `Gulzar-Regular.ttf` include `﷼`

### Scripts
#### To extract certain chars from a font
```py
import fontforge

def extract_particular_characters_from_font(font_path: str, output_font_path: str, characters = [], characters_unicode = []):
    font = fontforge.open(font_path)
    font.selection.none()

    for char in characters:
        font.selection.select(('more',), ord(char))
    for unicode in characters_unicode:
        font.selection.select(('more',), unicode)
    
    font.selection.invert()
    font.clear()
    font.generate(output_font_path)
    font.close()
```
