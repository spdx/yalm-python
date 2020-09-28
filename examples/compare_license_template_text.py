#!/usr/bin/env python

# Parses License Text and Template Strings passed into them and compare them 

if __name__ == '__main__':
    from normalize_license_text.normalize_class import NormalizeText
    from compare_template_text.compare_normalized_files import CompareNormalizedFiles
    from compare_template_text.normalize_template_text import NormalizeTemplate
    from generate_differences.differences import Generate_Differences

    a = "Any Sample Template passed into Module"
    b = "Any Sample Text passed into Module"
    
    object_a = NormalizeText(a)
    stringtemplate = object_a.returnfinalstring_for_template()
    object_b = NormalizeText(b)
    stringtext = object_b.returnfinalstring_for_template()
    
    test = NormalizeTemplate(stringtext, stringtemplate)
    test.normalize_template()
    normalized_text = test.return_normalized_text()
    normalized_template = test.return_normalized_template()
    if(CompareNormalizedFiles(normalized_template,normalized_text)):
        print("The License Text" +b+ " matches with the Template "+a)
    else:
        nl = "\n"
        print(f"The Text and the Template do not Match.{nl}"
              )
        compare_object = Generate_Differences(
            normalized_template, normalized_text)

        differences = compare_object.pretty_print_differences()
        print(differences)        
