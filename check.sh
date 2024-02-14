#/bin/bash

TESTS="bonus_tests/*.l"

rm -rf bonus_tests/out
mkdir bonus_tests/out

for file in $TESTS; do
	name=$(echo $file | cut -d'/' -f2 | cut -d'.' -f1)
	python3.12 -m src.main $file > "bonus_tests/out/$name.out"

	echo -n $file
	echo -n ": "

	diff -q "bonus_tests/out/$name.out" "bonus_tests/ref/$name.ref" > /dev/null
	if [ $? -eq 0 ]; then
		echo "OK"
	else
		echo "FAIL"
		echo "Expected:"
		cat "bonus_tests/ref/$name.ref"
		echo "Got:"
		cat "bonus_tests/out/$name.out"
		echo ""
	fi
done
