
from collections import deque

number_to_word = {
    0: 'ноль',
    1: 'один',
    2: 'два',
    3: 'три',
    4: 'четыре',
    5: 'пять',
    6: 'шесть',
    7: 'семь',
    8: 'восемь',
    9: 'девять',
    10: 'десять',
    11: 'одиннадцать',
    12: 'двенадцать',
    13: 'тринадцать',
    14: 'четырнадцать',
    15: 'пятнадцать',
    16: 'шестнадцать',
    17: 'семнадцать',
    18: 'восемнадцать',
    19: 'девятнадцать',
    20: 'двадцать',
    30: 'тридцать',
    40: 'сорок',
    50: 'пятьдесят',
    60: 'шестьдесят',
    70: 'семьдесят',
    80: 'восемьдесят',
    90: 'девяносто',
    100: 'сто',
    200: 'двести',
    300: 'триста',
    400: 'четыреста',
    500: 'пятьсот',
    600: 'шестьсот',
    700: 'семьсот',
    800: 'восемьсот',
    900: 'девятьсот'
}

word_to_number = {value: key for key, value in number_to_word.items()}

operations_dict = {
    'плюс': '+',
    'минус': '-',
    'умножить на': '*',
    'разделить на': '/',
    'скобка открывается': '(',
    'скобка закрывается': ')'
}



def find_and_replace_operations(text):
    replaced_text = text
    for operation in operations_dict.keys():
        if operation in replaced_text:
            replaced_text = replaced_text.replace(operation, operations_dict[
                operation])
    return replaced_text



def separate_number(num):
    if num == 0:
        return [0]
    num_parts = []
    if num % 1000 != num:
        num_parts.append(num - num % 1000)
        num = num % 1000

    if num % 100 != num:
        num_parts.append(num - num % 100)
        num = num % 100

    if num % 10 != num and num > 20:
        num_parts.append(num - num % 10)
        num = num % 10
    if num != 0:
        num_parts.append(num)
    return num_parts



def translate_number_to_words(num):
    words = []
    if num < 0:
        words.append("минус")
        num *= -1
    for num_part in separate_number(num):
        if num_part >= 1000:
            thousands_parts = separate_number(
                int(num_part / 1000))
            for t_part in thousands_parts:
                if t_part != thousands_parts[-1]:
                    words.append(number_to_word[t_part])
                else:
                    if t_part == 1:
                        words.append("одна тысяча")
                    elif t_part == 2:
                        words.append("две тысячи")
                    elif 3 <= thousands_parts[-1] <= 4:
                        words.append(number_to_word[t_part] + " тысячи")
                    elif 5 <= thousands_parts[-1] <= 999:
                        words.append(number_to_word[t_part] + " тысяч")
                    else:
                        return 'больше девятьсот тысяч девятьсот девяносто девять'
        else:
            words.append(number_to_word[num_part])
    return ' '.join(words)


def is_operation(symbol):
    return symbol in operations_dict.values()


def is_text_number(word):
    return word in number_to_word.values()

def is_number(word):
    try:
        int(word)
        return True
    except:
        return False


def parse(text):
    text = find_and_replace_operations(text)
    elements_list = text.split()
    for index in range(len(elements_list)):
        if len(elements_list) > index and is_text_number(elements_list[index]):
            elements_list[index] = word_to_number[elements_list[index]]

    while True:
        src_elements_list = elements_list.copy()
        for index in range(len(elements_list)):
            if len(elements_list) > index + 1 and is_number(elements_list[index]) and is_number(
                    elements_list[index + 1]):
                elements_list[index] += elements_list[index + 1]
                del elements_list[index + 1]
            if len(elements_list) > index + 1 \
                    and elements_list[index] == "-" \
                    and (index == 0 or is_operation(elements_list[index - 1])) and is_number(elements_list[index + 1]):
                elements_list[index + 1] = elements_list[index + 1] * -1
                del elements_list[index]
        if elements_list == src_elements_list:
            break
    return elements_list

def convert_to_reverse_polish_notation(math_expression):
    operations_priority = {
        '*': 3,
        '/': 3,
        '+': 2,
        '-': 2,
        '(': 1
    }

    operations_stack = deque()
    rpn_expression = []
    for token in math_expression:
        if is_number(token):
            rpn_expression.append(token)
        elif token == "(":
            operations_stack.append(token)
        elif token == ")":
            operation = operations_stack.pop()
            while operation != "(":
                rpn_expression.append(operation)
                operation = operations_stack.pop()
        elif is_operation(token):
            while len(operations_stack) > 0 and operations_priority[operations_stack[-1]] >= operations_priority[token]:
                rpn_expression.append(operations_stack.pop())
            operations_stack.append(token)
    while len(operations_stack) > 0:
        rpn_expression.append(operations_stack.pop())
    return rpn_expression


def evaluate_reverse_polish_notation(rpn_expression):
    numbers_stack = []
    for token in rpn_expression:
        if is_number(token):
            numbers_stack.append(token)
        elif is_operation(token):
            second_num = numbers_stack.pop()
            first_num = numbers_stack.pop()
            tmp_res = eval(str(first_num) + token + str(second_num))
            numbers_stack.append(tmp_res)
    return numbers_stack.pop()


def validate_paranthesis(text):
    open_parenthesis_count = text.count('скобка открывается')
    close_parenthesis_count = text.count('скобка закрывается')
    if open_parenthesis_count != close_parenthesis_count:
        return False, 'Количество открывающихся скобок: ' + str(
            open_parenthesis_count) + ', а количество закрывающихся: ' + str(close_parenthesis_count)
    return True, ''


def calc(text):
    text = text.lower()
    is_ok, err = validate_paranthesis(text)
    if not is_ok:
        return 'Ошибка! ' + err
    math_expression_list = parse(text)
    rpn_expression_list = convert_to_reverse_polish_notation(math_expression_list)
    result_num = int(evaluate_reverse_polish_notation(rpn_expression_list))
    return translate_number_to_words(result_num)

# test_text = "скобка открывается сто плюс девяносто скобка закрывается умножить на три"
# test_text2 = "шестьсот шестьдесят три умножить на шестьсот шестьдесят три"
# test_text3 = "сто умножить на минус пять"
# test_text4 = "минус минус семь минус минус два"
# test_text5 = "шесть разделить на шесть"
# test_text6 = "скобка открывается сто тридцать плюс три скобка закрывается умножить на семь минус минус восемь"
# test_text7 = "скобка открывается скобка открывается девять плюс три скобка закрывается умножить на скобка открывается " \
#              "шесть плюс семь скобка закрывается скобка закрывается"
#
# tests = [test_text, test_text2, test_text3, test_text4, test_text5, test_text6, test_text7]
#
# for i in tests:
#     print(f"Ввод: {i}, Вывод: {calc(i)}")

print("Это текстовый калькулятор. "
          "Введите, пожалуйста, математическое выражение в тексте:")
while True:
    input_string = input()
    print("Результат: ", calc(input_string))
