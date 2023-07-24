# trie operations Analysis
# 1.add new word to the dic: O(M), 
#                            where M is the length of the new word.
# 2.Space Complexity ≈ O(N * L * B)

# 3. find nearest 4 words:  O(N * M * log(M)),
#                   N: Number of words in the Trie.
#                   M: Average length of a word in the Trie.
# in depth analysis of each part is written inside the function

# Where:
# N: The number of words in the dictionary.
# L: The average length of the words.
# B: The branching factor of the trie (e.g., 26 for the English alphabet).



from Trie import Trie
class SpellChecker:
    def __init__(self,dictionary_route):
        self.words=[]
        self._read_dictionary_from_file(dictionary_route)
        self.dic : Trie =self._store_dic()  


    def _read_dictionary_from_file(self, dictionary_route):
        # the encoding MacRoman was detected using chardetect  
        try:
            with open(dictionary_route, 'r',encoding='MacRoman') as file:
                for line in file:
                    self.words.append(line.strip())
        except FileNotFoundError:
            print(f"File not found: {dictionary_route}")


    def _build_trie(self,word_list):
        trie = Trie()
        for word in word_list:
            trie.insert(word)
        return trie
    
    def _store_dic(self):
        return self._build_trie(self.words)
        
    
    def add_word(self,word):
        self.dic.insert(word)
        
    def is_in_dic(self,word)->bool:
        return self.dic.search(word)
    
    def _in_order_traversal(self, node, prefix, words_list):

        # Time complexity: O(N * M * log(M))
        # N: Number of words in the Trie.
        # M: Average length of a word in the Trie.

        # Space complexity: O(M)

        for char, child_node in sorted(node.children.items()):
            new_prefix = prefix + char
            if child_node.is_end_of_word:
                words_list.append(new_prefix)
            self._in_order_traversal(child_node, new_prefix, words_list)

    def _get_sorted_words(self):
        words_list = []
        self._in_order_traversal(self.dic.root, '', words_list)
        return words_list
    
    def nearest_words(self,word):
        '''
        Returns a list of the 4 nearest words to the input word.
        If the input word is in the dictionary, returns an empty list.
        '''
        
        # Time complexity: O(N * M * log(M))
        # The method calls _get_sorted_words, which has a time complexity of O(N * M * log(M)),
        # and then performs binary search with a time complexity of O(log(N)).
        # Space complexity: O(M)

        if self.is_in_dic(word):
            return []
        else:
            # convert the trie to a list of words sorted alphabetically
            words_list = self._get_sorted_words()
            # find the index of the input word in the list by binary search
            index = self._binary_search(words_list, word)
            return words_list[index-2:index]+ words_list[index:index+2]

    def _binary_search(self, words_list, word):
        # Time complexity: O(log(N))
        # N: Number of words in the words_list.
        # Space complexity: O(1)
        start = 0
        end = len(words_list) - 1
        while start <= end:
            mid = (start + end) // 2
            if words_list[mid] == word:
                return mid
            elif words_list[mid] < word:
                start = mid + 1
            else:
                end = mid - 1
        return start       
  

if __name__ == "__main__":
    spell_checker = SpellChecker("dictionary.txt")

    print(spell_checker.nearest_words("aaaa"))
    spell_checker.add_word("aaaa")
    print(spell_checker.nearest_words("aaaa"))

