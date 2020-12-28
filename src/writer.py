import os
from shutil import copyfile, move
import src.const as const


class Write:

    @staticmethod
    def accepted_variables_reannote(owner_file, section_variables, variables_hash, bunch, input_dir, output_dir):

        print("Saving accepted varibales and section in the final ann.")
        annotators = ['victoria', 'eugenia', 'isabel']
        number_files = len(section_variables)//2
        for annotator in annotators:
            for file_number, (file, section_variable) in enumerate(section_variables.items()):
                T = 1
                # if annotator == "carmen" and file_number > number_files:
                #     annotator = "isabel"

                if file == "sonespases_869603840.ann":
                    print("checl")


                os.makedirs(os.path.join(output_dir, bunch, annotator), exist_ok=True)
                output_path = os.path.join(output_dir, bunch, annotator, file).replace(".ann", ".txt")
                input_path = os.path.join(input_dir, owner_file[file], bunch, file).replace(".ann", ".txt")

                final_brat_f = open(os.path.join(output_dir, bunch, annotator, file), "w", encoding="UTF-8")
                copyfile(input_path, output_path)

                isabel_carmen_evidence = 0

                for section, variables in section_variable.items():
                    for var in variables:
                        if (var['label'].startswith("SECCION_") or
                                (annotator == 'eugenia' and (var['label'].split("_SUG_")[-1] in const.EUGENIA or
                                                         var['label'] in const.FECHA_HORA_TIEMO)) or
                                (annotator == 'victoria' and (var['label'].split("_SUG_")[-1] in const.VICTORIA)) or
                                ((annotator == 'carmen' or annotator == 'isabel') and
                                 (var['label'].split("_SUG_")[-1] in const.CARMEN_ISABEL or
                                  var['label'] in const.FECHA_HORA_TIEMO))):

                            if var["T"].startswith("T"):
                                tuple = (var['text'], var['start'], var['end'], var['label'])
                                final_brat_f.write('T' + str(T) +
                                                   "\t" + var['label'] + " " + str(var['start']) + " " + str(var['end']) +
                                                   "\t" + var['text'] + "\n")
                                if tuple in variables_hash[file].keys():
                                    final_brat_f.write('#' + str(T) + "\t" + "AnnotatorNotes T" + str(T) + "\t" +variables_hash[file][tuple].strip() + "\n")
                            else:
                                final_brat_f.write('T' + str(T) +
                                                   "\t" + var['label'] + " " + str(var['start']) + " " + str(var['end']) +
                                                   "\t" + var['text'] + "\n")
                            T += 1
                        else:
                            check = var
                        if var['label'] in const.EVIDENCE_CARMEN_ISABLE:
                            isabel_carmen_evidence += 1
                if annotator == "isabel" and isabel_carmen_evidence == 0:
                    os.makedirs(os.path.join(output_dir, bunch, "carmen"), exist_ok=True)
                    move(output_path, output_path.replace(annotator, "carmen"))
                    move(output_path.replace(".txt", ".ann"), output_path.replace(annotator, "carmen").replace(".txt", ".ann"))

                # if ((annotator == 'carmen' or annotator == 'isabel') and isabel_carmen_evidence == 0):
                #     os.remove(os.path.join(output_dir, bunch, annotator, file))
                #     os.remove(output_path)
                #     print("https://temu.bsc.es/ICTUSnet/index.xhtml#/.reannotate/" + bunch + "/" + annotator + "/"+ file.replace(".ann", ""))

                dissagreement = ["sonespases_869603840.ann",
"324973414.utf8.ann",
"448682704.utf8.ann",
"453878553.utf8.ann",
"453976646.utf8.ann",
"453847658.utf8.ann",
"422835700.utf8.ann",
"454769765.utf8.ann",
"424852481.utf8.ann",
"422449708.utf8.ann",
"430595323.utf8.ann",
"430038234.utf8.ann"]
                if ((annotator == 'carmen' or annotator == 'isabel') and file in dissagreement):
                    print(
                        "https://temu.bsc.es/ICTUSnet/index.xhtml#/.reannotate/" + bunch + "/" + annotator + "/" + file.replace(
                            ".ann", ""))




    @staticmethod
    def accepted_variables_neuroner(section_variable, variables_hash, output_dir):

        print("Saving accepted varibales and section in the final ann.")
        number_files = len(section_variable)//2
        for file_number, (file, section_varibale) in enumerate(section_variable.items()):
            T = 1
            final_brat_f = open(os.path.join(output_dir, file), "w", encoding="UTF-8")

            for section, variables in section_varibale.items():
                for var in variables:
                    if var["T"].startswith("T"):
                        tuple = (var['text'], var['start'], var['end'], var['label'])
                        final_brat_f.write('T' + str(T) +
                                           "\t" + var['label'] + " " + str(var['start']) + " " + str(var['end']) +
                                           "\t" + var['text'] + "\n")
                        if tuple in variables_hash[file].keys():
                            final_brat_f.write('#' + str(T) + "\t" + "AnnotatorNotes T" + str(T) + "\t" +variables_hash[file][tuple] + "\n")
                    else:
                        final_brat_f.write('T' + str(T) +
                                           "\t" + var['label'] + " " + str(var['start']) + " " + str(var['end']) +
                                           "\t" + var['text'] + "\n")
                    T += 1

    @staticmethod
    def copy_input_text_neuroner(input_path, output_path):
        copyfile(input_path, output_path)
