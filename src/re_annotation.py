import argparse
from utils import Utils
from entities import Entities
from merge import Merge
from writer import Write


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="re_annotation")
    parser.add_argument('--bunch', help='Which set is going to compare')
    args = parser.parse_args()

    bunch = args.bunch

    input_dir, output_dir = Utils.init_paths()
    annotators = Utils.annators_name(input_dir)

    variable_dict, variable_hash_dict, section_dict= Entities.get_annotators_entities(bunch,
                                                                                    annotators,
                                                                                    input_dir,
                                                                                    t_number=False)

    merged_variables, owner_file = Merge.merge_entities(variable_dict)
    merged_variables = Entities.sorted_entities(merged_variables)

    merged_sections, _ = Merge.merge_entities(section_dict)
    merged_variables_hash = Merge.merge_hash(variable_hash_dict)

    ctakes_dir = input_dir.replace("input", "ctakes_output")
    ctakes_variables, ctakes_variables_hash, ctakes_sections = Entities.get_ctakes_entities(bunch,
                                                                                            ctakes_dir,
                                                                                            t_number=False)

    merged_variables, merged_variables_hash, merged_sections = Merge.merge_ctakes_annotators(merged_variables,
                                                                            merged_variables_hash,
                                                                            merged_sections,
                                                                            ctakes_variables,
                                                                            ctakes_variables_hash,
                                                                            ctakes_sections)


    merged_variables = Entities.sorted_entities(merged_variables)
    section_variable = Merge.merge_variables_sections(merged_variables, merged_sections)

    # section_variable = Merge.diagnostic_filterring(section_variable)
    section_variable = Merge.diagnostic_filterring_new(section_variable)

    Write.accepted_variables_reannote(owner_file, section_variable, merged_variables_hash, bunch, input_dir, output_dir)

    print("Done")












