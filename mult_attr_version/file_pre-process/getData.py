import string

file_ob = open('in.data','r')
file_writer = open('data.txt','a')

worker_class = []
edu = []
race = []
birth_country = []

file_writer.write('worker_class,')
file_writer.write('edu,')
file_writer.write('race,')
file_writer.write('birth_country\n')

for line in file_ob:
	tmp_list = string.split(line,', ')
	worker_class.append(tmp_list[1])
	edu.append(tmp_list[4])
	race.append(tmp_list[10])
	birth_country.append(tmp_list[33])
	#write to a new txt file
	file_writer.write(worker_class[-1]+',')
	file_writer.write(edu[-1]+',')
	file_writer.write(race[-1]+',')
	file_writer.write(birth_country[-1] + '\n')


