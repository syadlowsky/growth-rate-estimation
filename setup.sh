# Just setup the COVID-19 folder, or update it if it exists.
if [ -d "./COVID-19" ]
then
    echo "Updating contents of COVID-19."
    cd COVID-19
    git pull
    cd ..
else
    echo "Cloning the COVID-19 JHU repository."
    git clone git@github.com:CSSEGISandData/COVID-19.git
fi
# Make sure that South Korea is correctly named.
echo "Making sure South Korea named correctly."
find ./COVID-19 \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i 's/"Korea, South"/South Korea/g'
