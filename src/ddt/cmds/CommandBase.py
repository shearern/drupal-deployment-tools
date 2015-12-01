import gflags
import sys
import os

from cPickle import dump, load

from abc import ABCMeta, abstractmethod

from py_wizard.PyMainWizard import PyMainWizard
from py_wizard.runner import run_wizard

from .questions.PathQuestion import PathQuestion


class CommandArgumentError(Exception):
    def __init__(self, parm_name, error):
        self.parm_name = parm_name
        self.parm_error = error

        if parm_name is not None:
            msg = "ERROR with parameter '%s': %s" % (parm_name, error)
        else:
            msg = 'ARGUMENT ERROR: %s' % (error)
        super(CommandArgumentError, self).__init__(msg)




class CommandBase(PyMainWizard):
    '''Class to derive from to create commands that can be run by the tool.

        When creating new commands, be sure to:
            TODO ...
    '''

    def __init__(self):
        self.argv = None        # Extra arguments (non-flags)
        self.parms = None       # Parameters from gflags or GUI

        super(CommandBase, self).__init__()



    # -- Parameter Handling --------------------------------------------------------------

    @abstractmethod
    def define_gflags(self):
        '''Define any command line flags for this command'''


    @abstractmethod
    def validate_parms(self, extra_args):
        '''Check provided parameter values and raise CommandArgumentError if needed'''


    # -- Execution -----------------------------------------------------------------------------

    @abstractmethod
    def run_command(self):
        '''Perform action of the command'''


    # -- PyWizard Overrides --------------------------------------------------------------------


    def execute(self):
        try:
            self.validate_parms(self.argv)
            self.run_command()
        except CommandArgumentError, e:
            print str(e)
            sys.exit(2)



    def configure_answer_saving(self):
        '''Setup answer saving for this run of the wizard'''
        # TODO: Should make parent class more configurable

        # Determine path for loading/saving previous answers
        self.__autosave_path = self._calc_autosave_path()
        if self.__autosave_path is None:
            return
        path = os.path.abspath(self.__autosave_path)

        # Load Previous Saved Answers (always)
        if os.path.exists(self.__autosave_path):
            with open(path, "rb") as fh:
                sa = load(fh)
                self.__saved_answers = sa['self']
                self.__saved_answers_for_sub_wizards = sa['subwizards']
                self.enable_load_prev_answers = True

        # Ask if we want to save after every answer (always)
        self.enable_autosave_answers = True

        self.enable_answer_saving = True


    def ask_question(self, question):

        # Check to see if answer specified on the commandline
        try:
            parm_value = getattr(self.parms, question.name)
            if parm_value is not None:
                return parm_value

        # Else ask user
        except AttributeError:
            pass

        # Ask user
        return super(CommandBase, self).ask_question(question)


    def ask_path(self, name, question, default=None, optional=False,
                 must_exist=False, parent_must_exist=False,
                 must_be_dir=False, must_be_file=False):
        return self.ask_simple(name, question, default, optional)


    def say_goodbye(self):
        print "Done"



def commandline_exec(command):

    # Parse commandline arguments
    command.define_gflags()
    try:
        argv = sys.argv
        command.argv = gflags.FLAGS(argv)[1:]  # parse flags
        command.parms = gflags.FLAGS
        gflags.auto_accept_defaults = True
    except gflags.FlagsError, e:
        print("%s\nUsage: %s ARGS\n%s" % (e, sys.argv[0], gflags.FLAGS))
        sys.exit(1)
    # except Exception, e:
    #     print("%s\nError: %s ARGS\n%s" % (e, sys.argv[0], gflags.FLAGS))
    #     sys.exit(1)

    run_wizard(command)
