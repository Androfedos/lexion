#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Губанов Фёдор (gubanov-fedja@yandex.ru)
# Lexion - программа вычисляющая количество не повторяющихся слов в документах, что позволит узнать некий словарный запас, слова паразиты и наличие украшающих слов
# Для установки морфологического анализатора нужно:
# pip install pymorphy2

import os
import re
import pymorphy2

#Как вычитать словари
#Чтобы получить элементы словаря A, которые не находятся в B, основываясь только на ключе:
#C = {k:v for k,v in A.items() if k not in B}
#Чтобы получить элементы словаря A, которые не находятся в B, на основе ключа и значения:
#C = {k:v for k,v in A.items() if k not in B or v != B[k]}    

# Путь к директории с текстовыми файлами в кодировке ... 
corpus_dir = "c:/Users/PRO-GubanovAN/Dropbox/Прочее/Python/lexion/corpus"

morph = pymorphy2.MorphAnalyzer(lang='ru')

#Словарь ключ - нормальная форма слова, значение - кол-во
normals={}



#Обработка слова
def process_word(word):
  #print(word)
  lexemms = morph.parse(word)
  #print(lexemms)
  if len(lexemms):
    norm_word = lexemms[0].normal_form
    count = normals.get(norm_word,0)
    #print(f"Слово: {norm_word}, score:{lexemms[0].score}, len(lexemms):{len(lexemms)}, methods_stack:{lexemms[0].methods_stack[0][0]}, methods_num:{len(lexemms[0].methods_stack)}")
    #print(lexemms)
    normals[norm_word]=count+1

# Обработка файла
def process_file(fname):
  print(fname)
  #utf-8-sig
  with open(fname, mode="r", encoding="cp1251") as f:
    lines = f.readlines()
    for line in lines:
      #print(line)
      #words = re.split(r'[#;,.\s]\s*', line)
      words = re.findall(r"[\w']+", line)
      #print(words)
      for word in words:
        if word:
          process_word(word)

    with open(fname+".csv", mode="w", encoding="cp1251") as fo:
      for norm_word, count in normals.items(): 
        fo.write(f"{norm_word};{count}\n")

# Перебираем все файлы в директории
for filename in os.listdir(corpus_dir):
  process_file( os.path.join(corpus_dir, filename))