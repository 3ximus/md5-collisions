import math
import struct
import sys

def gen_chunks(string, n):
	'''yield sucessive n sized chunks from string'''
	for i in range(0, len(string), n):
		yield string[i:i+n]

def rotl(x, c):
	'''apply left rotation'''
	return (x << c) | (x >> (32 - c))

def md5_hash(message=""):
	'''process in sucessive 64bytes (512-bit) chunks'''

	# initial values
	a, b, c, d = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
	# per round shifts
	s = [7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
		5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
		4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
		6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21]

	k = []
	for i in range(64):
		k.append(int(math.floor(abs(math.sin(i + 1)) * (2**32))) & 0xffffffff)

	# break chunk into sixteen 32-bit words M[j] , 0 <= j <= 15
	for chunk in gen_chunks(message, 64):
		aa, bb, cc, dd = a, b, c, d
		words = []
		for chrs in gen_chunks(chunk, 4):
			word = ''
			# reverse to little endian
			chrs = chrs[::-1]
			for cr in chrs:
				word += '%08x' % ord(cr)
			words.append(int(word, 16))

		# main loop
		print
		for i in range(64):
			step = math.floor(i/16)
			if step == 0:
				f = (b & c) | (~b & d)
				g = i
			elif step == 1:
				f = (d & b) | (~d & c)
				g = (5 * i + 1) % 16
			elif step == 2:
				f = b ^ c ^ d
				g = (3 * i + 5) % 16
			elif step == 3:
				f = c ^ (b | ~d)
				g = (7 * i) % 16
			tmp = d
			d = c
			c = b
			print("len %d" % len(words))
			print("index %d" % g)
			b = b + rotl((a + f + k[i] + words[g]) & 0xffffffff, s[i])
			a = tmp
		# add to chunk result so far
		a = a + aa & 0xffffffff
		b = b + bb & 0xffffffff
		c = c + cc & 0xffffffff
		d = d + dd & 0xffffffff
	x = struct.pack('<LLLL', a, b, c, d)
	return x


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Give file name')
		sys.exit(1)

	print(md5_hash(sys.argv[1]))

	#f = open(sys.argv[1], 'rb')
	#filecontent = f.read()
	#f.close()
	#print(md5_hash(filecontent))
