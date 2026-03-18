#1
def analyze_text(text):
    vowels = set('aeiouy')
    unique_vowels = set()
    words = []
    current = ""
    
    for ch in text.lower():
        if ch.isalpha():
            current += ch
            if ch in vowels:
                unique_vowels.add(ch)
        else:
            if current:
                words.append(current)
                current = ""
    if current:
        words.append(current)

    result = []
    seen = set()

    for w in words:
        if len(w) >= 5 and w[0] == w[-1] and w not in seen:
            result.append(w)
            seen.add(w)

    return (len(unique_vowels), " ".join(result))
#2
f2 = lambda s: " ".join(
    list(
        map(lambda w: w[::-1],
            filter(lambda w: w.isalpha() and len(w[::-1]) % 2 == 0,
                   filter(lambda w: not any(c.isdigit() for c in w), s.split())
            )
        )
    )
)
#3
def top_k_words(text, k):
    clean = ""
    for ch in text.lower():
        clean += ch if ch.isalpha() or ch == " " else " "
    
    words = clean.split()
    freq = {}

    for w in words:
        freq[w] = freq.get(w, 0) + 1

    items = list(freq.items())
    items.sort(key=lambda x: (-x[1], x[0]))

    return [w for w, _ in items[:k]]
#4
f4 = lambda s: " ".join(
    map(lambda w: w.lower(),
        filter(lambda w: sum(1 for c in w if c.isupper()) == 1 
               and not w[0].isupper() 
               and not w[-1].isupper(),
               s.split()))
)
#5
def compress_text(text):
    if not text:
        return ""

    result = ""
    count = 1

    for i in range(1, len(text)):
        if text[i].lower() == text[i-1].lower():
            count += 1
        else:
            result += text[i-1] + (str(count) if count > 1 else "")
            count = 1

    result += text[-1] + (str(count) if count > 1 else "")
    return result
#6
f6 = lambda s: list(
    filter(lambda w: len(w) >= 4 and w.isalpha() and len(set(w)) == len(w),
           s.split())
)
#7
def palindrome_words(text):
    clean = ""
    for ch in text.lower():
        clean += ch if ch.isalpha() or ch == " " else " "
    
    words = clean.split()
    res = set()

    for w in words:
        if len(w) >= 3 and w == w[::-1]:
            res.add(w)

    return sorted(res, key=lambda x: (-len(x), x))
#8
f8 = lambda s: " ".join(
    map(lambda w: w if any(c.isdigit() for c in w)
        else ("VOWEL" if w[0].lower() in "aeiouy" else "CONSONANT"),
        s.split())
)
#9
def alternate_case_blocks(text, n):
    res = ""
    block_index = 0

    for i in range(0, len(text), n):
        block = text[i:i+n]
        if block_index % 2 == 0:
            res += block.upper()
        else:
            res += block.lower()
        block_index += 1

    return res.replace(" ", "")
#10
f10 = lambda s: sum(
    1 for w in s.split()
    if any(c.isdigit() for c in w)
    and not w[0].isdigit()
    and len(w) >= 5
)
#11
def common_unique_chars(s1, s2):
    seen = set()
    res = ""

    for ch in s1:
        if ch.isalpha() and ch not in seen and ch in s2:
            res += ch
            seen.add(ch)

    return res
#12
f12 = lambda s: list(
    filter(lambda w: len(w) > 3 and w[0] == w[-1] and w != w[::-1],
           s.split())
)
#13
def replace_every_nth(text, n, char):
    res = list(text)

    for i in range(len(text)):
        if (i + 1) % n == 0:
            if not text[i].isdigit() and text[i] != " ":
                # проверка длины слова
                left = i
                while left > 0 and text[left-1] != " ":
                    left -= 1
                right = i
                while right < len(text)-1 and text[right+1] != " ":
                    right += 1
                
                if right - left + 1 >= 3:
                    res[i] = char

    return "".join(res)
#14
f14 = lambda s: ",".join(
    filter(lambda w: len(set(w)) > 3 and len([c for c in w if c in "aeiouy"]) == len(set([c for c in w if c in "aeiouy"])),
           s.split())
)
#15
def word_pattern_sort(text):
    words = text.split()
    groups = {}

    for w in words:
        groups.setdefault(len(w), []).append(w)

    res = []
    for length in sorted(groups):
        group = groups[length]
        group.sort(key=lambda w: (-sum(1 for c in w.lower() if c in "aeiouy"), w))
        res.extend(group)

    return res
#16
def transform_list(nums):
    res = []

    for n in nums:
        if n < 0:
            continue
        elif n % 2 == 0:
            res.append(n * n)
        elif n > 10:
            res.append(sum(int(d) for d in str(n)))
        else:
            res.append(n)

    return res
#17
f17 = lambda lst: list(
    map(lambda x: x*x,
        filter(lambda x: (x % 3 == 0 or x % 5 == 0) and x % 15 != 0 and len(str(abs(x))) % 2 == 1,
               lst))
)
#18
def flatten_and_filter(lst):
    res = []

    def helper(x):
        for el in x:
            if isinstance(el, list):
                helper(el)
            else:
                if isinstance(el, int) and el > 0 and el % 4 != 0 and len(str(el)) > 1:
                    res.append(el)

    helper(lst)
    return sorted(res)
#19
f19 = lambda a, b: [x for x, y in zip(a, b) if x == y and x % 2 == 0]
#20
def max_subarray_sum(nums, k):
    max_sum = None

    for i in range(len(nums) - k + 1):
        window = nums[i:i+k]
        if any(x <= 0 for x in window):
            continue
        s = sum(window)
        if max_sum is None or s > max_sum:
            max_sum = s

    return max_sum
#21
f21 = lambda lst: list(
    map(str.upper,
        filter(lambda s: s.isalpha() and len(s) > 4 and len(set(s)) == len(s),
               lst))
)
#22
def group_by_parity_and_sort(nums):
    even = []
    odd = []

    for n in nums:
        if n % 2 == 0:
            even.append(n)
        else:
            odd.append(n)

    even.sort()
    odd.sort()

    return even + odd
#23
f23 = lambda lst: [x for i, x in enumerate(lst)
                  if i > 1 and all(i % d for d in range(2, i))
                  and x % 2 == 1
                  and x > sum(lst)/len(lst)]
#24
def longest_increasing_sublist(nums):
    best = []
    current = [nums[0]] if nums else []

    for i in range(1, len(nums)):
        if nums[i] > nums[i-1]:
            current.append(nums[i])
        else:
            if len(current) > len(best):
                best = current
            current = [nums[i]]

    if len(current) > len(best):
        best = current

    return best
#25
f25 = lambda lst: list(
    map(lambda x: sum(x)/len(x),
        filter(lambda x: len(x) >= 3 and sum(x) % 2 == 0, lst))
)
#26
def remove_duplicates_keep_last(nums):
    seen = set()
    res = []

    for i in range(len(nums)-1, -1, -1):
        if nums[i] not in seen:
            res.append(nums[i])
            seen.add(nums[i])

    return res[::-1]
#27
f27 = lambda lst: sorted(lst, key=lambda x: (-len(x), x))[:5]
#28
def moving_average(nums, k):
    res = []

    for i in range(len(nums) - k + 1):
        window = nums[i:i+k]
        if any(x < 0 for x in window):
            continue
        res.append(sum(window)/k)

    return res
#29
f29 = lambda a, b: [x for x in a if x not in b and x > sum(a)/len(a)]
#30
def analyze_strings_list(words):
    seen = set()
    res = []

    for w in words:
        if any(c.isdigit() for c in w):
            continue

        new_w = w[::-1] if len(w) % 2 == 0 else w.upper()

        if new_w not in seen:
            res.append(new_w)
            seen.add(new_w)

    return res
#31
f31 = lambda d: {
    k: v for k, v in d.items()
    if len(v) == len(set(v)) and all(len(s) > 3 for s in v)
}
#32
def pairwise_intersections(sets_list):
    res = []

    if len(sets_list) < 2:
        return res

    for i in range(len(sets_list) - 1):
        res.append(sets_list[i] & sets_list[i+1])

    return res
#33
f33 = lambda d: (
    lambda avg: {
        k: v for k, v in d.items()
        if sum(v)/len(v) > avg
    }
)(sum(sum(v) for v in d.values()) / sum(len(v) for v in d.values()))
#34
def top_k_smallest_unique(nums, k):
    unique = sorted(set(nums))
    return set(unique[:k])
#35
f35 = lambda d: {
    k: v for k, v in d.items()
    if v % 3 != 0 and len(k) % 2 != 0
}
#36
def all_subsets_of_size_k(s, k):
    res = []
    s = list(s)

    def backtrack(start, path):
        if len(path) == k:
            res.append(set(path))
            return
        for i in range(start, len(s)):
            backtrack(i+1, path + [s[i]])

    backtrack(0, [])
    return res
#37
import math

f37 = lambda d: {
    k: (math.factorial(v) if v < 6 else v)
    for k, v in d.items()
}
#38
def multi_symmetric_difference(sets_list):
    if not sets_list:
        return set()

    res = sets_list[0]
    for s in sets_list[1:]:
        res = res ^ s

    return res
#39
f39 = lambda d: sorted(
    d.keys(),
    key=lambda k: (sum(1 for c in k.lower() if c in "aeiouy"), -d[k])
)
#  40
def analyze_dict_keys(d):
    res = set()

    for k in d:
        if isinstance(k, str) and not any(c.isdigit() for c in k):
            for ch in k:
                if ch.isalpha():
                    res.add(ch)

    return res