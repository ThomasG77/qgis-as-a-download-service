cd data

wget -c -i ../files_40k.txt
for f in *.7z.001 *.7z;
  do mkdir -p $(echo $f | grep -oh 'R[0-9]*' | tr [:upper:] [:lower:]);
done;

for f in *.7z.001 *.7z;
  do 7z x $f;
done;

for f in SCANEM40K_*/*/1_*/*/*.jp2;
  do mv $f "$(echo $f | grep -Eoh 'R[0-9]{2}' | tr [:upper:] [:lower:] | sort | uniq)/";
done;

rm -f *.7z.*
rm -rf SCANEM40K*

for d in r*;
  do cd $d;
     gdaltindex "scanem40k_"$d".shp" *.jp2
     cd ..;
done;

mv -f r*/*.jp2 .
gdaltindex -t_srs "EPSG:2154" "scanem40k_all.shp" *.jp2

mv */scanem40k_* .

wget -c -i ../files_10k.txt
7z x SCANEM10K_*.7z.001
