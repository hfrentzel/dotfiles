stageBranch() {
    if [ -z "$STAGE_BRANCH" ]; then
        echo "No stageBranch defined"
        return
    fi

    git diff --quiet
    if [[ $? -ne 0 ]]; then
        echo "Uncommitted changes on working tree. Commit and retry"
        return
    fi

    currBranch=$(git branch --show-current)

    git pull origin $currBranch
    if [[ $? -ne 0 ]]; then
        echo "Conflicts while pulling $currBranch. Resolve and press enter to continue "
        read NULL
        git commit -m "Merge origin"
    fi

    git push origin $currBranch

    git checkout $STAGE_BRANCH
    git pull

    git merge --no-ff $currBranch
    if [[ $? -ne 0 ]]; then
        echo "Conflicts while merging $currBranch into $STAGE_BRANCH. Resolve and press enter to continue"
        read NULL
        git commit -m "Merge $currBranch into $STAGE_BRANCH"
    fi

    git push origin $STAGE_BRANCH
    git checkout $currBranch
}

