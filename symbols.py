from grammar import Rule, Many

Rule.punctuation = ",.!?"

Verb = Rule(['move', 'kick', 'hit', 'caress', 'use'])
Verb3rd = Verb.transform(lambda words: [word + 'es' if word[-1]=='s' else word+'s' for word in words])
Adverb = Rule(['quickly', 'slowly', 'furiously'])
Noun = Rule(['bird', 'dog', 'dinosaur', 'force'])
Adjective = Rule(['large', 'tiny', 'crazy', 'psychopathic'])
Name = Rule(['Dio', 'Lem', 'Hackerman'])

Subject3rd = Rule([['the', Adjective, Noun], 'he', 'she', 'it', Name])
Subject = Rule(['you', 'they', 'we', 'you guys']) # Plural trnasforms?
Object = Rule(['you', 'them', 'us', 'him', 'her', ['the', Adjective, Noun], Name])
Question = Rule([['Does', Subject3rd, Verb3rd, Object, Adverb, '?'], ['Do', Subject, Verb, Object, Adverb, '?'],])
Statement = Rule([[Subject, Adverb, Verb, Object, '.'], [Subject3rd, Adverb, Verb3rd, Object, '.'],])
Command = Rule([[Verb, Object, Adverb, '!'],])
Sentence = Rule([Statement, Question, Command], lambda s: s[0].upper() + s[1:])
Novel = Rule([Many(Sentence, 1, 10)])


print(Novel.generate())