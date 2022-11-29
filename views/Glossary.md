### Variation Selectors (0xFE0E / 0xFE0F)

An invisible codepoint which specifies that the preceding character should be displayed with or without emoji presentation.


<table>
<tr><th>without Variant Selector (default)</th><td>0x2764</td><td>&#x2764;</td></tr>
<tr><th>with Emoji Variant Selector (0xFE0E)</th><td>0x2764 + 0xFE0F</td><td>&#x2764;&#xFE0F;</td></tr>
<tr><th colspan="3"></th></tr>
<tr><th>without Variant Selector (default)</th><td>0x1F44D</td><td>&#x1F44D;</td></tr>
<tr><th>with Text Variant Selector (0xFE0E)</th><td>0x1F44D + 0xFE0E</td><td>&#x1F44D;&#xFE0E;</td></tr>
</table>
<br>


ref: https://en.wikipedia.org/wiki/Variation_Selectors_(Unicode_block)


### Zero Width Joiner (0x200D)

ZWJ character is used to combine multiple (two or more) emojis into single glyph.

<table>
<tr>
    <th>Man Firefighter</th>
    <td>0x1F468 + 0x200D + 0x1F692</td>
    <td>&#x1F468; + ZWJ + &#x1F692; = &#x1F468;&#x200D;&#x1F692; </td>
</tr>
<tr>
    <th>Family with Mother and Two Sons</th>
    <td>0x1F469 + 0x200D + 0x1F466 + 0x200D + 0x1F466</td>
    <td>&#x1F469; + ZWJ + &#x1F466; + ZWJ + &#x1F466; = &#x1F469;&#x200D;&#x1F466;&#x200D;&#x1F466;</td>
</tr>
</table>
<br>


more examples: https://family-emoji.org/



### Skin Tone Modifier (0x1F3FB - 0x1F3FF)

<table>
<tr><th>Without modifier</th><td>-</td><td>&#x1F44F;</td></tr>
<tr><th>Fitzpatrick Type-1-2</th><td>0x1F3FB</td><td>&#x1F44F;&#x1F3FB;</td></tr>
<tr><th>Fitzpatrick Type-3</th><td>0x1F3FC</td><td>&#x1F44F;&#x1F3FC;</td></tr>
<tr><th>Fitzpatrick Type-4</th><td>0x1F3FD</td><td>&#x1F44F;&#x1F3FD;</td></tr>
<tr><th>Fitzpatrick Type-5</th><td>0x1F3FE</td><td>&#x1F44F;&#x1F3FE;</td></tr>
<tr><th>Fitzpatrick Type-6</th><td>0x1F3FF</td><td>&#x1F44F;&#x1F3FF;</td></tr>
</table>


### Gender Modifier (0x2640, 0x2642)

<table>
<tr><th>Without modifier</th><td>-</td><td>&#x1F9D9;</td></tr>
<tr><th>Female modifier</th><td>0x2640</td><td>&#x1F9D9;&#x200D;&#x2640;</td></tr>
<tr><th>Male modifier</th><td>0x2642</td><td>&#x1F9D9;&#x200D;&#x2642;</td></tr>
</table>


<!-- ### Letters (?? - ??)
TBA -->


### Twitter Language Codes

Three letter special codes:

- **und** - Undetermined
- **zxx** - Sensitive content
- **qme** - Only media
- **qam** - Only mentions
- **art** - Art related
- **qst** - Short utterances (single word)
- **qht** - Only hastags
- **ckb** - Arabic languages
- **qct** - Only cashtags
