#task 1
#def analyze_text(text):
#    vowels = 'aeiouAEIOU'
#    found_vowels = set()
#    results_words = []
#    for word in text.lower().split():  #(text.lower().split(): делает текст строчным и разбивает его на слова)
#        word = word.strip('.,!?";()')  #(word.strip('.,!?";()')) удаляет указанные символы из начала и конца слова
#        for char in word:
#            if char in vowels:
#                found_vowels.add(char) #(found_vowels.add(char) добавляет найденные гласные в множество, чтобы избежать повторений)
#        if len(word) >= 5 and word[0] == word[-1]: 
#            results_words.append(word)
#    return (len(found_vowels), " ". join(results_words))
#print(analyze_text("Бам бам бам"))
#task 2
#process_text = lambda text: " ".join(
#    filter(lambda w: len(w) % 2 == 0, [w[::-1] for w in text.split() if w.isalpha()])) #(1. [w[::-1] for w in text.split() if w.isalpha()] - создает список, в котором каждое слово из входного текста переворачивается задом наперед, но только если оно состоит из букв (без цифр и символов). 2. filter(lambda w: len(w) % 2 == 0, ...) - фильтрует полученный список, оставляя только те слова, длина которых является четной. 3. " ".join(...) - объединяет отфильтрованные слова в одну строку, разделяя их пробелами.)
#input_str = "привет мир 123 дом книгар слон2"
#print(process_text(input_str))
#task 3
def top_k_words(text, k):