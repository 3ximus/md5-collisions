import sys
import subprocess

if len(sys.argv) != 4:
	print("Usage: generate_files <initial_block_file> <middle_block_file> <final_block_file>")
	sys.exit(1)

initial_block_file = open(sys.argv[1], 'rb') # this must be 64B long
middle_block_file = open(sys.argv[2], 'rb')
final_block_file = open(sys.argv[3], 'rb')

if len(initial_block_file.read()) != 64:
	print("Initial block file is not 64 byte long.")
	exit(1)
else: initial_block_file.seek(0)

output_file_good = open('good_script.php', 'wb')
output_file_bad = open('bad_script.php', 'wb')

# generate collision block files
subprocess.call(['fastcoll/fastcoll', sys.argv[1]])

md5_data1 = open('md5_data1', 'rb')
md5_data2 = open('md5_data2', 'rb')

# write good file
output_file_good.write(initial_block_file.read()) # write initial 64B message that produced the initial IV
output_file_good.write(md5_data1.read()) # write B0 + B1 collision blocks for the first argument of comparison
output_file_good.write(middle_block_file.read()) # write comparison operator
md5_data1.seek(0) # reset file pointer
output_file_good.write(md5_data1.read()) # write B0 + B1 again for the 2nd argument of comparison
output_file_good.write(final_block_file.read()) # write the rest of the script with branching behavior
output_file_good.close()

# reset file reader pointers
initial_block_file.seek(0)
md5_data1.seek(0)
middle_block_file.seek(0)
final_block_file.seek(0)

# do the same for bad script file, however compared blocks must be different
output_file_bad.write(initial_block_file.read())
output_file_bad.write(md5_data2.read()) # write B0' + B1' to generate collision
output_file_bad.write(middle_block_file.read())
output_file_bad.write(md5_data1.read())
output_file_bad.write(final_block_file.read())
output_file_bad.close()

md5_data1.close()
md5_data2.close()
initial_block_file.close()
middle_block_file.close()
final_block_file.close()