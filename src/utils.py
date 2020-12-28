import difflib
import os
import src.const as const


class Utils:
    file_dir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(file_dir)

    @staticmethod
    def annators_name(annotators_dir):
        list_annotators = []
        for sub_dir in os.listdir(annotators_dir):
            if not sub_dir.startswith('.'):
                list_annotators.append(sub_dir)

        return list_annotators

    @staticmethod
    def init_paths():

        input_dir = os.path.join(Utils.parentDir, "data", "input")
        output_dir = os.path.join(Utils.parentDir, "data", "output")

        return input_dir, output_dir

    @staticmethod
    def init_paths_neuroner(input_dir):
        if input_dir is None:
            input_dir = os.path.join(Utils.parentDir, "data", "output")
        output_dir = os.path.join(Utils.parentDir, "data", "output_neuroner")

        return input_dir, output_dir

    @staticmethod
    def convertor_to_sug(variable_list):
        sug_varilabe_list = []
        for var in variable_list:
            sug_varilabe_list.append("_SUG_" + var)
        return sug_varilabe_list

    @staticmethod
    def similarity_hemorragia_evidence(text):
        """
        :param line: input line
        :return:
            The most similarity defined section with the given line
        """

        list_similarities = difflib.get_close_matches(text, const.HEMORRAGIA_EVIDENCE, 1, 0.85)
        if len(list_similarities) > 0:
            return True
        else:
            return False

    @staticmethod
    def similarity_isquemico_evidence(text):
        """
        :param line: input line
        :return:
            The most similarity defined section with the given line
        """

        list_similarities = difflib.get_close_matches(text, const.ISQUEMICO_EVIDENCE, 1, 0.85)
        if len(list_similarities) > 0:
            return True
        else:
            return False
