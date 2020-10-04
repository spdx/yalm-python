
# Parses Two License Text Strings passed into them 

if __name__ == '__main__':
    from normalize_license_text.normalize_class import NormalizeText
    from compare_template_text.compare_normalized_files import CompareNormalizedFiles
    from compare_template_text.normalize_template_text import NormalizeTemplate
    from generate_differences.differences import Generate_Differences

    a = "Any Sample Text passed into Module"
    b = "Any Sample Text passed into Module"
    
    object_a = NormalizeText(a)
    stringtemplate = object_a.returnfinalstring()
    object_b = NormalizeText(b)
    stringtext = object_b.returnfinalstring()
    
    if(stringtemplate==stringtext):
        print("The License Text \" " +b+ "\" matches with the Text \""+a+" \" ")
    else:
        nl = "\n"
        print(f"The Texts do not Match.{nl}"
              )
        compare_object = Generate_Differences(
            stringtemplate, stringtext)

        differences = compare_object.pretty_print_differences()
        print(differences)
