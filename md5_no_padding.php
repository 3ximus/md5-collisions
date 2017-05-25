<?php

// apply left rotation
function rotl ($x, $c) {
    return ($x << $c) | ($x >> (32 - $c));
}

//Process the message in successive 512-bit chunks:
function md5_hash($message) {

    //Initialize variables:
    list($a, $b, $c, $d) = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476];

    // specify per-round shift amounts
    $s = [ 7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
           5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
           4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
           6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21];

    $K = [];
    for ($i =0; $i < 64; $i++) {
        $K[$i] = floor(abs(sin($i + 1)) * (pow(2, 32))) & 0xffffffff;
    }

    // break chunk into sixteen 32-bit words M[j], 0 ≤ j ≤ 15
    $chunks = str_split($message, 64);
    foreach ($chunks as $chunk) {
        list($aa, $bb, $cc, $dd) = [$a, $b, $c, $d];
        $words = str_split($chunk, 4);
        foreach ($words as $i => $chrs) {
            $chrs = str_split($chrs);
            $word = '';
            //little endian
            $chrs = array_reverse($chrs);
            foreach ($chrs as $chr) {
                $word .= sprintf('%08b', ord($chr));
            }
            $words[$i] = bindec($word);
        }
        //Main loop:
        for ($i = 0; $i < 64; $i++) {
            $step = floor($i /16);
            switch ($step) {
                case 0;
                    $f = ($b & $c) | (~$b & $d);
                    $g = $i;
                    break;
                case 1;
                    $f = ($d & $b) | (~$d & $c);
                    $g = (5 * $i + 1) % 16;
                    break;
                case 2;
                    $f = $b ^ $c ^ $d;
                    $g = (3 * $i + 5) % 16;
                    break;
                case 3;
                    $f = $c ^ ($b | ~$d);
                    $g = (7 * $i) % 16;
                    break;
            }
            $temp = $d;
            $d = $c;
            $c = $b;
            $b = $b + rotl(($a + $f + $K[$i] + $words[$g]) & 0xffffffff, $s[$i]) ;
            $a = $temp;
        }
        // add this chunk's hash to result so far:
        $a = $a + $aa & 0xffffffff;
        $b = $b + $bb & 0xffffffff;
        $c = $c + $cc & 0xffffffff;
        $d = $d + $dd & 0xffffffff;
    }
    $x = pack('V4', $a, $b, $c, $d);
    return bin2hex($x);
}

$inputFile = $argv[1];
echo md5_hash(file_get_contents(__DIR__."/$inputFile"));
