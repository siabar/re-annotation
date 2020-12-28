import os
import string
from src.writer import Write
import src.const as const


class Entities:

    removed_punc_counter = dict()
    removed_punc = dict()

    @staticmethod
    def update_punc(punc, annotator, who):
        if who == "annotators" and punc not in Entities.removed_punc:
            if annotator not in Entities.removed_punc.keys():
                Entities.removed_punc[annotator] = [punc]
            else:
                temp = Entities.removed_punc.get(annotator)
                if punc not in temp:
                    temp.append(punc)
                    Entities.removed_punc.update({annotator: temp})

    @staticmethod

    def span_fixer(text, start_span, end_span, label, who, annotator):
        original_text = text
        if not (label.startswith("NIHSS") or label.startswith("mRankin") or label.startswith("ASPECTS") or len(text) != 0):
            punctuation = string.punctuation.replace(".", "")

            before_rstrip = len(text)
            text = text.rstrip()
            after_rstrip = len(text)
            end_span -= before_rstrip - after_rstrip
            while text[len(text) - 1] in punctuation:
                Entities.update_punc(text[len(text) - 1], annotator, who)

                text = text[:-1]
                removed_space = len(text) - len(text.rstrip())
                text = text.rstrip()
                end_span -= 1 + removed_space
            before_lstrip = len(text)
            text = text.lstrip()
            after_lstrip = len(text)
            start_span += before_lstrip - after_lstrip
            while text[0] in string.punctuation:
                Entities.update_punc(text[0], annotator, who)

                text = text[1:]
                removed_space = len(text) - len(text.lstrip())
                text = text.lstrip()
                start_span += 1 + removed_space

        if who == "annotators" and original_text != text:
            if annotator not in Entities.removed_punc_counter.keys():
                Entities.removed_punc_counter[annotator] = 1
            else:
                temp = Entities.removed_punc_counter.get(annotator)
                Entities.removed_punc_counter.update({annotator: temp + 1})

        return text, start_span, end_span

    @staticmethod
    def sorted_entities(merged_variables):

        for file, entites in merged_variables.items():
            if file == "430595323.utf8.ann":
                print("checl")
            vars_ordered = sorted(entites, key=lambda entity: entity['start'])
            merged_variables.update({file: vars_ordered})
        return merged_variables

    @staticmethod
    def get_annotators_entities(bunch, list_annotators, input_dir, t_number=False):
        bunch_prefix = bunch.split("_")[0]

        variable_dict = dict()
        variable_hash_dict = dict()
        section_dict = dict()



        for dir in list_annotators:
            annotators_variable = {}
            annotators_variable_hash = {}
            annotators_sections = {}

            # entities_dir = os.path.join(input_dir, dir, bunch)
            # for annotators_files in os.listdir(entities_dir):

            for annotators_files in os.listdir(os.path.join(input_dir, dir, bunch)):
                if annotators_files == "430595323.utf8.ann":
                    print("checl")
                if annotators_files.endswith(".ann"):
                    with open(os.path.join(input_dir, dir, bunch_prefix, annotators_files), "r") as r:
                        entites = []
                        entity_tuple = ()
                        entities_row = dict()
                        hash_entities = dict()
                        sections = []
                        pre_header = ""
                        for line in r:
                            temp_line = line.split("\t", 2)
                            if line.startswith("T") and not \
                                    (temp_line[1].startswith("HORA") or
                                     temp_line[1].startswith("FECHA") or
                                     temp_line[1].startswith("_SUG_") or
                                     temp_line[1].startswith("TIEMPO")):

                                checking_text = temp_line[-1].replace("\n", "")
                                checking_start = int(temp_line[1].split()[1])
                                checking_end = int(temp_line[1].split()[2])
                                checking_label = temp_line[1].split()[0]

                                if checking_text.startswith("rtpa"):
                                    check = 0
                                if bunch.startswith("04") or bunch.startswith("03") or bunch.startswith(
                                        "02") or bunch.startswith("01"):
                                    # For bunch 1,2,3 we revised manual annotations for variables and sections that
                                    # ended with a punctuations except of dot (.) and started with a punctuations
                                    # we fixed the span and saved it in a correct file (03, 02)...
                                    # for having a correct evaluation our pipeline tools with the manual, we should
                                    # apply the same for output of pipeline
                                    checking_text, checking_start, checking_end = \
                                        Entities.span_fixer(checking_text, checking_start, checking_end, checking_label,
                                                        "ctakes", dir)

                                    if bunch.startswith("03") and temp_line[-1].replace("\n", "") != checking_text:
                                        print("ERROR!!!!!!")

                                # entity['row'] = temp_line[0]
                                # entity['text'] = checking_text
                                # entity['start'] = checking_start
                                # entity['end'] = checking_end
                                # entity['label'] = checking_label

                                if checking_label.startswith("SECCION_"):
                                    if checking_label != pre_header:
                                        if t_number:
                                            section = {'row': temp_line[0], 'text': checking_text,
                                                      'start': checking_start,
                                                      'end': checking_end, 'label': checking_label}
                                        else:
                                            section = {'text': checking_text,
                                                       'start': checking_start,
                                                       'end': checking_end, 'label': checking_label}


                                        sections.append(section)
                                    # else:
                                    #     print("X")
                                    pre_header = checking_label



                                else:
                                    if t_number:
                                        entity = {'row': temp_line[0], 'text': checking_text,
                                              'start': checking_start,
                                              'end': checking_end, 'label': checking_label}
                                    else:
                                        entity = {'text': checking_text,
                                                  'start': checking_start,
                                                  'end': checking_end, 'label': checking_label}

                                        entity_tuple = (checking_text,checking_start, checking_end, checking_label)


                                    entites.append(entity)

                                    if not t_number:
                                        entities_row[temp_line[0]] = entity_tuple

                            elif line.startswith("#"):

                                if t_number:
                                    hash_entities[temp_line[0]] = temp_line[1] + "\t" + temp_line[2]
                                else:
                                    hash_entities[temp_line[1].split(" ")[-1]] = temp_line[2]


                        vars_ordered = sorted(entites, key=lambda entity: entity['start'])
                        secs_ordered = sorted(sections, key=lambda entity: entity['start'])

                        annotators_variable[annotators_files] = vars_ordered


                        final_hash_entities = dict()
                        for hash, notes in hash_entities.items():
                            if t_number:
                                final_hash_entities[hash] = notes
                            elif entities_row.get(hash) is not None:
                                final_hash_entities[entities_row[hash]] = notes
                        annotators_variable_hash[annotators_files] = final_hash_entities

                        annotators_sections[annotators_files] = secs_ordered

            variable_dict[dir] = annotators_variable
            variable_hash_dict[dir] = annotators_variable_hash

            section_dict[dir] = annotators_sections

        return variable_dict, variable_hash_dict, section_dict


    @staticmethod
    def get_ctakes_entities(bunch, input_dir, t_number=False):
        bunch_prefix = bunch.split("_")[0]

        annotators_variable = {}
        annotators_variable_hash = {}
        annotators_sections = {}

        # entities_dir = os.path.join(input_dir, dir, bunch)
        # for annotators_files in os.listdir(entities_dir):

        for annotators_files in os.listdir(os.path.join(input_dir, bunch)):
            if annotators_files.endswith(".ann"):
                with open(os.path.join(input_dir, bunch_prefix, annotators_files), "r") as r:
                    entites = []
                    entity_tuple = ()
                    entities_row = dict()
                    hash_entities = dict()
                    sections = []
                    pre_header = ""
                    for line in r:
                        temp_line = line.strip().split("\t", 2)
                        if line.startswith("T") and \
                                (temp_line[1].startswith("_SUG_") or temp_line[1].startswith("SECCION")):

                            checking_text = temp_line[-1].replace("\n", "")
                            checking_start = int(temp_line[1].split()[1])
                            checking_end = int(temp_line[1].split()[2])
                            checking_label = temp_line[1].split()[0]
                            if bunch.startswith("04") or bunch.startswith("03") or bunch.startswith(
                                    "02") or bunch.startswith("01"):
                                # For bunch 1,2,3 we revised manual annotations for variables and sections that
                                # ended with a punctuations except of dot (.) and started with a punctuations
                                # we fixed the span and saved it in a correct file (03, 02)...
                                # for having a correct evaluation our pipeline tools with the manual, we should
                                # apply the same for output of pipeline
                                checking_text, checking_start, checking_end = \
                                    Entities.span_fixer(checking_text, checking_start, checking_end, checking_label,
                                                    "ctakes", dir)

                                if bunch.startswith("03") and temp_line[-1].replace("\n", "") != checking_text:
                                    print("ERROR!!!!!!")

                            # entity['row'] = temp_line[0]
                            # entity['text'] = checking_text
                            # entity['start'] = checking_start
                            # entity['end'] = checking_end
                            # entity['label'] = checking_label

                            if checking_label.startswith("SECCION_"):
                                if checking_label != pre_header:
                                    if t_number:
                                        section = {'row': temp_line[0], 'text': checking_text,
                                                  'start': checking_start,
                                                  'end': checking_end, 'label': checking_label}
                                    else:
                                        section = {'text': checking_text,
                                                   'start': checking_start,
                                                   'end': checking_end, 'label': checking_label}


                                    sections.append(section)
                                # else:
                                #     print("X")
                                pre_header = checking_label
                            else:
                                if t_number:
                                    entity = {'row': temp_line[0], 'text': checking_text,
                                          'start': checking_start,
                                          'end': checking_end, 'label': checking_label}
                                else:
                                    entity = {'text': checking_text,
                                              'start': checking_start,
                                              'end': checking_end, 'label': checking_label}

                                    entity_tuple = (checking_text,checking_start, checking_end, checking_label)


                                entites.append(entity)

                                if not t_number:
                                    entities_row[temp_line[0]] = entity_tuple

                        elif line.startswith("#"):

                            if t_number:
                                hash_entities[temp_line[0]] = temp_line[1] + "\t" + temp_line[2]
                            else:
                                hash_entities[temp_line[1].split(" ")[-1]] = temp_line[2]


                    vars_ordered = sorted(entites, key=lambda entity: entity['start'])
                    secs_ordered = sorted(sections, key=lambda entity: entity['start'])

                    annotators_variable[annotators_files] = vars_ordered


                    final_hash_entities = dict()
                    for hash, notes in hash_entities.items():
                        if t_number:
                            final_hash_entities[hash] = notes
                        elif entities_row.get(hash) is not None:
                            final_hash_entities[entities_row[hash]] = notes
                    annotators_variable_hash[annotators_files] = final_hash_entities

                    annotators_sections[annotators_files] = secs_ordered

        return annotators_variable, annotators_variable_hash, annotators_sections

    @staticmethod
    def get_final_annotators_entities(input_dir, output_dir, t_number=False):

        variable_dict = dict()
        variable_hash_dict = dict()
        section_dict = dict()

        for bunch in os.listdir(input_dir):

            # entities_dir = os.path.join(input_dir, dir, bunch)
            # for annotators_files in os.listdir(entities_dir):
            if not os.path.isdir(os.path.join(input_dir, bunch)):
                continue
            for dir in os.listdir(os.path.join(input_dir, bunch)):
                annotators_variable = {}
                annotators_variable_hash = {}
                annotators_sections = {}
                if not os.path.isdir(os.path.join(input_dir, bunch, dir)):
                    continue
                for annotators_files in os.listdir(os.path.join(input_dir, bunch, dir)):
                    if annotators_files.endswith(".ann"):
                        if dir in variable_dict.keys() and annotators_files in variable_dict.get(dir).keys():
                            print("Douplicated file", bunch, dir, annotators_files)
                        with open(os.path.join(input_dir, bunch, dir, annotators_files), "r") as r:
                            entites = []
                            entity_tuple = ()
                            entities_row = dict()
                            hash_entities = dict()
                            sections = []
                            pre_header = ""
                            for line in r:
                                temp_line = line.strip().split("\t", 2)

                                if line.startswith("T") and not \
                                        (temp_line[1].startswith("HORA") or
                                         temp_line[1].startswith("FECHA") or
                                         temp_line[1].startswith("_SUG_") or
                                         temp_line[1].startswith("TIEMPO")):

                                    checking_text = temp_line[-1].replace("\n", "")
                                    checking_start = int(temp_line[1].split()[1])
                                    checking_end = int(temp_line[1].split()[2])
                                    checking_label = temp_line[1].split()[0]
                                    if bunch.startswith("04") or bunch.startswith("03") or bunch.startswith(
                                            "02") or bunch.startswith("01"):
                                        # For bunch 1,2,3 we revised manual annotations for variables and sections that
                                        # ended with a punctuations except of dot (.) and started with a punctuations
                                        # we fixed the span and saved it in a correct file (03, 02)...
                                        # for having a correct evaluation our pipeline tools with the manual, we should
                                        # apply the same for output of pipeline
                                        checking_text, checking_start, checking_end = \
                                            Entities.span_fixer(checking_text, checking_start, checking_end, checking_label,
                                                            "ctakes", dir)

                                        if bunch.startswith("03") and temp_line[-1].replace("\n", "") != checking_text:
                                            print("ERROR!!!!!!")

                                    # entity['row'] = temp_line[0]
                                    # entity['text'] = checking_text
                                    # entity['start'] = checking_start
                                    # entity['end'] = checking_end
                                    # entity['label'] = checking_label

                                    if (checking_label.startswith("SECCION_") or
                                            (dir == 'eugenia' and (checking_label.split("_SUG_")[-1] in const.EUGENIA or
                                                               checking_label in const.FECHA_HORA_TIEMO)) or
                                            (dir == 'victoria' and (
                                                    checking_label.split("_SUG_")[-1] in const.VICTORIA)) or
                                            ((dir == 'carmen' or dir == 'isabel') and
                                             (checking_label.split("_SUG_")[-1] in const.CARMEN_ISABEL or
                                              checking_label in const.FECHA_HORA_TIEMO))):

                                        if checking_label.startswith("SECCION_"):
                                            if checking_label != pre_header:
                                                if t_number:
                                                    section = {'row': temp_line[0], 'text': checking_text,
                                                               'start': checking_start,
                                                               'end': checking_end, 'label': checking_label}
                                                else:
                                                    section = {'text': checking_text,
                                                               'start': checking_start,
                                                               'end': checking_end, 'label': checking_label}


                                                sections.append(section)
                                            # else:
                                            #     print("X")
                                            pre_header = checking_label

                                        else:
                                            if t_number:
                                                entity = {'row': temp_line[0], 'text': checking_text,
                                                      'start': checking_start,
                                                      'end': checking_end, 'label': checking_label}
                                            else:
                                                entity = {'text': checking_text,
                                                          'start': checking_start,
                                                          'end': checking_end, 'label': checking_label}

                                                entity_tuple = (checking_text,checking_start, checking_end, checking_label)


                                            entites.append(entity)

                                            if not t_number:
                                                entities_row[temp_line[0]] = entity_tuple

                                elif line.startswith("#"):

                                    if t_number:
                                        hash_entities[temp_line[0]] = temp_line[1] + "\t" + temp_line[2]
                                    else:
                                        hash_entities[temp_line[1].split(" ")[-1]] = temp_line[2]


                            vars_ordered = sorted(entites, key=lambda entity: entity['start'])
                            secs_ordered = sorted(sections, key=lambda entity: entity['start'])

                            annotators_variable[annotators_files] = vars_ordered


                            final_hash_entities = dict()
                            for hash, notes in hash_entities.items():
                                if t_number:
                                    final_hash_entities[hash] = notes
                                elif entities_row.get(hash) is not None:
                                    final_hash_entities[entities_row[hash]] = notes
                            annotators_variable_hash[annotators_files] = final_hash_entities

                            annotators_sections[annotators_files] = secs_ordered
                    elif annotators_files.endswith(".txt"):
                        Write.copy_input_text_neuroner(os.path.join(input_dir, bunch, dir, annotators_files),
                                                       os.path.join(output_dir, annotators_files))


                # variable_dict[dir] = annotators_variable
                variable_dict = Entities.update_dic(dir, variable_dict, annotators_variable)
                variable_hash_dict = Entities.update_dic(dir, variable_hash_dict, annotators_variable_hash)
                section_dict = Entities.update_dic(dir, section_dict, annotators_sections)

                # variable_hash_dict[dir] = annotators_variable_hash
                # section_dict[dir] = annotators_sections

        return variable_dict, variable_hash_dict, section_dict


    @staticmethod
    def update_dic(dir, dict, value):
        if dir not in dict.keys():
            dict[dir] = value
        else:
            dict[dir].update(value)
        return dict

