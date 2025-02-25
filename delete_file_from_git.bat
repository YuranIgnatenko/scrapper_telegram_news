git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch путь/к/файлу.txt' --prune-empty --tag-name-filter cat -- --all
