function register-application() {
    read "application_name? Application name: "
    application_name=$(echo "$application_name" | awk '{ for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2)); }1' | tr ' ' '_')
    read "application_location? Application location: "

    application_folder=$HOME/Career/Applications/$application_name
    mkdir -p $application_folder
    cd $application_folder
    echo "Company :- $application_name\nLocation :- $application_location\n\n~-\n\n-~\n" > "${application_name}.letter"
}

function compile-letter() {
    caller_directory=$(pwd)
    letter_file=(*.letter)

    if [[ $(echo $letter_file | wc -w) -gt 1 ]]; then
        echo "Error: Multiple letter files found. Ceasing compilation."
        return
    fi

    output_directory="${caller_directory}/generated"
    rm -rf "${output_directory}/*"
    mkdir $output_directory

    generator_workspace="$HOME/Career/Applications/Generator"
    letter_workspace="${generator_workspace}/Letter"
    virtual_env_path="${generator_workspace}/.venv-3.11/bin/python"
    script_path="${letter_workspace}/generate.py"

    cd $letter_workspace
    $virtual_env_path $script_path "${caller_directory}/${letter_file}" -o $output_directory
    cd $caller_directory
}
