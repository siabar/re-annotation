import argparse
from utils import Utils
from entities import Entities
from merge import Merge
from writer import Write


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="prepare_for_neuronet")
    parser.add_argument('--input', help='Input directory of bunches (annotation files)')
    args = parser.parse_args()

    input_dir = args.input

    input_dir, output_dir = Utils.init_paths_neuroner(input_dir)
    annotators = ['eugenia', 'victoria', 'isabel', 'carmen']

    variable_dict, variable_hash_dict, section_dict = Entities.get_final_annotators_entities(
                                                                                    input_dir,
                                                                                    output_dir,
                                                                                    t_number=False)

    merged_variables, _ = Merge.merge_entities(variable_dict)
    merged_sections, _ = Merge.merge_entities(section_dict)
    merged_variables_hash = Merge.merge_hash(variable_hash_dict)

    section_variable = Merge.merge_variables_sections(merged_variables, merged_sections)

    Write.accepted_variables_neuroner(section_variable, merged_variables_hash, output_dir)

    print("Done")












