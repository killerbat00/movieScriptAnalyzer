#!/bin/bash

# moves files greater than 1K into a directory of likely good
mkdir processed_scripts/likely_good
for f in `find processed_scripts/ -size +1k -type f`;
do mv $f processed_scripts/likely_good/;
done

