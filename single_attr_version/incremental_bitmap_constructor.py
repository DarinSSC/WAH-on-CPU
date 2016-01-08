import numpy

file_ob = open('input.txt','r')
#file_all_lines = file_ob.readlines()

input_data = []
for line in file_ob:
	input_data.append(int(line))

input_length = len(input_data)
row_id = range(input_length)

print "input_length: " + str(input_length)

cardinality = 6 #the cardinality of the attribute
word_size = 32  #length of a word
chunk_size = 31
bitmap = []
for i in xrange(cardinality):
	bitmap.append([])

w = numpy.random.randint(1, size = [cardinality,word_size])
appeared_value = []
appear_flag = [0 for i in xrange(cardinality)]

for row_counter in range(input_length+1)[1:input_length+1]:
	value = input_data[row_counter-1]
	w[value][(row_counter-1)%32] = 1
	if(appear_flag[value] == 0):
		appeared_value.append(value)
		appear_flag[value] = 1
	print "row_counter:  "+str(row_counter)
	if(row_counter%32 == 0):
		print "**************"+str(row_counter/32)+"**************"
		for i in appeared_value:
			for j in xrange(row_counter/32-len(bitmap[i])/32-1):
				bitmap[i].extend([0 for j in xrange(word_size)])
			bitmap[i].extend(w[i])
			w[i] = [0 for j in xrange(word_size)]
		appeared_value = []
		appear_flag = [0 for i in xrange(cardinality)]
for i in range(cardinality):
	for j in xrange(len(input_data)/32-len(bitmap[i])-1):
				bitmap[i].extend(numpy.random.randint(1,[wowrd_size]))

if __name__ == '__main__':
	for row in range(input_length):
		print input_data[row], bitmap[0][row], bitmap[1][row] ,bitmap[2][row], bitmap[3][row], bitmap[4][row], bitmap[5][row]
		
	
