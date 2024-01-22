from Key_word import Key_word
class determine:
    def calculate_score(input_string):
        print(input_string)
        keyword_list = [Key_word.MPRS_keyword,Key_word.WCPS_keyword,Key_word.TSDS_keyword]
        result = []
        for keyword in keyword_list:
            score = 0
            for keyword, value in keyword.items():
                if keyword in input_string:
                    score += value
            result.append(score)

        #set_return_dict
        return max(result), result.index(max(result))

    def determine_frequency(input_string):
        frequency_map = {'50hz': '50hz', '200hz': '200hz', '400hz': '400hz', '800hz': '800hz'}
        for freq in frequency_map:
            if freq in input_string:
                return frequency_map[freq]
        return '50hz'

    def determine_material(input_string):
        material_map = {'FeSiCr': 0, 'NeFi': 1}
        for material in material_map:
            if material in input_string:
                return material_map[material]
        return 0
    
    def determine_workpiece(input_string):
        material_map = {'圓環': 0, '狗骨頭': 1}
        for material in material_map:
            if material in input_string:
                return material_map[material]
        return 0
    
    def determine_ratio(input_string):
        material_map = {'低鐵損': 0, '高最大拉伸': 1,'高拉伸強度': 1,'客製化': 2}
        for material in material_map:
            if material in input_string:
                return material_map[material]
        return 0
