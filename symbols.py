from grammar import Rule, Many

Rule.punctuation = ",.!?"

Verb=Rule(['move', 'kick', 'hit', 'caress', 'use'])
Adverb=Rule(['quickly', 'slowly', 'furiously'])
Noun=Rule(['bird', 'dog', 'dinosaur', 'force'])
Adjective=Rule(['large', 'tiny', 'crazy', 'psychopathic'])
Name=Rule(['Dio', 'Lem', 'Hackerman'])

Subject=Rule([['the', Adjective, Noun], 'we', 'they', Name])
Object=Rule(['you', 'them', 'us', ['the', Adjective, Noun], Name])
Question=Rule([['Did', Subject, Verb, Object, Adverb, '?'],])
Statement=Rule([[Subject, Adverb, Verb, Object, '.'],])
Command=Rule([[Verb, Object, Adverb, '!'],])
Sentence=Rule([Statement, Question, Command], lambda s: s[0].upper() + s[1:])
Novel=Rule([Many(Sentence, 1, 10)])


print(Novel.generate())