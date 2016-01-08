import numpy

file_ob = open('input.txt','r')
#file_all_lines = file_ob.readlines()

input_data = []
for line in file_ob:
	input_data.append(int(line))

input_length = len(input_data)
row_id = range(input_length)

def even_odd_sorting(input_data,row_id):
	for i in xrange(len(input_data)):
		if(i % 2 == 0):
			for j in xrange(input_length/2):
				if input_data[2*j] > input_data[2*j+1]:
					input_data[2*j],input_data[2*j+1] = input_data[2*j+1],input_data[2*j]
					row_id[2*j],row_id[2*j+1] = row_id[2*j+1],row_id[2*j]
		if(i % 2 == 1):
			for j in xrange((input_length-1)/2):
				if input_data[2*j+1] > input_data[2*(j+1)]:
					input_data[2*j+1],input_data[2*(j+1)] = input_data[2*(j+1)],input_data[2*j+1]
					row_id[2*j+1],row_id[2*(j+1)] = row_id[2*(j+1)],row_id[2*j+1]
	return input_data,row_id

def set_bit(num,off_set):
	#off_set should be range from 0 to 31.
	#The right bit refers to 0 while the left to 31
	mask = 1<<off_set
	return (num|mask)
	
def bin(s):
	#transform the integer to the type of binary code
	#return value is a string
	return str(s) if s<=1 else bin(s>>1) + str(s&1)

#step 1: sort row_id by values(even_odd sorting)
input_data,row_id = even_odd_sorting(input_data,row_id)

#step 2: produce chunk_id and literal
chunk_size = 31
chunk_id = [-1 for i in xrange(input_length)]
literal = [0 for i in xrange(input_length)]
for i in xrange(input_length):
	chunk_id[i] = row_id[i]/31
	literal[i] = set_bit(literal[i],31) #the left bit set to 1
	off_set = 30-row_id[i]%31
	literal[i] = set_bit(literal[i],off_set)

#step 3: reduce by key_pair(value,chunk_id)
scanned_input_data = [input_data[0]]
scanned_chunk_id = [chunk_id[0]]
scanned_literal = [literal[0]]

head = [1] #1 if chunk_id is the 1st of the value else 0

for i in xrange(1,input_length):
	if input_data[i]==scanned_input_data[-1] and chunk_id[i] == scanned_chunk_id[-1]:
		scanned_literal[-1] |= literal[i]
	else:
		if input_data[i]!=scanned_input_data[-1]:
			head.append(1)
		else:
			head.append(0)
		scanned_input_data.append(input_data[i])
		scanned_chunk_id.append(chunk_id[i])
		scanned_literal.append(literal[i])

scanned_length = len(scanned_input_data)

#step 4: prodece 0-Fill word
fill_0_word = [0 for i in xrange(scanned_length)]

for i in xrange(scanned_length):
	if head[i] == 0:
		fill_0_word[i] = scanned_chunk_id[i] - scanned_chunk_id[i-1] - 1
	else:
		fill_0_word[i] = scanned_chunk_id[i] #0,1,2...scanned_chunk_id[i]-1
		pass

#step 5: get index by interleaving 0-Fill word and literal(also remove all-zeros word)
out_index = [0 for i in xrange(2*scanned_length)]
for i in xrange(scanned_length):
	out_index[2*i] = fill_0_word[i]
	out_index[2*i+1] = scanned_literal[i]
out_index = filter(lambda x:x>0,out_index) #remove all zeros
index_length = len(out_index)

#step 6: get offsets and key
tmp_array = [1 for i in xrange(scanned_length)]
for i in xrange(scanned_length):
	if fill_0_word[i] != 0:
		tmp_array[i] += 1
#6.1: index length for each key
key_idx_length = [tmp_array[0]]
for i in xrange(1,scanned_length):
	if scanned_input_data[i] == scanned_input_data[i-1]:
		key_idx_length[-1] += tmp_array[i]
	else:
		key_idx_length.append(tmp_array[i])
#6.2: offset for each key in the whole index
offset = [0 for i in key_idx_length] 
for i in xrange(1,len(key_idx_length)):
	offset[i] = offset[i-1] + key_idx_length[i-1]


if __name__ == '__main__':
	for i in xrange(input_length):
		print input_data[i], row_id[i], chunk_id[i], bin(literal[i])
	print len(scanned_input_data)
	for i in xrange(len(scanned_input_data)):
		print scanned_input_data[i], scanned_chunk_id[i], bin(scanned_literal[i]), fill_0_word[i]
	print len(out_index)
	for i in out_index:
		print bin(i)
	print key_idx_length
	print offset
