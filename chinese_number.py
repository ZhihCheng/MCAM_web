def extract_and_convert_numbers(s):
    """
    Extracts numbers from a string, handling both Chinese and Arabic numerals, and converts them to an integer.
    """
    cn_num = {'零': 0, '一': 1, '二': 2, '兩': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    unit = {'十': 10, '百': 100, '千': 1000, '萬': 10000, '億': 100000000}
    total = 0
    num = 0
    r = 0
    arabic_number_part = ""  
    for i in range(len(s)):
        if s[i] in cn_num:
            if arabic_number_part:  
                total += int(arabic_number_part)
                arabic_number_part = "" 
            num = cn_num[s[i]]
            if i == len(s) - 1 or s[i+1] not in unit:
                total += num
            r = 1  
        elif s[i] in unit:
            r = unit[s[i]]
            if num == 0: 
                num = 1
            total += num * r
            num = 0  
        elif s[i].isdigit():  
            arabic_number_part += s[i]
        else:  
            if arabic_number_part:
                total += int(arabic_number_part)
                arabic_number_part = ""
            num = 0
            r = 1
    if arabic_number_part:
        total += int(arabic_number_part)
    return total

# # Test the function with both examples
# example_str1 = "我需要最大瞬間扭矩為六萬三千的馬達曲線"
# example_str2 = "我需要最大瞬間扭矩為63000的馬達曲線"

# extracted_number1 = extract_and_convert_numbers(example_str1)
# extracted_number2 = extract_and_convert_numbers(example_str2)


# print(extracted_number1, extracted_number2)

