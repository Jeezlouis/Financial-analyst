git init
git add .
read -p "Enter commit message: " message
git commit -m "$message"
git branch -M main
read -p "Enter the repo url: " url
git remote add origin $url
git push origin main