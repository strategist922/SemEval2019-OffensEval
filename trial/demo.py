#! /usr/bin/env python
# _*_coding:utf-8_*_
# project: SemEval2019
# Author: zcj
# @Time: 2019/1/16 0:03

#! /usr/bin/env python
# _*_coding:utf-8_*_
# project: SemEval2019
# Author: zcj
# @Time: 2019/1/4 10:18

import re

def emoji_to_text(review_text):

    # review_text = str(review_text)
    review_text = review_text.replace("👊", " Oncoming Fist ")
    review_text = review_text.replace("😂", " Face With Tears of Joy ")
    review_text = review_text.replace(" 🎶 ", " Musical Notes ")
    review_text = review_text.replace("🎶 ", " Musical Notes ")
    review_text = review_text.replace("♥️",  " Heart Suit ")
    review_text = review_text.replace("♥", " Heart Suit ")
    review_text = review_text.replace("👏", " Clapping Hands ")
    review_text = review_text.replace(" ✔️", " Heavy Check Mark ")
    review_text = review_text.replace("✔", " Heavy Check Mark ")
    review_text = review_text.replace(" 🙉 ", " Hear-No-Evil Monkey ")
    review_text = review_text.replace("🙉", " Hear-No-Evil Monkey ")
    review_text = review_text.replace("🤔", " Thinking Face ")
    review_text = review_text.replace("🤷‍♂", " Man Shrugging ")
    review_text = review_text.replace("️👀	", " Eyes ")
    review_text = review_text.replace("👀", " Eyes ")
    review_text = review_text.replace("🗽", " Statue of Liberty ")
    review_text = review_text.replace("😀", " Grinning Face " )
    review_text = review_text.replace("👌", " OK ")
    review_text = review_text.replace("🙄", " Face With Rolling Eyes ")
    review_text = review_text.replace("💚", " Green Heart ")
    review_text = review_text.replace("🤠", " Cowboy Hat Face ")
    review_text = review_text.replace("👍", " Thumbs Up ")
    review_text = review_text.replace("❤", " Red Heart ")
    review_text = review_text.replace("❤️", " Red Heart ")
    review_text = review_text.replace("*", " Asterisk ")
    review_text = review_text.replace("😌", " Relieved Face ")
    review_text = review_text.replace("😢", " Crying Face ")
    review_text = review_text.replace("💛", " Yellow Heart ")
    review_text = review_text.replace("😑", " Expressionless Face ")
    review_text = review_text.replace("😄", " Grinning Face With Smiling Eyes ")
    review_text = review_text.replace("🤨", " Face With Raised Eyebrow ")
    review_text = review_text.replace("$", " dollar ")
    review_text = review_text.replace("💕", " Two Hearts ")
    review_text = review_text.replace("🙏", " Folded Hands ")
    review_text = review_text.replace("😉", " Winking Face ")
    review_text = review_text.replace("🔥", " Fire ")
    review_text = review_text.replace("👍🏻", " Thumbs Up: Light Skin Tone ")
    review_text = review_text.replace("😅", " Grinning Face With Sweat ")
    review_text = review_text.replace("😍", " Smiling Face With Heart-Eyes ")
    review_text = review_text.replace("😗", " Kissing Face ")
    review_text = review_text.replace("💜", " Purple Heart ")
    review_text = review_text.replace("😭", " Loudly Crying Face ")
    review_text = review_text.replace("🤦🏻‍♀", " Woman Facepalming: Light Skin Tone ")
    review_text = review_text.replace("🤷", " Person Shrugging ")
    review_text = review_text.replace("☝️", " Index Pointing Up ")
    review_text = review_text.replace("☝", " Index Pointing Up ")
    review_text = review_text.replace("🤟", " Love-You Gesture ")
    review_text = review_text.replace("😊", " Smiling Face With Smiling Eyes ")
    review_text = review_text.replace("🌹", " Rose ")
    review_text = review_text.replace("😁", " Beaming Face With Smiling Eyes ")
    review_text = review_text.replace("❣", " Heavy Heart Exclamation ")
    review_text = review_text.replace("👍🏼", " Thumbs Up: Medium-Light Skin Tone ")
    review_text = review_text.replace("👏🏼", " Clapping Hands: Medium-Light Skin Tone ")
    review_text = review_text.replace("🙏🏼", " Folded Hands: Medium-Light Skin Tone ")
    review_text = review_text.replace("✌🏼", " Victory Hand: Medium-Light Skin Tone ")
    review_text = review_text.replace("👮🏻", " Police Officer: Light Skin Tone ")
    review_text = review_text.replace("👩🏻‍✈‍", " Woman Pilot: Light Skin Tone ")
    review_text = review_text.replace("👏🏻‍", " Clapping Hands: Light Skin Tone ")
    review_text = review_text.replace("😛", " Face With Tongue ")
    review_text = review_text.replace("❤️", " Red Heart ")
    review_text = review_text.replace("😆", " Grinning Squinting Face ")
    review_text = review_text.replace("😎", " Smiling Face With Sunglasses ")
    review_text = review_text.replace("🤷‍♀", " Woman Shrugging ")
    review_text = review_text.replace("😚", " Kissing Face With Closed Eyes ")
    review_text = review_text.replace("🙌🏾", " Raising Hands: Medium-Dark Skin Tone ")
    review_text = review_text.replace("😳", " Flushed Face ")
    review_text = review_text.replace("✌️", " Victory Hand ")
    review_text = review_text.replace("🙈", " See-No-Evil Monkey ")
    review_text = review_text.replace("☕️", " Hot Beverage ")
    review_text = review_text.replace("☕", " Hot Beverage ")
    review_text = review_text.replace("🙌🏽", " Raising Hands: Medium Skin Tone ")
    review_text = review_text.replace("💯", " Hundred Points ")
    review_text = review_text.replace("👏🏽", " Clapping Hands: Medium Skin Tone ")
    review_text = review_text.replace("🤣", " Rolling on the Floor Laughing ")
    review_text = review_text.replace("😶", " Face Without Mouth ")
    review_text = review_text.replace("💥", " Collision ")
    review_text = review_text.replace("‼️", " Double Exclamation Mark ")
    review_text = review_text.replace("‼", " Double Exclamation Mark ")
    review_text = review_text.replace("😳", " Flushed Face ")
    review_text = review_text.replace("😘", " Face Blowing a Kiss ")
    review_text = review_text.replace("🎂", " Birthday Cake ")
    review_text = review_text.replace("🙌", " Raising Hands ")
    review_text = review_text.replace("😪", " Sleepy Face ")
    review_text = review_text.replace("🐇", " Rabbit ")
    review_text = review_text.replace("🕳️", " Hole ")
    review_text = review_text.replace("😡", " Pouting Face ")
    review_text = review_text.replace("🙏🏻", " Folded Hands: Light Skin Tone ")
    review_text = review_text.replace("💙", " Blue Heart ")
    review_text = review_text.replace("💝", " Heart With Ribbon ")
    review_text = review_text.replace("😅", " Grinning Face With Sweat ")
    review_text = review_text.replace("🌸", " Cherry Blossom ")
    review_text = review_text.replace("📣", " Megaphone ")
    review_text = review_text.replace("🌪", " Tornado ")
    review_text = review_text.replace("⛏️", " Pick ")
    review_text = review_text.replace("⛏", " Pick ")
    review_text = review_text.replace("👎", " Thumbs Down ")
    review_text = review_text.replace("😩", " Weary Face ")
    review_text = review_text.replace("😣", " Persevering Face ")
    review_text = review_text.replace("🥀", " Wilted Flower ")
    review_text = review_text.replace("🐍", " Snake ")
    review_text = review_text.replace("💞", " Revolving Hearts ")
    review_text = review_text.replace("📱", " Mobile Phone ")
    review_text = review_text.replace("🐕 ", " dog ")
    review_text = review_text.replace("😇", " Smiling Face With Halo ")
    review_text = review_text.replace("😤", " Face With Steam From Nose ")
    review_text = review_text.replace("👊🏽", " Oncoming Fist: Medium Skin Tone ")
    review_text = review_text.replace("⁉️", " Exclamation Question Mark ")
    review_text = review_text.replace("⁉", " Exclamation Question Mark ")
    review_text = review_text.replace("🐨", " Koala ")
    review_text = review_text.replace("🐻", " Bear Face ")
    review_text = review_text.replace("🐨", " Koala ")
    review_text = review_text.replace("🛑", " Stop Sign ")
    review_text = review_text.replace("👉", " Backhand Index Pointing Right ")
    review_text = review_text.replace("👊🏻", " Oncoming Fist: Light Skin Tone ")
    review_text = review_text.replace("🤥", " Lying Face ")
    review_text = review_text.replace("🙋", " Person Raising Hand ")
    review_text = review_text.replace("💋", " Kiss Mark ")
    review_text = review_text.replace("🎁", " Wrapped Gift ")
    review_text = review_text.replace("⭐️", " Star ")
    review_text = review_text.replace("⭐", " Star ")
    review_text = review_text.replace("🤐"," Zipper-Mouth Face ")
    review_text = review_text.replace("❄️"," Snowflake ")
    review_text = review_text.replace("❄", " Snowflake ")
    review_text = review_text.replace("🤢", " Nauseated Face ")
    review_text = review_text.replace("😈", " Smiling Face With Horns ")
    review_text = review_text.replace("🧐", " Face With Monocle ")
    review_text = review_text.replace("🤦🏾‍♀️", " Woman Facepalming: Medium-Dark Skin Tone ")
    review_text = review_text.replace("👋", " Waving Hand ")
    review_text = review_text.replace("🐾", " Paw Prints ")
    review_text = review_text.replace("💀", " Skull")
    review_text = review_text.replace("😋", " Face Savoring Food ")
    review_text = review_text.replace("😢", " Crying Face ")
    review_text = review_text.replace("🤬", " Face With Symbols on Mouth ")
    review_text = review_text.replace("😒", " Unamused Face ")
    review_text = review_text.replace("🤒", " Face With Thermometer ")
    review_text = review_text.replace("💼", " Briefcase ")
    review_text = review_text.replace("🕶", " Sunglasses ")
    review_text = review_text.replace("👢", " Woman’s Boot ")
    review_text = review_text.replace("⚽️", " Soccer Ball ")
    review_text = review_text.replace("⚽", " Soccer Ball ")
    review_text = review_text.replace("🤗", " Hugging Face ")
    review_text = review_text.replace("😩", " Weary Face ")
    review_text = review_text.replace("🤷🏼‍♂", " Man Shrugging: Medium-Light Skin Tone ")
    review_text = review_text.replace("🤷🏼‍♂️", " Man Shrugging: Medium-Light Skin Tone ")
    review_text = review_text.replace("🤦‍♀", " Woman Facepalming")
    review_text = review_text.replace("🤦‍♀️", " Woman Facepalming")
    review_text = review_text.replace("💪🏻", " Flexed Biceps: Light Skin Tone ")
    review_text = review_text.replace("💩", " Pile of Poo")
    review_text = review_text.replace("💉", " Syringe ")
    review_text = review_text.replace("😱"," Face Screaming in Fear ")
    review_text = review_text.replace("😠 "," Angry Face ")
    review_text = review_text.replace("🌍", " Globe Showing Europe-Africa ")
    review_text = review_text.replace("👮‍♀️", " Woman Police Officer ")
    review_text = review_text.replace("👮‍♀", " Woman Police Officer ")
    review_text = review_text.replace("💰", " Money Bag ")
    review_text = review_text.replace("💖", " Sparkling Heart ")
    review_text = review_text.replace("😏", " Smirking Face ")
    review_text = review_text.replace("💁🏽‍♀️", " Woman Tipping Hand: Medium Skin Tone ")
    review_text = review_text.replace("💁🏽‍♀", " Woman Tipping Hand: Medium Skin Tone ")
    review_text = review_text.replace("🌚"," New Moon Face ")
    review_text = review_text.replace("🤯"," Exploding Head ")

    # review_text = " ".join(review_text)
    return review_text


def abbreviation_to_text(review_text):
    review_text = re.sub("you’re", "you are",review_text)
    review_text = re.sub("You’re", "You are",review_text)
    review_text = re.sub("You're", "You are",review_text)
    # review_text = review_text.replace("You’re", "You are")
    # review_text = review_text.replace("You're", "You are")
    review_text = review_text.replace("should've", "should have ")
    review_text = review_text.replace("it’s", "it is")
    review_text = review_text.replace("It’s", "It is")
    review_text = review_text.replace("It's","It is")
    review_text = review_text.replace("doesn’t", "dose not")
    review_text = review_text.replace("What’s", "What is")
    review_text = review_text.replace(" what's", "what is")
    review_text = review_text.replace("you've", "you have")
    review_text = review_text.replace("he’s", "he is")
    review_text = review_text.replace("He’s", "He is")
    review_text = review_text.replace("There's", "There is")
    review_text = review_text.replace("there's", "there is")
    review_text = review_text.replace("women's", "woman is")
    review_text = review_text.replace("men's", "men is")
    review_text = review_text.replace("That's", "That is")
    review_text = review_text.replace("that’s", "that is")
    review_text = review_text.replace("She's", "she is")
    review_text = review_text.replace("she’s", "she is")
    review_text = review_text.replace("didn’t", "did not")
    review_text = review_text.replace("don't", "do not")
    review_text = review_text.replace("don’t", "do not")
    review_text = review_text.replace("Don't", "Do not")
    review_text = review_text.replace("I'll","I will")
    review_text = review_text.replace("I’ll", "I will")
    review_text = review_text.replace("I'd", "I would")
    review_text = review_text.replace("I’ve", "I have")
    review_text = review_text.replace("I’m", "I am")
    review_text = review_text.replace("i’m", "i am")
    review_text = review_text.replace("Let's", "Let is")
    review_text = review_text.replace("won’t", "won not")
    review_text = review_text.replace("can’t", "can not")
    review_text = review_text.replace("hadn't", "had not")
    review_text = review_text.replace("wouldn’t", "would not")
    review_text = review_text.replace("Shouldn't", "Should not")
    review_text = review_text.replace("shouldn't", "should not")
    review_text = review_text.replace("shouldn’t", "should not")
    review_text = review_text.replace("aren't", "are not")
    review_text = review_text.replace("She’s", "She is")
    review_text = review_text.replace("she’s", "she is")
    review_text = review_text.replace("She’ll", "She will")
    review_text = review_text.replace("she’ll", "she will")
    review_text = review_text.replace("Couldn't", "Could not")
    review_text = review_text.replace("isn’t", "is not")


    # review_text = " ".join(review_text)
    return review_text

