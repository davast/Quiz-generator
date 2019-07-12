import urllib.request
import json
import configparser
import re

class Quiz:

    def __init__(self, file, mode):
        self.file = file
        self.mode = mode

    def types(self):
        config = configparser.ConfigParser()
        config.read(self.mode)
        self.mark = config["general"]["mark"]
        return getattr(self, config["general"]["mode"])()


    def generate(self):
        url = self.file
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        with open('quiz.json', 'w') as json_file:
            json.dump(data, json_file)

        return "file crertaed with quiz.json name"


    def interactive(self):
        make = self.json_to_txt()
        with open(make, "r") as f:
            f = f.read()
            f = f.strip().split("****")
            answers = ("A","B","C","D","E")
            with open(make, "w") as fw:
                for line in f[1:]:
                    print(line)
                    while True:
                        inp = input("please select correct answer: ")
                        if inp not in answers:
                            print("Please fill one of this (A,B,C,D,E)")
                        else:
                            break
                    line = line.replace(inp+".", self.mark+inp+".")

                    fw.write(line)


    def json_to_txt(self):
        with open("quiz.json", "r") as f:
            f = json.load(f)

        with open("quiz.txt", "w") as fw:
            next = 1
            fw.write(list(f.keys())[0] + " " + list(f.values())[0] + "\n")
            fw.write("\t" + list(f.keys())[1] + "\n")
            for item in list(f.values())[1]:
                for k, v in item.items():
                    if isinstance(v, str):
                        fw.write("*"*4 + "\n")
                        fw.write("\n" + str(next) + ". " + v + "\n")
                        next += 1
                    else:
                        alpha = 65
                        for item in v:
                            fw.write("\t"*2 + chr(alpha) + ". " + item + "\n")
                            alpha += 1

        return "quiz.txt"





path = Quiz("http://devel.pythonanywhere.com/quiz/static/quiz.json", "config.ini")
print(path.types())
