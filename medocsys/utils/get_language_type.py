def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

# print(is_contains_chinese("hello"))
# print(is_contains_chinese("hello你好"))
# print(is_contains_chinese("123456"))
# print(is_contains_chinese("你好"))
