from grammar import Rule, Many, Production, maybe
from helpers import pluralize, resolve_pronouns, replace_pronouns, replace_you

# Declarations
Verb, Verb3rd, Adverb, Noun, Adjective, Name, NamePhrase, Subject3rd, Subject, Object, IfPhrase, WhilePhrase, WhenPhrase, \
Conditional, Question, Statement, Command, Sentence, Novel, Article, ArticlePlural = Rule.declare_all(21)

#import pdb; pdb.set_trace()
# Definitions
Verb.define('move', 'kick', 'hit', 'caress', 'use', 'super punch', 'punch')
Verb3rd = Verb.clone().transform(pluralize)
Adverb.define('quickly', 'slowly', 'furiously', 'lovingly')
Noun.define('bird', 'dog', 'dinosaur', 'force', 'Masterball', 'alien')
Adjective.define('large', 'tiny', 'crazy', 'psychopathic')
Name.define('Dio', 'Lem', 'Hackerman', 'Benny', 'Luke')
Article.define('the', 'this', 'that', 'this one', 'that one', 'a', 'some')
ArticlePlural.define('the', 'these', 'those', 'all these', 'all those', 'many', 'some')

NamePhrase.define(Production(',', Name))
Subject3rd.define(
    Production(Article, Many(Adjective, 0, 1), Noun),
    'he', 'she', 'it', Name
)
Subject.define(
    'you', 'they', 'we', 'y\'all',
    Production(ArticlePlural, Many(Adjective, 0, 1), 
        Noun.clone().transform(pluralize)
    )
)
Object.define(
    'you', 'them', 'us', 'him', 'her', 'y\'all', 'me', Name, 
    Production(ArticlePlural, Many(Adjective, 0, 1), Noun.clone().transform(pluralize)), 
    Production(Article, Many(Adjective, 0, 1), Noun)
)

IfPhrase.define(Production('if', Statement), Production('only if', Statement), Production('if and only if', Statement))
WhenPhrase.define(Production('when', Statement),)
WhilePhrase.define(Production('while', Statement), Production('as', Statement))
Conditional.define(
    Production(maybe(IfPhrase), maybe(WhilePhrase), maybe(WhenPhrase)),
    Production(maybe(IfPhrase), maybe(WhenPhrase), maybe(WhilePhrase)),
    Production(maybe(WhenPhrase), maybe(WhilePhrase), maybe(IfPhrase)),
    Production(maybe(WhenPhrase), maybe(IfPhrase), maybe(WhilePhrase)),
    Production(maybe(WhilePhrase), maybe(WhenPhrase), maybe(IfPhrase)),
    Production(maybe(WhilePhrase), maybe(IfPhrase), maybe(WhenPhrase)),
)

Question.define(
    Production(
        maybe(Production(Conditional, ',')), 
        'does', Subject3rd, Verb, Object, Many(Adverb, 0, 1),
        maybe(Conditional),
    ).set_pre(replace_pronouns(1, 3)), 
    Production(
        maybe(Production(Conditional, ',')), 
        'do', Subject, Verb, Object, Many(Adverb, 0, 1),
        maybe(Conditional),
    ).set_pre(replace_pronouns(1, 3)),
)
Statement.define(
    Production(Subject, Many(Adverb, 0, 1), Verb, Object,).set_pre(replace_pronouns(0, 3)), 
    Production(Subject3rd, Many(Adverb, 0, 1), Verb3rd, Object,).set_pre(replace_pronouns(0, 3)),
)
Command.define(
    Production(
        maybe(Production(Conditional, ',')), 
        Verb, Object, Many(Adverb, 0, 1), Many(NamePhrase, 0, 1),
        maybe(Conditional),
    ).set_pre(replace_you(2))
)
Sentence.define(
    Production(Statement, '.'),
    Production(Question, '?'),
    Production(Command, '!'),
).set_post(lambda s: s[0].upper() + s[1:]).set_distr([0, 0.5, 0.5])

Novel.define(Many(Sentence, 1, 10))


print(Novel.generate())