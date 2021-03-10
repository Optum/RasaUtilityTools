import csv
import pandas as pd
import fileinput

line_indexes = []

with open("newfaq.md") as file_in:
    lines = []
    for line in file_in:
      print(line)
      if "### " in line:
        question = line
        chatquestion = question.replace('### ','')
        with open("faq.mdx", "a+") as myfile:
          if chatquestion not in open('faq.mdx').read():
            myfile.write("\n")
            myfile.write("\n" + question)

      if "intent" in line:
        intent = line
        chatintent = intent.replace('intent: ','')
        with open("./data/nlu.md", "a+") as myfile:
          if chatintent not in open('./data/nlu.md').read():
            myfile.write("\n")
            myfile.write("\n" + "## intent:" + chatintent.replace(" ", "_"))
            myfile.write("- " + chatquestion) # This is working as expected, probably appending to the row below the latest

        with open("domain.yml", "r+") as myfile: # Working to modify specific portions
          contents = myfile.readlines()
          for i, line2 in enumerate(contents):
            if "entities:" in line2 and "_entities:" not in line2 and chatintent not in contents[i - 1]:
              contents.insert(i, "- " + chatintent)
              myfile.seek(0)
              myfile.writelines(contents)
              myfile.truncate()
              break

      if "altquestion:" in line:
        altquestion = line
        altquestion2 = altquestion.replace('altquestion:','-')
        print(altquestion2)
        with open("./data/nlu.md", "a+") as myfile:
          if altquestion2 not in open('./data/nlu.md').read():
            myfile.write(altquestion2)

      if "answer: " in line:
        answer = line
        answer2 = answer.replace('answer: ','').rstrip()
        with open("faq.mdx", "a+") as myfile:
          if answer2.rstrip() not in open('faq.mdx').read():
            myfile.write("\n" + answer2.rstrip())

       
        with open("domain.yml", "r+") as myfile: # Working to modify specific portions
          contents = myfile.readlines()
          noforms = True #Initial logic to append files if the forms field is not being used
          for i, line2 in enumerate(contents):
            if "actions:" in line2 and answer2 not in contents[i - 1]:
              contents.insert(i, "  - text: " + answer2 + "\n")
              contents.insert(i, "  utter_" + chatintent.rstrip() + ":\n")
              myfile.seek(0)
              myfile.writelines(contents)
              myfile.truncate()
              
            if "forms:" in line2 and chatintent not in contents[i - 1]:
              noforms = False
              contents.insert(i, "- utter_" + chatintent.rstrip() + "\n")
              myfile.seek(0)
              myfile.writelines(contents)
              myfile.truncate()

            if "forms" in line2:
              noforms = False
              
          print(noforms) # Logic to apply utterances without forms
          if noforms:
            contents.append("\n- utter_" + chatintent.rstrip())
            myfile.seek(0)
            myfile.writelines(contents)
            myfile.truncate()

        with open("./data/stories.md", "a+") as myfile: # Working to modify specific portions
          intent2 = intent.replace('intent: ','').rstrip()
          if chatintent not in open('./data/stories.md').read():
            myfile.write("\n\n## " + intent2)
            myfile.write("\n" + "* " + chatintent.rstrip())
            myfile.write("\n" + "   - utter_" + chatintent.rstrip())
            myfile.write("\n" + "   - action_restart")
            
with open("./working.txt", "a+") as myfile:
    myfile.write("It worked")
