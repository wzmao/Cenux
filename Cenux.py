import os

__all__ = ['Cenux_datapoint', 'Cenux_question',
           'Cenux_user', 'Cenux_competition']


def __searchfile(p, f, exp, **kwargs):
    if not (os.path.exists(p) and os.path.isdir(p)):
        return []
    temp = []
    su = [f + i for i in exp]
    ll = os.listdir(p)
    for i in ll:
        if i in su and os.path.isfile(os.path.join(p, i)):
            temp = temp + [os.path.abspath(os.path.join(p, i))]
    for i in ll:
        if os.path.isdir(os.path.join(p, i)):
            temp += __searchfile(os.path.join(p, i), f, **kwargs)
    return temp


class Cenux_datapoint(object):

    """This is a data point class for Cenux."""

    def __init__(self, inputfile, outputfile, timelimit=1., memorylimit=128.,
                 score=None, info=False, index='', **kwargs):
        if not (os.path.exists(inputfile) and os.path.isfile(inputfile)):
            raise ValueError("Input file {0} is not valid.".format(inputfile))
        if not (os.path.exists(outputfile) and os.path.isfile(outputfile)):
            raise ValueError(
                "Output file {0} is not valid.".format(outputfile))
        self.inputfile = str(inputfile)
        self.outputfile = str(outputfile)
        self.timelimit = float(timelimit)
        self.memorylimit = float(memorylimit)
        if not score == None:
            score = float(score)
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
        self.timelimit = float(timelimit)

    def set_memorylimit(self, memorylimit=128., **kwargs):
        '''Set the memory limit for data point(128MB)
        Default as 128MB.'''
        self.memorylimit = float(memorylimit)

    def set_inputfile(self, inputfile, **kwargs):
        '''Set the input file path for data point'''
        self.inputfile = str(inputfile)

    def set_outputfile(self, outputfile, **kwargs):
        '''Set the output file path for data point'''
        self.outputfile = str(outputfile)

    def set_score(self, score, **kwargs):
        '''Set the score for data point'''
        if not score == None:
            score = float(score)
        self.score = score


class Cenux_question(object):

    """This is a question class for Cenux."""

    def __init__(self, name=None, sourcefilename=None, timelimit=1.,
                 memorylimit=128., datapoint=[], **kwargs):
        if not sourcefilename:
            sourcefilename = name
        self.name = str(name)
        self.sourcefilename = str(sourcefilename)
        self.timelimit = float(timelimit)
        self.memorylimit = float(memorylimit)
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

    def __eq__(self, other):
        return (isinstance(other, Cenux_question) and
                (self.name == other.name) and
                (self.sourcefilename == other.sourcefilename) and
                (self.memorylimit == other.memorylimit) and
                (self.timelimit == other.timelimit) and
                (len(self.datapoint) == len(other.datapoint)) and
                (all([self[i] == other[i]
                      for i in range(len(self.datapoint))])))

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
            inpath, inname = os.path.split(inputfile)
            outpath, outname = os.path.split(outputfile)
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
                intemp = [j for j in [i for i in os.listdir(inpath) if rr.match(i)] if rr.match(
                    j).span() == (0, len(j)) and rr.match(j).groups()[::2] == informat[::2]]
                outtemp = [j for j in [i for i in os.listdir(outpath) if rr.match(i)] if rr.match(
                    j).span() == (0, len(j)) and rr.match(j).groups()[::2] == outformat[::2]]
                informat1 = list(informat)
                outformat1 = list(outformat)
                for i in sorted(list(set([rr.match(i).groups()[1] for i in intemp]).intersection(set([rr.match(i).groups()[1] for i in outtemp]))), cmp=lambda x, y: cmp(int(x), int(y))):
                    if i == informat[1]:
                        continue
                    informat1[1] = i
                    outformat1[1] = i
                    self.datapoint = self.datapoint + [Cenux_datapoint(os.path.join(inpath, ''.join(informat1)),
                                                                       os.path.join(
                        outpath, ''.join(outformat1)),
                        timelimit=timelimit,
                        memorylimit=memorylimit,
                        score=score,
                        info=info,
                        index=len(self.datapoint), **kwargs)]

    def set_timelimit(self, timelimit=1., **kwargs):
        '''Set the time limit for all data point in the question.(second)
        Default as 1 second.'''
        self.timelimit = float(timelimit)
        for i in self.datapoint:
            i.set_timelimit(float(timelimit))

    def set_memorylimit(self, memorylimit=128., **kwargs):
        '''Set the memory limit for all data point in the question.(MB)
        Default as 128MB.'''
        self.memorylimit = float(memorylimit)
        for i in self.datapoint:
            i.set_memorylimit(float(memorylimit))

    def set_score(self, score, **kwargs):
        '''Set the score for all data point in the question.'''
        if not score == None:
            score = float(score)
        for i in self.datapoint:
            i.set_score(score)

    def set_name(self, name, source=False, **kwargs):
        '''Set the question name.
        If the sourcefilename is empty, it will be set to the source file name too.
        source option could be set to False if you want to keep the sourcefilename empty.'''
        self.name = str(name)
        if source:
            self.sourcefilename = str(name)

    def set_sourcefilename(self, sourcefilename, **kwargs):
        '''Set the source file name without file extension'''
        self.sourcefilename = str(sourcefilename)

    def get_scores(self):
        '''Get score for all datapoint'''
        return [i.score for i in self.datapoint]

    def get_timelimits(self):
        '''Get time limits for all datapoint'''
        return [i.timelimit for i in self.datapoint]

    def get_memorylimits(self):
        '''Get memory limits for all datapoint'''
        return [i.memorylimit for i in self.datapoint]

    def remove_dulplicate(self):
        temp = self.datapoint
        a = [True] * len(temp)
        for i in range(len(temp)):
            if not a[i]:
                continue
            for j in range(i + 1, len(temp)):
                if not a[j]:
                    continue
                if temp[i] == temp[j]:
                    a[j] = False
        for i in range(len(self.datapoint) - 1, -1, -1):
            if not a[i]:
                temp.pop(i)
        self.datapoint = temp
        for i in range(len(self.datapoint)):
            self.datapoint[i].index = i


class Cenux_user(object):

    '''This is a contestant class for Cenux.'''

    def __init__(self, name, **kwargs):
        self.name = str(name)
        self.code = []
        self.result = []

    def __str__(self):
        return 'Cenux contestant ' + self.name

    def __repr__(self):
        return 'Cenux contestant ' + self.name

    def add_code(self, path, **kwargs):
        if path == None:
            self.code = self.code + [None]
        else:
            if not(os.path.exists(path) and os.path.isfile(path)):
                raise ValueError("The path for the code is invalid.")
            self.code = self.code + [path]
        self.result = self.result + [None]

    def clear_code(self, **kwargs):
        self.code = []
        self.result = []

    # def add_competition(self, path, question, exp=['.c', '.cpp', '.c++', '.pas'], **kwargs):
    #     if not all([isinstance(Cenux_question) for i in question]):
    #         raise ValueError("You must provide a question list.")
    #     for i in question:
    #         temp = __searchfile(path, i.sourcefilename, exp)
    #         if len(temp) == 0:
    #             self.add_code(None)
    #         elif len(temp) == 1:
    #             self.add_code(os.path.relpath(temp[0], self.abspath))
    #         else:
    #             print '## There are more than one file for question {0}'.format(i.name)
    #             print '## You could set exp option.'
    #             self.


class Cenux_competition(object):

    '''This is a competition class for Cenux.
    You should add the questions first and then add the user.
    Cenux will collect the user's program based on the questions in this competition.
    `Save` function could be used to save the competition profile.'''

    def __init__(self, name, path=None, **kwargs):
        self.name = str(name)
        if not path:
            path = os.path.abspath(os.getcwd())
        self.abspath = path
        self.__fullfilepath = os.path.join(self.abspath, name + '.Cenux')
        f = open(self.__fullfilepath, 'w')
        f.close()
        self.question = []
        self.user = []

    def __str__(self):
        return 'Cenux Competiiton ' + self.name + '({0} qustions)'.format(len(self.question))

    def __repr__(self):
        return 'Cenux Competiiton ' + self.name + '({0} qustions)'.format(len(self.question))

    def __getitem__(self, index):
        return self.question[index]

    def __len__(self):
        return len(self.question)

    def set_name(self, name, **kwargs):
        f = open(self.__fullfilepath, 'r')
        a = f.read()
        f.close()

        if input("## Do you want to remove the original file?"):
            os.remove(self.__fullfilepath)

        self.name = name
        self.__fullfilepath = os.path.join(self.abspath, name + '.Cenux')
        f = open(self.__fullfilepath, 'w')
        f.write(a)
        f.close()

    def add_qustion(self, name, sourcefilename=None, timelimit=1., memorylimit=128., datapoint=[], inputfile=None, outputfile=None, score=None, **kwargs):
        if not sourcefilename:
            sourcefilename = name
        self.question = self.question + [Cenux_question(name=name,
                                                        sourcefilename=sourcefilename,
                                                        timelimit=timelimit,
                                                        memorylimit=memorylimit,
                                                        datapoint=datapoint)]
        if inputfile and outputfile:
            self.question[-1].add_datapoint(inputfile,
                                            outputfile, score, 1, info=1)

    def add_user(self, name=None, path=None, **kwargs):
        '''Add a user to the competition.
        You could give the path to collect the codes for the competition.
        *** Add all the questions first.'''
        if not name:
            name = str(len(self.user) + 1)
        self.user = self.user + [Cenux_user(name)]
        print '## User {0} has been added.'.format(name)
        auto = kwargs.pop('auto', None)
        exp = kwargs.pop(exp, ['.c', '.cpp', '.c++', '.pas'])
        if auto and not path:
            path = os.getcwd()
        if path:
            if not os.path.isdir(path):
                print "The path {0} is not valid. Collect the codes by collect_code.".format(path)
            else:
                self.collect_code(len(user) - 1, path, exp=exp)

    def collect_code(self, index, path, exp=['.c', '.cpp', '.c++', '.pas'] ** kwargs):
        try:
            self.user[index]
        except:
            raise ValueError("The index couldn't be recognized.")
        for i in self.question:
            temp=__searchfile(path,i.sourcefilename,exp)
            if len(temp) == 0:
                self.user[i].code+=[None]
            elif len(temp) == 1:
                # self.user[i].code+=[None]
                self.add_code(os.path.relpath(temp[0], self.abspath))
            else:
                print '## There are more than one file for question {0}'.format(i.name)
                print '## You could set exp option.'
                for j in self.user[i].code:
                    
