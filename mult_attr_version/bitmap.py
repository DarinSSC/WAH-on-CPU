import data
import numpy

def set_bit(num,off_set):
	#off_set should be range from 0 to 31.
	#The right bit refers to 0 while the left to 31
	mask = 1<<off_set
	return (num|mask)
	
def bin(s):
	#transform the integer to the type of binary code
	#return value is a string
	return str(s) if s<=1 else bin(s>>1) + str(s&1)

def even_odd_sorting(input_data,row_id):#step 1
	input_length = len(input_data)
	for i in xrange(input_length):
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

def produce_chId_lit(row_id):#step 2
	input_length = len(row_id)
	chunk_id = [-1]*input_length
	literal = [0 for i in xrange(input_length)]
	for i in xrange(input_length):
		chunk_id[i] = row_id[i]/31
		literal[i] = set_bit(literal[i],31) #the left bit set to 1
		off_set = 30-row_id[i]%31
		literal[i] = set_bit(literal[i],off_set)
	return chunk_id,literal

def reduce_by_key(input_data, chunk_id, literal):#step 3
	input_length = len(input_data)
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
	return scanned_input_data,scanned_chunk_id,scanned_literal,head

def produce_0_fill(head, scanned_chunk_id):#step 4
	scanned_length = len(head)
	fill_0_word = [0]*scanned_length

	for i in xrange(scanned_length):
		if head[i] == 0:
			fill_0_word[i] = scanned_chunk_id[i] - scanned_chunk_id[i-1] - 1
		else:
			fill_0_word[i] = scanned_chunk_id[i] #0,1,2...scanned_chunk_id[i]-1
			pass
	return fill_0_word

def getIdx(fill_0_word,scanned_literal):#step 5: get index by interleaving 0-Fill word and literal(also remove all-zeros word)
	scanned_length = len(scanned_literal)
	out_index = [0]*(2*scanned_length)
	for i in xrange(scanned_length):
		out_index[2*i] = fill_0_word[i]
		out_index[2*i+1] = scanned_literal[i]
	out_index = filter(lambda x:x>0,out_index) #remove all zeros
	return out_index

def get_idxlen_offset(fill_0_word,scanned_input_data):#step 6: get offsets and key
	scanned_length = len(fill_0_word)
	tmp_array = [1]*scanned_length
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
	return key_idx_length,offset

if __name__ == '__main__':
	path = 'data.txt'	#file path
	attr_dict,attr_values,attr_value_NO = data.openfile(path)
	total_row = len(attr_values[0])
	for input_data in attr_values:
		row_id = range(total_row)
		input_data,row_id = even_odd_sorting(input_data,row_id)#step 1
		chunk_id,literal = produce_chId_lit(row_id)#step2
		scanned_input_data,scanned_chunk_id,scanned_literal,head = reduce_by_key(input_data, chunk_id, literal)#step 3
		fill_0_word = produce_0_fill(head, scanned_chunk_id)#step 4
		out_index = getIdx(fill_0_word,scanned_literal)#step 5
		key_idx_length,offset = get_idxlen_offset(fill_0_word,scanned_input_data)
