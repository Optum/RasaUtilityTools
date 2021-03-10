import rasa

f = open("modelname.txt", "r")
x = ""

for line in f:
  stripped_line = line.rstrip()
  x += stripped_line
f.close()

config = "config.yml"
training_files = "data/"
domain = "domain.yml"
output = "models/"

model_path = rasa.train(domain, config, [training_files], output, fixed_model_name = x)
print(model_path)
