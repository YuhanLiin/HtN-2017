from grammar import Rule, Many, Production
from helpers import pluralize, resolve_pronouns, replace_pronouns, replace_you

# Declarations
Verb, Verb3rd, Adverb, Noun, Adjective, Name, NamePhrase, Subject3rd, Subject, Object, IfPhrase, Question, \
Statement, Command, Sentence, Novel = Rule.declare_all(16)

#import pdb; pdb.set_trace()
# Definitions
Verb.define('move', 'kick', 'hit', 'caress', 'use', 'super punch', 'punch')
Verb3rd = Verb.clone().transform(pluralize)
Adverb.define('quickly', 'slowly', 'furiously', 'lovingly')
Noun.define('bird', 'dog', 'dinosaur', 'force', 'Masterball')
Adjective.define('large', 'tiny', 'crazy', 'psychopathic')
Name.define('Dio', 'Lem', 'Hackerman', 'Benny', 'Luke')

NamePhrase.define(Production(',', Name))
Subject3rd.define(
    Production('the', Many(Adjective, 0, 1), Noun),
    'he', 'she', 'it', Name
)
print (Noun, Noun.clone())
Subject.define(
    'you', 'they', 'we', 'y\'all',
    Production('the', Many(Adjective, 0, 1), 
        Noun.clone().transform(pluralize)
    )
)
Object.define(
    'you', 'them', 'us', 'him', 'her', 'y\'all', 'me', Name, 
    Production('the', Many(Adjective, 0, 1), Noun.clone().transform(pluralize)), 
    Production('the', Many(Adjective, 0, 1), Noun)
)

IfPhrase.define(Production('If', Statement),)

Question.define(
    Production('does', Subject3rd, Verb, Object, Many(Adverb, 0, 1), '?').set_pre(replace_pronouns(1, 3)), 
    Production('do', Subject, Verb, Object, Many(Adverb, 0, 1), '?').set_pre(replace_pronouns(1, 3)),
)
Statement.define(
    Production(Subject, Many(Adverb, 0, 1), Verb, Object, '.').set_pre(replace_pronouns(0, 3)), 
    Production(Subject3rd, Many(Adverb, 0, 1), Verb3rd, Object, '.').set_pre(replace_pronouns(0, 3)),
)
Command.define(
    Production(IfPhrase, Verb, Object, Many(Adverb, 0, 1), Many(NamePhrase, 0, 1), '!').set_pre(replace_you(2))
)
Sentence.define(
    Statement, Question, Command
).set_post(lambda s: s[0].upper() + s[1:]).set_distr([0.33, 0.33, 0.34])

Novel.define(Many(Sentence, 1, 10))


print(Novel.generate())