# Parses Two License Text Strings passed into them

if __name__ == '__main__':
    from normalize_license_text.normalize_class import NormalizeText
    from compare_template_text.compare_normalized_files import compare_normalized_files
    from compare_template_text.normalize_template_text import NormalizeTemplate
    from generate_differences.differences import DifferenceGenerator

    a = "Any Sample Text passed into Module"
    b = "Any Sample Text passed into Module"

    object_a = NormalizeText(a)
    stringtemplate = object_a.get_final_string()
    object_b = NormalizeText(b)
    stringtext = object_b.get_final_string()

    if (stringtemplate == stringtext):
        print("The License Text \" " + b + "\" matches with the Text \"" + a + " \" ")
    else:
        nl = "\n"
        print(f"The Texts do not Match.{nl}")
        compare_object = DifferenceGenerator(stringtemplate, stringtext)

        differences = compare_object.pretty_print_differences()
        print(differences)
