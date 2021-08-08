# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 21:03:29 2017

@author: HawkeyeZAR
"""

import re
import ntpath

from tkinter import messagebox

class Obfuscator(object):
    def __init__(self, file):
        self.file_name = file
        self.class_list = []
        self.func_list = []

    def find_words(self, orig_file):
        """
        Takes one input, the filename.

        Loops through file creating two lists.
        One list contains all the class names,
        the other list contains all the function names.

        Any builtin class or function name will be removed from the list.
        """
        with open(orig_file, 'r') as f:
            read_data = f.read()
            # Find all class names and save it as a list for later use
            find_class = re.findall(r'Class (.*?)\(', read_data, re.I | re.DOTALL)
            self.class_list.extend(find_class)
            # Delete any built in classes from the list. Cannot be renamed.
            for x, y in enumerate(self.class_list):
                if y.startswith('_'):
                    del self.class_list[x]
            # Find all function names and save it as a list for later use
            find_func = re.findall(r'def (.*?)\(', read_data, re.I | re.DOTALL)
            self.func_list.extend(find_func)
            # Delete any built in functions from list. Cannot be renamed.
            for x, y in enumerate(self.func_list):
                if y.startswith('_'):
                    del self.func_list[x]
                if 'main' in y:
                    del self.func_list[x]

    def replace_words(self, file_txt, rep_words):
        """
        Takes two inputs,
        the text data containing the words you want replaced
        and a dictionery containing the old values and the new values

        Returns the updated text to be written to file
        """
        
        for key, val in rep_words.items():
            file_txt = re.sub(r'\b{0}\b'.format(key), val, file_txt)
        return file_txt

    def obf_word_dict(self, obf_dict, obf_str):
        """
        Takes two arguments as input, a list value and a string value.
        And returns a dictionery.
        
        List contains words to get replaced
        The string contains the obfuscate string name
        """
        
        obf_counter = 111
        obf_word = {}
        for i, v in enumerate(obf_dict):
            obf_word[v] = obf_str + str(obf_counter)
            obf_counter += 1
        return obf_word

    def obf_data(self, orig_file):
        """
        First calls the self.find_words() function and ignores all builtin
        class and function names.
        The results are added to the self.class_list and self.func_list lists.
        
        Calls the obf_word_dict function and returns dictioneries containing
        obf_str_class and obf_str_func values and all class names and
        function names generated by the previous 2 lists.
        The two dictioneries are then merged into one

        self.class_list and self.func_list are stored as the dict.keys
        obf_str_class and obf_str_func are stored as dict.values

        Finally the replace_words() function is called.
        """
        
        self.find_words(orig_file)
        obf_str_class = 'vwxyz'
        obf_word_class = self.obf_word_dict(self.class_list, obf_str_class)
        obf_str_func = 'zyxwv'
        obf_word_func = self.obf_word_dict(self.func_list, obf_str_func)

        # merge dictioneries into one dictionery
        merged_dict = {**obf_word_class, **obf_word_func}

        # read file and save it as variable read_data
        with open(orig_file, 'r') as f:
            read_data = f.read()

        # call the replace words function, save data to new file
        new_data = self.replace_words(read_data, merged_dict)
        #new_file = 'obf_' + ntpath.basename(orig_file)
        path, file = ntpath.split(orig_file)
        new_name = 'obf_' + file
        new_file = path + '/' + new_name
        message = 'All user class and function names have been obfuscated.'
        try:
            with open(new_file, 'r+') as f:
                f.write(new_data)
            messagebox.showinfo('Obfuscation Successful', message)
        except:
            with open(new_file, 'w') as f:
                f.write(new_data)
            messagebox.showinfo('Obfuscation Successful', message)

    def del_blank_lines(self, orig_file):
        """
        Removes all empty lines and
        lines that contain only whitespaces.
        """
        
        # new_file = 'obf_' + ntpath.basename(orig_file)
        path, file = ntpath.split(orig_file)
        new_name = 'obf_' + file
        new_file = path + '/' + new_name
        message = 'All blank lines have successfully been removed.'
        try:
            with open(orig_file) as in_file, open(new_file, 'r+') as out_file:
                out_file.writelines(line for line in in_file if line.strip())
                out_file.truncate()
            messagebox.showinfo('Success', message)
        except:
            with open(orig_file) as in_file, open(new_file, 'w') as out_file:
                out_file.writelines(line for line in in_file if line.strip())
                out_file.truncate()
            messagebox.showinfo('Success', message)

    def del_doc_str(self, orig_file):
        """
        Removes all doc_strings.
        
        Removes all comments that are on a seperate line.
        Comments placed after code will be ignored.
        """

        def encode_list(lst):
            encoded_lst = []
            decode_str = "decode('cp037')"
            for i in lst:
                encoded_lst.append(i.encode('cp037'))
            return encoded_lst

        path, file = ntpath.split(orig_file)
        new_name = 'obf_' + file
        new_file = path + '/' + new_name
        message = 'All comments and doc strings have been encoded.'

        with open(orig_file, 'r') as f:
            text = f.read()

        # compile regex expressions
        comm_regex = re.compile(r'#(.*?)\n', re.DOTALL)
        docstr_regex1 = re.compile(r'\"\"\"(?:.|\n)*?\"\"\"', re.I | re.DOTALL)
        docstr_regex2 = re.compile(r'\'\'\'(?:.|\n)*?\'\'\'', re.I | re.DOTALL)
        # Store regex reults as a list
        comment = comm_regex.findall(text)
        doc_str1 = docstr_regex1.findall(text)
        doc_str2 = docstr_regex2.findall(text)
        # create new encoded lists from the regex lists
        coded_commment = encode_list(comment)
        coded_doc_str1 = encode_list(doc_str1)
        coded_doc_str2 = encode_list(doc_str2)

        for i in range(len(doc_str1)):
            result = re.sub(doc_str1[i], str(coded_doc_str1[i]), text)
            print(doc_str1[i])
        #add_obfuscation(doc_str1, coded_doc_str1, text)
        #add_obfuscation(doc_str2, coded_doc_str2, text)

                
##        try:
##            with open(new_file, 'r+') as f:
##                add_obfuscation(comment, coded_commment)
##                add_obfuscation(doc_str1, coded_doc_str1)
##                add_obfuscation(doc_str2, coded_doc_str2)
##                f.write(new_data)
##            messagebox.showinfo('Success', message)
##        except:
##            with open(new_file, 'w') as f:
##                f.write(new_data)
##            messagebox.showinfo('Success', message)



##file_name = 'test script.py'   
##obf = Obfuscator(file_name)
##obf.find_words(file_name)
##obf.obf_data()
##obf.del_blank_lines()
##obf.del_doc_str(file_name)





