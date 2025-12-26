filename=~/workspaces
if [[ ! -f $filename ]]; then
    return
fi

while read -r line
do
    array=($line)
    alias cd${array[0]}="cd ${array[1]}"
done < $filename

