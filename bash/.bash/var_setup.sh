filename=~/sandbox/hfrentzel/configs/variables
if [[ ! -f $filename ]]; then
    return
fi

declare -A local_useful_keys
while read -r line
do
    array=($line)
    local_useful_keys[${array[0]}]=${array[1]}
done < $filename

getVar() {
    echo ${local_useful_keys[$1]}
}
