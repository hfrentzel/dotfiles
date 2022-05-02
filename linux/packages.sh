
install_packages () {
    package_list=("$@")

    installed_packages=$(dpkg -l)
    install_command="sudo apt-get install"

    for i in "${package_list[@]}"; do
        found_package=$(echo "$installed_packages" | grep " $i")
        if [ -z "$found_package" ]; then
            install_command="$install_command $i"
        else
            echo "$found_package"
        fi              
    done

    if [ "$install_command" != "sudo apt-get install" ]; then
        echo "$install_command"
        eval $install_command
    fi
}

