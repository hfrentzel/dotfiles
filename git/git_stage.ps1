function stageBranch {
    $currBranch = git branch --show-current

    git pull origin $currBranch
    if (-Not($?)) {
        Read-Host "Conflicts while pulling $currBranch. Resolve and press enter to continue " 
        git commit -m "Merge origin"
    }

    git push origin $currBranch

    git checkout $env:stageBranch
    git pull

    git merge --no-ff $currBranch
    if (-Not($?)) {
        Read-Host "Conflicts while merging $currBranch into $env:stageBranch. Resolve and press enter to continue " 
        git commit -m "Merge $currBranch into $env:stageBranch"
    }

    git push origin $env:stageBranch

    git checkout $currBranch
}
