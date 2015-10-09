
def _name_to_value(name):
    val = {'A': 0, 'B': 2, 'C': 3, 'D': 5, 'E': 7, 'F': 8, 'G': 10}
    mod = {'#': 1, 'b': -1}
    result = val[name[0]] + sum(mod[m] for m in name[1:])
    return result % 12

def _value_to_name(value, accidentals='#'):
    name = {0: 'A', 2: 'B', 3: 'C', 5: 'D', 7: 'E', 8: 'F', 10: 'G'}
    mod = {'#': -1, 'b': 1} 
    value = value % 12
    mods = list()
    while value not in name:
        mods.append(accidentals)
        value += mod[accidentals]
    return name[value] + ''.join(mods)


class Note(object):
    def __init__(self, name, octave=0, duration=1, volume=1, *args, **kwargs):
        self.name = name[0].upper() + name[1:]
        self.octave = octave
        self.duration = duration
        self.volume = volume
        self.value = _name_to_value(self.name) + (octave * 12)

    def _play(self):
        print 'Playing %s' % self
        pass

    def __repr__(self):
        # self._play()
        return '%s%d for duration %s at volume %s' % (self.name, self.octave,
                                                    self.duration, self.volume)

    def __cmp__(self, other):
        '''
        Compares octave, name, duration, volume in that order.
        i.e. pitch, duration, volume
        By definition, Note < Chord < Phrase
        '''
        if isinstance(other, Chord) or isinstance(other, Phrase):
            return -1
        elif isinstance(other, Note):
            for attr in ['octave', 'name', 'duration', 'volume']:
                c = cmp(getattr(self, attr), getattr(other, attr))
                if c != 0:
                    return c
            return 0
        else:
            raise TypeError('%s is of type %s, but must be either Note, Chord\
                            or Phrase' % (other, type(other)))

    def __add__(self, other):
        '''
        note + note = phrase consisting of note then note
        note + chord = phrase consisting of note then chord
        note + phrase = phrase consisting of note then phrase
        '''
        if any(isinstance(other, musical) for musical in [Note, Chord, Phrase]):
            return Phrase(self, other)
        else:
            raise TypeError('%s is of type %s, but must be either Note, Chord\
                            or Phrase' % (other, type(other)))
        
    def __mul__(self, other):
        '''
        note * note = chord
        note * chord = chord with note added
        note * phrase = phrase where everything has had note added
        '''
        if isinstance(other, Note):
            return Chord(self, other)
        elif isinstance(other, Chord) or isinstance(other, Phrase):
            return other * self
        else:
            raise TypeError('%s is of type %s, but must be either Note, Chord\
                            or Phrase' % (other, type(other)))

    def __pow__(self, other):
        '''
        transposes note by number of semitones specified
        '''
        if isinstance(other, int):
            new_value = self.value + other
            name = _value_to_name(new_value)
            octave = new_value / 12
            return Note(name, octave=octave, duration=self.duration,
                        volume=self.volume)
        else:
            raise TypeError('%s is of type %s, must be an int to transpose' % (other, type(other)))


class Chord(object):

    def __init__(self, *musics):
        if any(isinstance(m, Chord) for m in musics):
            return sum(musics)
        else:
            '''Chords must be made from notes'''
            if all(isinstance(m, Note) for m in musics):
                self.notes = sorted(musics)
            else:
                raise TypeError

    def __repr__(self):
        return 'Chord containing notes\n\t' + '\n\t'.join(str(n) for n in self.notes)

    def __add__(self, other):
        '''
        chord + note = phrase consisting of note then note
        chord + chord = phrase consisting of note then chord
        chord + phrase = phrase consisting of note then phrase
        '''
        if any(isinstance(other, musical) for musical in [Note, Chord, Phrase]):
            return Phrase(self, other)
        else:
            raise TypeError('%s is of type %s, but must be either Note, Chord\
                            or Phrase' % (other, type(other)))
 
    def __mul__(self, other):
        if isinstance(other, Note):
            return Chord(*self.notes.append(other))
        elif isinstance(other, Chord):
            return Chord(*self.notes + other.notes)
        elif isinstance(other, Phrase):
            return other * self
        else:
            raise TypeError

    def __pow__(self, other):
        '''
        transposes note by number of semitones specified
        '''
        if isinstance(other, int):
            return Chord(*(n**other for n in self.notes))
        else:
            raise TypeError('%s is of type %s, must be an int to transpose' % (other, type(other)))


class Phrase(object):

    def __init__(self, *musics):
        self.musics = list()
        for m in musics:
            if isinstance(m, Phrase):
                self.musics += m.musics
            else:
                self.musics.append(m)

    def __repr__(self):
        return 'Phrase containing\n\t' + '\n\t'.join(str(m) for m in self.musics)

    def __add__(self, other):
        '''
        chord + note = phrase consisting of note then note
        chord + chord = phrase consisting of note then chord
        chord + phrase = phrase consisting of note then phrase
        '''
        if any(isinstance(other, musical) for musical in [Note, Chord, Phrase]):
            return Phrase(self, other)
        else:
            raise TypeError('%s is of type %s, but must be either Note, Chord\
                            or Phrase' % (other, type(other)))

    def __mul__(self, other):
        if isinstance(other, Note) or isinstance(other, Chord):
            return Phrase(*(m*other for m in self.musics))
        elif isinstance(other, Phrase):
            # TODO: some crazy shit to get note durations right
            pass
        else:
            raise TypeError('%s is of type %s, but must be either Note, Chord\
                            or Phrase' % (other, type(other)))

    def __pow__(self, other):
        '''
        transposes note by number of semitones specified
        '''
        if isinstance(other, int):
            return Phrase(*(n**other for n in self.musics))
        else:
            raise TypeError('%s is of type %s, must be an int to transpose' % (other, type(other)))


