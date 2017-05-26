#include <iostream>
#include <fstream>
#include <time.h>
#include <stdio.h>

#include "main.hpp"

using namespace std;

// IV = 0123456789abcdeffedcba9876543210
const uint32 MD5IV[] = { 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476 };

unsigned load_block(istream& i, uint32 block[]);
void save_block(ostream& o, const uint32 block[]);
void find_collision(const uint32 IV[], uint32 msg1block0[], uint32 msg1block1[], uint32 msg2block0[], uint32 msg2block1[], bool verbose = false);

int main(int argc, char *argv[]) {
	if (argc != 2) {
		printf("Usage: %s <file_name>\n", argv[0]);
		return 0;
	}

	seed32_1 = uint32(time(NULL));
	seed32_2 = 0x12345678;
	uint32 IV[4] = { MD5IV[0], MD5IV[1], MD5IV[2], MD5IV[3] };

	ifstream ifs(argv[1], ios::binary);
	ofstream ofs1("md5_data1", ios::binary);
	ofstream ofs2("md5_data2", ios::binary);

	uint32 block[16];
	while (true) {
		unsigned len = load_block(ifs, block);
		if (len) {
			//save_block(ofs1, block);
			//save_block(ofs2, block);
			md5_compress(IV, block);
		} else
			break;
	}

	uint32 msg1block0[16];
	uint32 msg1block1[16];
	uint32 msg2block0[16];
	uint32 msg2block1[16];
	find_collision(IV, msg1block0, msg1block1, msg2block0, msg2block1, true);

	save_block(ofs1, msg1block0);
	save_block(ofs1, msg1block1);
	save_block(ofs2, msg2block0);
	save_block(ofs2, msg2block1);

	return 0;
}

unsigned load_block(istream& i, uint32 block[]) {
	unsigned len = 0;
	char uc;
	for (unsigned k = 0; k < 16; ++k) {
		block[k] = 0;
		for (unsigned c = 0; c < 4; ++c) {
			i.get(uc);
			if (i) ++len;
			else uc = 0;
			block[k] += uint32((unsigned char)(uc))<<(c*8);
		}
	}
	return len;
}

void save_block(ostream& o, const uint32 block[]) {
	for (unsigned k = 0; k < 16; ++k)
		for (unsigned c = 0; c < 4; ++c)
			o << (unsigned char)((block[k] >> (c*8))&0xFF);
}

void find_collision(const uint32 IV[], uint32 msg1block0[], uint32 msg1block1[], uint32 msg2block0[], uint32 msg2block1[], bool verbose) {
	if (verbose) cout << "Generating first block: " << flush;
	find_block0(msg1block0, IV);

	uint32 IHV[4] = { IV[0], IV[1], IV[2], IV[3] };
	md5_compress(IHV, msg1block0);

	if (verbose) cout << endl << "Generating second block: " << flush;
	find_block1(msg1block1, IHV);

	for (int t = 0; t < 16; ++t) {
		msg2block0[t] = msg1block0[t];
		msg2block1[t] = msg1block1[t];
	}
	msg2block0[4] += 1 << 31; msg2block0[11] += 1 << 15; msg2block0[14] += 1 << 31;
	msg2block1[4] += 1 << 31; msg2block1[11] -= 1 << 15; msg2block1[14] += 1 << 31;
	if (verbose) cout << endl;
}
