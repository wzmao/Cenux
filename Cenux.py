from os import path, listdir, getcwd
__all__ = ['Cenux_datapoint', 'Cenux_question']


class Cenux_datapoint(object):

    """This is a data point class for Cenux."""

    def __init__(self, inputfile, outputfile, timelimit=1., memorylimit=128.,
                 score=None, info=False, **kwargs):
        if not (path.exists(inputfile) and path.isfile(inputfile)):
            raise ValueError("Input file {0} is not valid.")
        if not (path.exists(output) and path.isfile(output)):
            raise ValueError("Output file {0} is not valid.")
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.timelimit = timelimit
        self.memorylimit = memorylimit
        self.score = score
        self.__kwargs = kwargs
        if info:
            print "## Datapoint {0}/{1} ddded.".format(inputfile, outputfile)

    def Set_timelimit(self, timelimit=1., **kwargs):
        '''Set the time limit for data point(second)
        Default as 1 second.'''
        self.timelimit = timelimit

    def Set_memorylimit(self, memorylimit=128., **kwargs):
        '''Set the memory limit for data point(128MB)
        Default as 128MB.'''
        self.memorylimit = memorylimit

    def Set_inputfile(self, inputfile, **kwargs):
        '''Set the input file path for data point'''
        self.inputfile = inputfile

    def Set_outputfile(self, outputfile, **kwargs):
        '''Set the output file path for data point'''
        self.outputfile = outputfile

    def Set_score(self, score, **kwargs):
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
        if type(datapoint) == list and all([type(i) == Cenux_datapoint for i in datapoint]):
            self.datapoint = datapoint
        else:
            self.datapoint = []
            print "*** Could not read datapoint. Datapoint set to empty list."

    def Add_datapoint(self, inputfile, outputfile, score=None, auto=1, **kwargs):
        '''Add datapoint to the question.
        inputfile: inpuut file path
        outputfile: output file path
        score: the score for this data point
        timelimit: the time limit for this datapoint, default as the question's limit.
        memorylimit: the memory limit for this datapoint, default as the question's limit.
        auto: add similar datapoints automaticly, default as 1
        '''

        timelimit = kwargs.get("timelimit", self.timelimit)
        memorylimit = kwargs.get("memorylimit", self.memorylimit)
        self.datapoint.append(Cenux_datapoint(
            inputfile, outputfile, timelimit=timelimit, memorylimit=memorylimit, score=score, info=True, **kwargs))
        if auto:
            print "## Add datapoint autometicly."
            inpath, inname = path.split(inputfile)
            outpath, outname = path.split(outputfile)
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
                    j).span == (0, len(j)) and rr.match(j).groups()[::2] == informat[::2]]
                outtemp = [j for j in [i for i in listdir(outpath) if rr.match(i)] if rr.match(
                    j).span == (0, len(j)) and rr.match(j).groups()[::2] == outformat[::2]]
                for i in set([rr.match(i).groups()[1] for i in intemp]).intersection(set([rr.match(i).groups()[1] for i in outtemp])):
                    informat[1] = i
                    outformat[1] = i
                    self.datapoint.append(Cenux_datapoint(''.join(informat), ''.join(
                        outformat), timelimit=timelimit, memorylimit=memorylimit, score=score, info=True, **kwargs))

    def Set_timelimit(self, timelimit=1., **kwargs):
        '''Set the time limit for all data point in the question.(second)
        Default as 1 second.'''
        for i in self.datapoint:
            i.Set_timelimit(timelimit)

    def Set_memorylimit(self, memorylimit=128., **kwargs):
        '''Set the memory limit for all data point in the question.(MB)
        Default as 128MB.'''
        for i in self.datapoint:
            i.Set_memorylimit(memorylimit)

    def Set_score(self, score, **kwargs):
        '''Set the score for all data point in the question.'''
        for i in self.datapoint:
            i.Set_score(score)

    def Set_name(self, name, source=True, **kwargs):
        '''Set the question name.
        If the sourcefilename is empty, it will be set to the source file name too.
        source option could be set to False if you want to keep the sourcefilename empty.'''
        self.name = name
        if source:
            self.sourcefilename = name

    def Set_sourcefilename(self, sourcefilename, **kwargs):
        '''Set the source file name without file extension'''
        self.sourcefilename = sourcefilename


class Cenux_competition(object):

    '''This is a competition class for Cenux.'''

    def __init(self, name, path=None, **kwargs):
        self.name = name
        if not path:
            path = getcwd()
        self.__fullpath = path.join(path, name)
        f = open(self.__fullpath, 'w')
        f.close()
        self.questions = []
