from os import path as opath
from os import listdir, getcwd
__all__ = ['Cenux_datapoint', 'Cenux_question']


class Cenux_datapoint(object):

    """This is a data point class for Cenux."""

    def __init__(self, inputfile, outputfile, timelimit=1., memorylimit=128.,
                 score=None, info=False, index='', **kwargs):
        if not (opath.exists(inputfile) and opath.isfile(inputfile)):
            raise ValueError("Input file {0} is not valid.".format(inputfile))
        if not (opath.exists(outputfile) and opath.isfile(outputfile)):
            raise ValueError(
                "Output file {0} is not valid.".format(outputfile))
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.timelimit = timelimit
        self.memorylimit = memorylimit
        self.score = score
        self.index = index
        self.__kwargs = kwargs
        if info:
            print "## Datapoint {0} & {1} added.".format(inputfile, outputfile)

    def __str__(self):
        return 'Cenux Datapoint ' + str(self.index)

    def __repr__(self):
        return 'Cenux Datapoint ' + str(self.index)

    def __eq__(self, other):
        return (isinstance(other, Cenux_datapoint) and
                (self.inputfile == other.inputfile) and
                (self.outputfile == other.outputfile) and
                (self.memorylimit == other.memorylimit) and
                (self.timelimit == other.timelimit) and
                ((self.score and other.score and self.score == other.score)
                 or not(self.score and other.score)))

    def set_timelimit(self, timelimit=1., **kwargs):
        '''Set the time limit for data point(second)
        Default as 1 second.'''
        self.timelimit = timelimit

    def set_memorylimit(self, memorylimit=128., **kwargs):
        '''Set the memory limit for data point(128MB)
        Default as 128MB.'''
        self.memorylimit = memorylimit

    def set_inputfile(self, inputfile, **kwargs):
        '''Set the input file path for data point'''
        self.inputfile = inputfile

    def set_outputfile(self, outputfile, **kwargs):
        '''Set the output file path for data point'''
        self.outputfile = outputfile

    def set_score(self, score, **kwargs):
        '''Set the score for data point'''
        self.score = score


class Cenux_question(object):

    """This is a question class for Cenux."""

    def __init__(self, name=None, sourcefilename=None, timelimit=1.,
                 memorylimit=128., datapoint=[], **kwargs):
        if not sourcefilename:
            sourcefilename = name
        self.name = name
        self.sourcefilename = sourcefilename
        self.timelimit = timelimit
        self.memorylimit = memorylimit
        self.__kwargs = kwargs
        if type(datapoint) == list and all([isinstance(i, Cenux_datapoint) for i in datapoint]):
            self.datapoint = datapoint
        else:
            self.datapoint = []
            print "*** Could not read datapoint. Datapoint set to empty list."

    def __str__(self):
        return 'Cenux Datapoint ' + self.name + '({0} datapoints)'.format(len(self.datapoint))

    def __repr__(self):
        return 'Cenux Datapoint ' + self.name + '({0} datapoints)'.format(len(self.datapoint))

    def __getitem__(self, index):
        return self.datapoint[index]

    def __len__(self):
        return len(self.datapoint)

    def add_datapoint(self, inputfile, outputfile, score=None, auto=1, **kwargs):
        '''Add datapoint to the question.
        inputfile: inpuut file path
        outputfile: output file path
        score: the score for this data point
        timelimit: the time limit for this datapoint, default as the question's limit.
        memorylimit: the memory limit for this datapoint, default as the question's limit.
        info: print information
        auto: add similar datapoints automaticly, default as 1
        '''

        info = kwargs.pop("info", 1)
        timelimit = kwargs.pop("timelimit", self.timelimit)
        memorylimit = kwargs.pop("memorylimit", self.memorylimit)
        self.datapoint = self.datapoint + \
            [Cenux_datapoint(inputfile, outputfile, timelimit=timelimit, memorylimit=memorylimit,
                             score=score, info=info, index=len(self.datapoint), **kwargs)]
        if auto:
            print "\n## Add datapoint autometicly."
            inpath, inname = opath.split(inputfile)
            outpath, outname = opath.split(outputfile)
            import re
            rr = re.compile("(\D*)(\d+)(\D*)")
            inmatch = rr.match(inname)
            outmatch = rr.match(outname)
            if not(inmatch and outmatch):
                print "*** Couldn't recongnize the file name. Only 1 datapoint added."
            elif inmatch.span() != (0, len(inname)) or outmatch.span() != (0, len(outname)):
                print "*** Couldn't recongnize the file name. Only 1 datapoint added."
            elif inmatch.groups()[1] != outmatch.groups()[1]:
                print "*** Couldn't recongnize the file name. Only 1 datapoint added."
            else:
                informat = inmatch.groups()
                outformat = outmatch.groups()
                intemp = [j for j in [i for i in listdir(inpath) if rr.match(i)] if rr.match(
                    j).span() == (0, len(j)) and rr.match(j).groups()[::2] == informat[::2]]
                outtemp = [j for j in [i for i in listdir(outpath) if rr.match(i)] if rr.match(
                    j).span() == (0, len(j)) and rr.match(j).groups()[::2] == outformat[::2]]
                informat1 = list(informat)
                outformat1 = list(outformat)
                for i in sorted(list(set([rr.match(i).groups()[1] for i in intemp]).intersection(set([rr.match(i).groups()[1] for i in outtemp]))), cmp=lambda x, y: cmp(int(x), int(y))):
                    if i == informat[1]:
                        continue
                    informat1[1] = i
                    outformat1[1] = i
                    self.datapoint = self.datapoint + [Cenux_datapoint(opath.join(inpath, ''.join(informat1)),
                                                                       opath.join(
                                                                           outpath, ''.join(outformat1)),
                                                                       timelimit=timelimit,
                                                                       memorylimit=memorylimit,
                                                                       score=score,
                                                                       info=info,
                                                                       index=len(self.datapoint), **kwargs)]

    def set_timelimit(self, timelimit=1., **kwargs):
        '''Set the time limit for all data point in the question.(second)
        Default as 1 second.'''
        self.timelimit = timelimit
        for i in self.datapoint:
            i.set_timelimit(timelimit)

    def set_memorylimit(self, memorylimit=128., **kwargs):
        '''Set the memory limit for all data point in the question.(MB)
        Default as 128MB.'''
        self.memorylimit = memorylimit
        for i in self.datapoint:
            i.set_memorylimit(memorylimit)

    def set_score(self, score, **kwargs):
        '''Set the score for all data point in the question.'''
        for i in self.datapoint:
            i.set_score(score)

    def set_name(self, name, source=True, **kwargs):
        '''Set the question name.
        If the sourcefilename is empty, it will be set to the source file name too.
        source option could be set to False if you want to keep the sourcefilename empty.'''
        self.name = name
        if source:
            self.sourcefilename = name

    def set_sourcefilename(self, sourcefilename, **kwargs):
        '''Set the source file name without file extension'''
        self.sourcefilename = sourcefilename

    def get_scores(self):
        '''Get score for all datapoint'''
        return [i.score for i in self.datapoint]

    def get_timelimits(self):
        '''Get time limits for all datapoint'''
        return [i.timelimit for i in self.datapoint]

    def get_memorylimits(self):
        '''Get memory limits for all datapoint'''
        return [i.memorylimit for i in self.datapoint]


class Cenux_competition(object):

    '''This is a competition class for Cenux.'''

    def __init__(self, name, path=None, **kwargs):
        self.name = name
        if not path:
            path = opath.abspath(getcwd())
        self.path = path
        self.__fullpath = opath.join(path, name + '.Cenux')
        f = open(self.__fullpath, 'w')
        f.close()
        self.questions = []

    def set_name(self, name, **kwargs):
        f = open(self.__fullpath, 'r')
        a = f.read()
        f.close()

        self.name = name
        self.__fullpath = opath.join(path, name + '.Cenux')
        f = open(self.__fullpath, 'w')
        f.write(a)
        f.close()
