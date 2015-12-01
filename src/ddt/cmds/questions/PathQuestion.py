import os

from py_wizard.questions.SimpleQuestion import SimpleQuestion

# TODO: Refactor to PyWizard project
class PathQuestion(SimpleQuestion):

    def __init__(self, name, question, default=None,
                 must_exist=False, parent_must_exist=False,
                 must_be_dir=False, must_be_file=False):

        self.__must_exist = must_exist
        self.__parent_must_exist = parent_must_exist
        self.__must_be_dir = must_be_file
        self.__must_be_file = must_be_file

        super(PathQuestion, self).__init__(name, question, default)


    def get_simple_question_child_error(self, answer):

        if answer is not None:

            if self.__must_exist:
                if not os.path.exists(answer):
                    return "Path doesn't exist:"

            if self.__parent_must_exist:
                parent = os.path.dirname(os.path.abspath(answer))
                if parent is None or not os.path.exists(parent):
                    return "Parent path %s doesn't exist" % (parent)

            if self.__must_be_dir:
                if not os.path.exists(answer) or not os.path.isdir(answer):
                    return "Path is not a directoy"

            if self.__must_be_file:
                if not os.path.exists(answer) or not os.path.isfile(answer):
                    return "Path is not a file"

        return None