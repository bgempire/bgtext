# BGText
## BGText: A BGE Dynamic Text Utility

BGText is a [Blender Game Engine](https://en.wikipedia.org/wiki/Blender_Game_Engine) and [UPBGE](https://upbge.org/) utility aiming to enhance the experience with text objects.

Motivations
===========

In the old days of BGE there was a feature known as bitmap text. It allowed you to setup a font texture to a plane, map its UV to a single character, enable the Text option on its material, add an Text property to the object and then show a text based on the property, pretty complicated. Then, it was replaced by the dynamic text, now based on True Type fonts, where you add a text, a property named Text to it and then show a text based on this property.

Although the dynamic texts are much easier to use than the bitmap texts, both have their pros and cons. The main cons are:

- Bitmap texts
    - No support for latin characters.
    - Pretty hard and clunky to setup, even to make a functional font texture.

- Dynamic texts
    - Text resolution is frequently a problem.
    - When scaled at runtime, the text must be redrawn, slowing down the engine a lot.
    - The text is bound to be flat, with no custom styles besides the color.

- Both
    - No support for text alignment and justify.
    - Horizontal and vertical distance between characters are fixed.
    - No automatic text wrapping.

Obs: UPBGE fixed the resolution issues on dynamic texts, allowing you to change its resolution at runtime.

I've used dynamic texts over a long time due to its ease, and I know some people that still uses the bitmap text due to the ability to stylize the text with outlines and other stuff. Based on this, I thought to work in some way to overcome those issues.

BGText's Features
=================

BGText tries to mix the pros and fix most of the cons on bitmap texts and dynamic texts, also providing an easy interface to setup each feature (by using game properties). The main features are:

- Easy to use, but also complex if you need.
- Text styles based on textures, so it's highly customizable.
- Character size based on each character origin.
- Horizontal and vertical character offset (distance between characters).
- Automatic text wrap based on number of characters per line.
- Left, center and right text alignment (justify).
- Literal text or Python expressions (a huge time saver!).
- Color based on predefined color names or RGBA vectors.
- Static text or updated by an specified interval.
- Update texts without the need of constant processing with the message `UpdateText`.
- `UpdateText` messages can update `All` texts or the ones with specific `Id` properties.

BGText is compatible with both vanilla BGE and UPBGE. BGText uses the replace mesh functionality to switch between characters values.

How To Use
==========

It's simple: on your blend file, link the group BGText from BGText blend file (`File` > `Link`), then you're ready to use it. To setup the text, all you have to do is to add properties to the group instance of BGText, and when you play the game the given properties will be applied.

All the characters on BGText instance will automatically be parented to the group object, so you can do whatever logic you want to on top of the instance, even change the text at runtime (see the use of `UpdateText` messages below).

Messages
========

BGText can trigger specific actions by using messages. To use this functionality, just send a message with a specific subject and you're ready to go.

- **Subject:** `UpdateText`
    - **Description:** Updates the text at command without the need of processing the text each frame with the `Update` property.
    - **Body:** `All` to update all texts or an `Id` value to update only texts with this value.

Reference
=========

This reference shows which attributes you could use on BGText group instance to change its behavior. You don't need to add all the attributes, only those you want to setup.

- `Text`
    - **Description:** String literal or Python expression.
    - **Type:** `String`

- `Size`
    - **Description:** Individual character size multiplier.
    - **Type:** `Float`

- `Offset`
    - **Description:** Distance multiplier between each character.
    - **Type:** `Float` 

- `OffsetH`
    - **Description:** Horizontal distance multiplier between each character. Overrides `Offset`.
    - **Type:** `Float`

- `OffsetV`
    - **Description:** Vertical distance multiplier between each character. Overrides `Offset`.
    - **Type:** `Float`

- `Wrap`
    - **Description:** Number of characters before line break.
    - **Type:** `Integer`

- `Justify`
    - **Description:** Text alignment. Can be `left` (default), `right` or `center` (case insensitive).
    - **Type:** `String`

- `Update`
    - **Description:** Updates values constantly (for example, time). The value is the number of skipped frames. If value is less than 0, it disables `Update`.
    - **Type:** `Integer`
    
- `Style`
    - **Description:** Which font style (texture) to use in the current text. Currently supports from 1 to 5. Defaults to 1 if style doesn't exist.
    - **Type:** `Integer` 

- `Color`
    - **Description:** Name of color or vector. Currently supports `red`, `green`, `blue`, `white`, `black`, `yellow`, `purple`, `cyan` (case insensitive) or a tuple or list like `(1, 0.5, 0.1, 1)` representing RGBA values.
    - **Type:** `String`

- `Id`
    - **Description:** Identifier of current text. Can be used to update texts with specific identifiers with `UpdateText` messages.
    - **Type:** `String`

Known Issues
============

There's some issues I noticed when using BGText, so they are on the list to be fixed or amenized on the future.

Script performance is not optimal
--------------------------------------------

For portability reasons, I chose to use the Script mode on Python controller instead of Module mode. This fixes some script import issues and gives freedom for the developer to put BGText blend file wherever it wants to, but it comes with a price. As the Script mode makes the script be parsed at runtime, it's much slower than the module Mode, and this can be a serious issue when using lots of BGText instances with the `Update` property. I don't plan to change the controller mode for the already mentioned reasons, but the `bgtext.py` script is already in a module format, so if the performance becomes a serious issue to you, you could only change the entry points on the Python controllers of BGText blend file to fit your needs. The comments on the last lines of the `bgtext.py` will explain what to do.

Extras
======

Along with the default font style textures, BGText comes with some image overlays for you to design your own font style textures. They are at the `source` directory, and comes with a single overlay (`TextStyleOverlay.png`) or multiple overlays (directory `TextStyleOverlay`). Those are useful when you're working with a image editor that supports layers.

The character's order is the following:


```text
! " # $ % & ' ( ) * + , - . / 0
1 2 3 4 5 6 7 8 9 : ; < = > ? @
A B C D E F G H I J K L M N O P
Q R S T U V W X Y Z [ \ ] ^ _ `
a b c d e f g h i j k l m n o p
q r s t u v w x y z { | } ~ ¡ ¢
£ ¥ © ® À Á Â Ã Ç É Ê Í Ñ Ó Ô Õ
Ú Ü à á â ã ç é ê í ñ ó ô õ ú ü
```
