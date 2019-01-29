import pandas as pd
import numpy as np

inp = pd.read_csv("16 17 list.csv")
k = inp.values[1]
with open("temp.py","w") as out :
    out.write("dictionary = {")
    for person in inp.values :
        p = person[0]
        id_name = str(p)+"_name"
        id_email = str(p)+"_email"
        pp = "\"" + str(id_name) + "\"" +":"+"\""+str(person[1])+"\""+","
        ppp = "\"" + str(id_email) + "\"" + ":"+"\"" +person[1]+"@mechyd.ac.in"+"\""+","
        out.write(pp)
        out.write(ppp)
        print(pp)
        print(ppp)
        # print(person[0])
    out.write("}")




















