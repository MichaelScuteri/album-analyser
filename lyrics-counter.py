import re
from collections import Counter

# Input the lyrics
lyrics = """
I'm tryna put you in the worst mood, ah
P1 cleaner than your church shoes, ah
Milli point two just to hurt you, ah
All red lamb just to tease you, ah
None of these toys on lease too, ah
Made your whole year in a week too, yeah
Main bitch out of your league too, ah
Side bitch out of your league too, ah
House so empty, need a centerpiece
Twenty racks, a table cut from ebony
Cut that ivory into skinny pieces
Then she clean it with her face, man
I love my baby
You talking money, need a hearing aid
You talking 'bout me, I don't see the shade
Switch up my style, I take any lane
I switch up my cup, I kill any pain
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
Look what you've done!
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
I'm a motherfuckin' Starboy
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
Look what you've done!
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
I'm a motherfuckin' Starboy
Every day a nigga try to test me, ah
Every day a nigga try to end me, ah
Pull off in that roadster SV, ah
Pockets over weight getting hefty, ah
Coming for the king, that's a far cry
I come alive in the fall time I
No competition, I don't really listen
I'm in the blue Mulsanne bumping New Edition
House so empty, need a centerpiece
Twenty racks, a table cut from ebony
Cut that ivory into skinny pieces
Then she clean it with her face, man
I love my baby
You talking money, need a hearing aid
You talking 'bout me, I don't see the shade
Switch up my style, I take any lane
I switch up my cup, I kill any pain
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
Look what you've done!
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
I'm a motherfuckin' Starboy
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
Look what you've done!
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
I'm a motherfuckin' Starboy
Let a nigga brag Pitt
Legend of the fall took the year like a bandit
Bought mama a crib and a brand new wagon
Now she hit the grocery shop looking lavish
Star Trek roof in that Wraith of Khan
Girls get loose when they hear this song
Hundred on the dash get me close to God
We don't pray for love, we just pray for cars
House so empty, need a centerpiece
Twenty racks, a table cut from ebony
Cut that ivory into skinny pieces
Then she clean it with her face
Man, I love my baby
You talking money, need a hearing aid
You talking 'bout me, I don't see the shade
Switch up my style, I take any lane
I switch up my cup, I kill any pain
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
Look what you've done!
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
I'm a motherfuckin' Starboy
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
Look what you've done!
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
I'm a motherfuckin' Starboy
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
Look what you've done!
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
I'm a motherfuckin' Starboy
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
Look what you've done!
Ha-ha-ha-ha-ha-ha-ha-ha-ha-ha
I'm a motherfuckin' Starboy 
"""

filtered_words = []

words = re.findall(r'\b\w+\b', lyrics.lower())
word_count = Counter(words)
excluded_words = ['the','and','that', 'your', 'you']

for word in words:
    if word not in excluded_words and len(word) >= 3:
        filtered_words.append(word)

print(Counter(filtered_words).most_common(20))

