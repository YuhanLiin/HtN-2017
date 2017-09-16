from grammar import Rule, Many

def pluralize(words):
    return [word + 'es' if word.endswith('s') or word.endswith('ch') else word+'s' for word in words]

Verb = Rule('move', 'kick', 'hit', 'caress', 'use', 'super punch', 'punch')
Verb3rd = Verb.transform(pluralize)
Adverb = Rule('quickly', 'slowly', 'furiously', 'lovingly')
Noun = Rule('bird', 'dog', 'dinosaur', 'force')
Adjective = Rule('large', 'tiny', 'crazy', 'psychopathic')
Name = Rule('Dio', 'Lem', 'Hackerman', 'Benny')

NamePhrase = Rule([',', Name])
Subject3rd = Rule(
    ['the', Many(Adjective, 0, 1), Noun],
    'he', 'she', 'it', Name
)
Subject = Rule(
    'you', 'they', 'we', 'you guys', 
    ['the', Many(Adjective, 0, 1), Noun.transform(pluralize)]
)
Object = Rule(
    'you', 'them', 'us', 'him', 'her', Name, 
    ['the', Many(Adjective, 0, 1), Noun.transform(pluralize)], 
    ['the', Many(Adjective, 0, 1), Noun]
)

Question = Rule(
    ['Does', Subject3rd, Verb, Object, Many(Adverb, 0, 1), '?'], 
    ['Do', Subject, Verb, Object, Many(Adverb, 0, 1), '?'],
)
Statement = Rule(
    [Subject, Many(Adverb, 0, 1), Verb, Object, '.'], 
    [Subject3rd, Many(Adverb, 0, 1), Verb3rd, Object, '.'],
)
Command = Rule(
    [Verb, Object.set_post(lambda o: 'yourself' if o == 'you' else o), Many(Adverb, 0, 1), Many(NamePhrase, 0, 1), '!'],
)
Sentence = Rule(
    Statement, Question, Command
).set_post(lambda s: s[0].upper() + s[1:])

Novel = Rule(Many(Sentence, 1, 10))


print(Novel.generate())